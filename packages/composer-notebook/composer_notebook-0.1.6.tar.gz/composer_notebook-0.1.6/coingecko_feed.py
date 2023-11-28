import requests
from molang.models import *
from molang.helper import *
from molang.core import *

def get_coin_id(coin_symbol) -> str:
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    coins_list = response.json()
    matched_coins_symbol = [c for c in coins_list if c["symbol"] == coin_symbol]
    if len(matched_coins_symbol) == 0:
        raise ValueError(f"no matched coins form symbol {coin_symbol}")
    if len(matched_coins_symbol) == 1:
        return matched_coins_symbol[0]["id"]
    formatted_coins = "coins id list:\n" + "\n".join(d['id'] for d in matched_coins_symbol)

    # llm filter coins
    filter_sys = f"""
    You are a content filter and ID picker, you are given a range of 
    crypto coins that matches the symbol

    your task is to pick the most relevant coin name that best matches the symbol
    you must only pick one ID. you must also make sure to output the ID in the next message, DO NOT write any other messages aside from an ID you pick
    the ID in the next message you output must match one of the coins id list.

    for example:
    Input:
    usdt

    coins id list:
    tether
    bridged-tether-(fuse)
    tether-6069e553
    tether
    UnstableStableDependableToken

    Output:
    tether
    ----
    Input:
    {coin_symbol}
    
    {formatted_coins}
    Output:
    """
    sys_message = Message("system", filter_sys)
    initial_memory = Memory(messages=[sys_message], state={})
    initial_chain = add_message()(initial_memory)
    coin_id_chain = initial_chain | oai_chat_complete()
    coin_id = coin_id_chain.memory.messages[-1].content
    matching_real_id_check = next((item for item in matched_coins_symbol if item['id'] == coin_id), None)
    if matching_real_id_check is None:
        raise ValueError(f"no coin for ID found from LLM coin picker: {coin_id}")
    return coin_id

def get_market_data(coin_id):
    params = {
        "vs_currency": "usd",
        "ids": coin_id,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d,30d,1y"
    }
    response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch market data")

    return response.json()

def format_market_data(data):
    formatted_data = []

    for item in data:
        formatted_item = (
            f"Name: {item['name']}, "
            f"Current Price: ${item['current_price']:,.2f}, "
            f"Market Cap: ${item['market_cap']:,.2f}, "
            f"Market Cap Rank: {item['market_cap_rank']}, "
            f"Fully Diluted Valuation: ${item['fully_diluted_valuation']:,.2f}, "
            f"Total Volume: ${item['total_volume']:,.2f}, "
            f"High 24h: ${item['high_24h']:,.2f}, "
            f"Low 24h: ${item['low_24h']:,.2f}, "
            f"Price Change 24h: ${item['price_change_24h']:,.2f}, "
            f"Price Change Percentage 24h: {item['price_change_percentage_24h']:.2f}%, "
            f"Market Cap Change 24h: ${item['market_cap_change_24h']:,.2f}, "
            f"Market Cap Change Percentage 24h: {item['market_cap_change_percentage_24h']:.2f}%, "
            f"Price Change Percentage 1h in USD: {item['price_change_percentage_1h_in_currency']:.2f}%, "
            f"Price Change Percentage 24h in USD: {item['price_change_percentage_24h_in_currency']:.2f}%, "
            f"Price Change Percentage 7d in USD: {item['price_change_percentage_7d_in_currency']:.2f}%"
            f"Price Change Percentage 30d in USD: {item['price_change_percentage_30d_in_currency']:.2f}%, "
            f"Price Change Percentage 1y in USD: {item['price_change_percentage_1y_in_currency']:.2f}%, "
        )
        formatted_data.append(formatted_item)

    return "\n\n".join(formatted_data)

def gen_coingecko_feed_output(ticker: str):
    coin_id = get_coin_id(ticker.lower())
    market_data = get_market_data(coin_id)
    fmt_market = format_market_data(market_data)
    analyst_sys = """
    you are a Crypto market analyst that summarizes data from Coinmarketcap
    Your goal is to analyze data in a way that retains the original information as much as possible.

    You will: 
    - always clarify and sum up price, marketcap and volume of a given coin
    - highlight the most important aspect of the data, such as the biggest changes.
    - make sure to retain all the numerical and quantitative source of the data ja, never alter the data that is given
    - output data in a form of a market feed that is concise, at most a few paragraphs in length, and convey the core message
    - provide first the headline in one sentence, and then the rest of the body text in the next line

    you will now be given market data of a specific coin in the next message,
    """
    feed_output_message = Message("system", fmt_market)
    initial_memory = Memory(messages=[Message("system", analyst_sys), feed_output_message], state={})
    initial_chain = add_message()(initial_memory)
    coingecko_chain = initial_chain | oai_chat_complete()

    if coingecko_chain.error:
        raise ValueError(f"error executing:, {coingecko_chain.error}, trace: {coingecko_chain.stacktrace}")
    
    return coingecko_chain.memory.messages[-1].content
    