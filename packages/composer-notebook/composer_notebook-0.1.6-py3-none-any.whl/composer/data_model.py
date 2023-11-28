# goal: generate new dataset for finetuning
from pydantic import BaseModel, Field
import json
import inspect
from molang.models import *
from molang.helper import *
from molang.core import *

load_api_key()

# declare sub class variations table, for each class key, we will have 10 unique variation seed
variations_table = {
    "Dune": [
      "Unique and detailed analysis related Decentralized Exchange metrics",
      "analysis of NFT and NFT market related metrics and questions",
      "Unique and detailed analysis of top lending pools, money market funds- borrowing and lending analytics",
      "analysis related to all the available metrics of stable coins, collateralization, market cap, etc.",
      "Unique and detailed analysis of metrics related to staking, liquid staking derivatives, LST (liquid staking tokens)"
    ],
    "Coingecko": [
      "analysis over price trends over time for an individual cryptocurrency, explicitly pick a token ie. BTC, be creative with ticker",
      "analysis over market cap trends over time for an individual cryptocurrency, explicitly pick a token ie. BTC, be creative with ticker",
      "analysis over volume trends over time for an individual cryptocurrency, explicitly pick a token ie. BTC, be creative with ticker",
      "analyze and contrast the historical price metrics of a number of cryptocurrencies, explicitly pick tokens, ie. BTC, be creative with tickers, ie. BTC, be creative with tickers"
      "analyze and contrast the historical volume, and marketcap metrics of a number of different cryptocurrencies, explicitly pick tokens, ie. BTC, be creative with tickers, ie. BTC, be creative with tickers"
    ],
    "RCrypto": [
        "Speculative threads predicting the next meme coin tokens that will go 10x, 100x or 1000x",
        "Discussions overflowing with FUD on a token or crypto trends, be explicit on said token or trend",
        "Bullish megathreads backing the potential of new tokens, for eg. SOL, or LINK",
        "Rumor-mill, and conspiracy theories on possible partnerships that could send some tokens 'to the moon', or crash to zero",
        "Degen trading strategies and the latest 'pump and dump' alerts"
    ],
    "CryptoNewsSites": [
        "Feature articles on the impact of recent news on the price of tokens like BTC and ETH",
        "Analysis of how global events are influencing the market caps of stablecoins, or other assets",
        "Reporting on the trading volumes of up-and-coming tokens post-regulatory announcements",
        "Summaries of market trends for major cryptocurrencies during significant economic shifts, explicitly name the token",
        "Reports on emerging blockchain projects with potential token baskets for investment"
    ],
    "Forums": [
        "User experiences and performance comparisons for tokens within a specific blockchain like BSC",
        "Technical Improvement proposals that goes into new features, functionality, or supply issuances, explicitly pick a project",
        "General discussions around the health and performance of the overall crypto market",
        "Predictive analytics based on forum trends for tokens experiencing high volatility",
        "Comparisons of technical advancements and their potential impact on token prices"
    ],
    "Snapshot": [
        "Voting patterns and outcomes for DeFi protocols like Synthetix, specifically focusing on SNX governance",
        "Analysis of governance proposals affecting tokens like AAVE, that has serious implications on its budgets and spending",
        "Study of community engagement, voting activities in governance for tokens that relies on govt, ie. like Uniswap",
        "Insight into DAO structures and their effectiveness in driving token value via proposals like Curve CRV liquidity incentives",
        "Analysis of proposals that propose to integrate new DeFi yield protocol or diversify existing treasury into other assets"
    ],
    "Documentation": [
        "API documentation for integration",
        "How does a certain blockchain or protocol works or functions",
        "Crypto Infrastructure breakdowns for some leading cryptocurrencies project",
        "Details behind how certain some key functionalities of a blockchain smart contract platform works",
        "what are the relevant smart contracts, links, application and quick start guides for a certain technology"
    ],
    "Reports": [
        "Quarterly financial analysis of top-performing tokens and their market movements, be explicit and name the tokens",
        "In-depth annual blockchain tech reviews focusing on key tokens within the industry",
        "Crypto exchange security audit summaries for assets like BNB and FTT",
        "Investor-focused analysis on the market potential of tokens in sectors like DeFi or GameFi",
        "Sector-wide reports on subsector market trends such as NFT, spotlighting leading tokens and developments"
    ]
}

class SyntheticDataset(BaseModel):
    counts: int = Field(default=0, description="how many synthetic data sets has been generated (based on msg count)")
    messages: List[str] = Field(default=[], description="requirements string in a form of message lists")


# declare namespaces, and classes in python
class Metrics(BaseModel):
    """
    abstract class, with metrics namespace. ie. 
    <metrics.sub_class.method>(arg1, arg2)

    metrics are:
    1. quantitative in general, useful for numerical and statistical analysis or question
    2. utilized in descriptive analysis
    3. highly temporal: time, date and date range significantly matters
    """
    pass

class Dune(Metrics):
    """
    metrics subclass, from metrics namespace. ie.
    <metrics.dune.method>(arg1, arg2)

    dune analytics is a platform where multiple quantitative analyses done by professional analysts are posted
    1. they contain useful feeds for DeFi analysis: from lending market, dexs, staking provider, smart contract stats, active wallets, nfts
    2. they contain useful feeds long-tail of analyses on protocols and, predominantly smart contract chains, both new and old
    3. they are generally not useful for analyses involving CEXs flows, barebone price movements, traditional price charts and technical analyses

    requirement for Dune should be extremely specific
    """
    def get(filter_keywords: List[str], match_description: str):
        """
        get an analyses currently supported on Dune, accepts the following arguments

        usage:
        <metrics.dune.get>(["ETH", "Ethereum", "Staking"], "analyses of the top eth staking providers, including protocols and staking pools, over the past 6 months timeframe")
        arguments:
          filter_keywords: the keyword list to filter the feeds for
          match_description: natural language description that you want to find the best match for
        """
        pass

class Coingecko(Metrics):
    """
    metrics subclass, from metrics namespace. ie.
    <metrics.coingecko.method>(arg1, arg2)

    CoinGecko specializes in tracking cryptocurrency prices, volumes, and market capitalizations.
    1. It is particularly useful for market data and trends for a wide array of cryptocurrencies.
    2. It provides detailed charts and historical data for price and market metrics.
    3. It is not suited for non-market related cryptocurrency data such as in-depth, niche focused blockchain analytics.

    The Coingecko class is designed for market data inquiries and cryptocurrency comparisons.
    """
    def get(coin_symbol: str, comparison_metrics: List[str]):
        """
        Retrieve specific market data for a given cryptocurrency from CoinGecko.

        usage:
        <metrics.coingecko.get>("btc", ["price", "volume", "market_cap"])
        arguments:
          coin_symbol: the symbol or ticket of the cryptocurrency in lower case, DO NOT use full coin name, use a ticker only, ie. BTC, ETH, USDT
          comparison_metrics: the list of metrics to retrieve data for (e.g., "price", "volume", "market_cap")
        """
        pass
    
    def compare(coins: List[str], comparison_metrics: List[str]):
        """
        Compare a selection of cryptocurrencies on specified metrics from CoinGecko.

        usage:
        <metrics.coingecko.compare>(["BTC", "ETH", "LTC"], ["price", "volume", "market_cap"])
        arguments:
          coins: the list of cryptocurrency symbols or names to compare (up to 5)
          comparison_metrics: the list of metrics for comparison (e.g., "price", "volume", "market_cap")
        """
        pass

class News(BaseModel):
    """
    "news" source type
    
    abstract class, with a news namespace. ie. 
    <news.sub_class.search>(arg1, arg2, arg3, arg4)    
    News are:
    1. qualitative in nature, useful for sentiment analysis and market mood
    2. utilized in sentiment analysis
    3. temporal, with time factors like latest, past week, or past month being significant
    4. could be useful to understand why something happens, ie. in case price is event driven
    """
    pass

class RCrypto(News):
    """
    news subclass, from news namespace. ie.
    <news.r_crypto.search>(arg1, arg2, arg3, arg4)

    r/crypto is a subreddit dedicated to cryptocurrency discussions
    1. It contains user-generated content, discussions, and opinions on various aspects of cryptocurrencies.
    2. It's a valuable source for gauging community sentiment and reactions to market events or technological developments.
    3. It's not an authoritative source for factual reporting, therefore can be unreliable for facts, but can reflect the mood and trends within the crypto community.

    Search queries for r/crypto should be tailored to extract community sentiment and discussion trends.
    """
    def search(best_match: str, time: str, keywords: List[str], sentiment: str):
        """
        Search for news on r/crypto, accepts the following arguments

        usage example:
        <news.r_crypto.search>("top staking discussion", "7 days", ["ETH", "Staking"], "bullish")
        arguments:
          best_match: natural language description for best matching threads
          time: time frame for the search ('latest', '7 days', '30 days')
          keywords: list of keywords to focus the search on
          sentiment: desired sentiment of the content ('bullish', 'bearish', 'neutral', 'all')
        """
        pass

class CryptoNewsSites(News):
    """
    news subclass, from news namespace. ie.
    <news.crypto_news_sites.search>(arg1, arg2, arg3, arg4)

    crypto-news-sites aggregate news from various sources related to cryptocurrencies
    1. They offer formal reporting and articles from across the crypto industry.
    2. They can be used to obtain a more global and formal perspective on market events, regulatory news, and technological advancements.
    3. They are generally factual and less about community sentiment compared to user-generated content 

    The search function for crypto-news-sites should focus on extracting formal reporting and factual news content.
    """
    def search(best_match: str, time: str, keywords: List[str], sentiment: str):
        """
        Search for news on crypto-news-sites, accepts the following arguments

        usage example:
        <news.crypto_news_sites.search>("latest regulatory changes", "30 days", ["regulation"], "all")
        arguments:
          best_match: natural language description for best matching articles
          time: time frame for the search ('latest', '7 days', '30 days')
          keywords: list of keywords to focus the search on
          sentiment: desired sentiment of the content ('bullish', 'bearish', 'neutral', 'all')
        """
        pass

class CryptoGovernance(BaseModel):
    """
    "governance" source type
    abstract class, with a crypto governance namespace. ie.
    <governance.sub_class.method>(arg1, arg2, arg3)

    Governance discussions and decisions are:
    1. Foundational to understanding the direction and development of blockchain protocols.
    2. Important for gauging the sentiment and involvement of stakeholders.
    3. Time-sensitive as they often relate to specific proposals and voting periods.
    """
    pass

class Forums(CryptoGovernance):
    """
    governance subclass, from governance namespace, for forums. ie.
    <governance.forums.method>(arg1, arg2, arg3)

    Forums such as Discourse or improvement proposals discussion forums like BIPs, EIPs:
    1. Serve as platforms for deliberation and detailed discussions on protocol changes and improvements.
    2. Act as a barometer for community engagement and sentiment on governance issues.
    3. Provide a historical archive of governance discussions and their evolution over time.

    Forums require targeted searches for extracting specific governance discourse.
    """
    def search(best_match: str, time: str, keywords: Optional[List[str]] = None):
        """
        Search governance-related discussions in forums, accepts the following arguments

        usage:
        <governance.forums.search>("EIP-1559 discussion", "30 days", ["EIP-1559", "transaction fee", "burn"])
        arguments:
          best_match: natural language description for best matching discussions
          time: time frame for the search ('latest', '7 days', '30 days')
          keywords: (optional) list of keywords to focus the search on
        """
        pass

class Snapshot(CryptoGovernance):
    """
    governance subclass, from governance namespace, for Snapshot. ie.
    <governance.snapshot.method>(arg1, arg2, arg3)

    Snapshot is a voting platform used by many decentralized organizations:
    1. Provides insight into active governance proposals and voting outcomes.
    2. Reflects the stance and voting behavior of token holders and delegates.
    3. Can be indicative of the future direction and priorities of the protocol.

    Snapshot searches should be focused on retrieving voting results and proposal discussions.
    """
    def search(best_match: str, time: str, keywords: Optional[List[str]] = None):
        """
        Search for voting proposals and outcomes on Snapshot, accepts the following arguments

        usage:
        <governance.snapshot.search>("DeFi protocol upgrade vote", "latest", ["governance", "DeFi", "upgrade"])
        arguments:
          best_match: natural language description for best matching votes
          time: time frame for the search ('latest', '7 days', '30 days')
          keywords: (optional) list of keywords to focus the search on
        """
        pass

class Documents(BaseModel):
    """
    "documents" source type
    abstract class, with a documents namespace. ie.
    <documents.sub_class.method>(arg1, arg2)

    Documents provide:
    1. In-depth information and are vital for research and understanding complex topics.
    2. A static source of knowledge, contrasting with the dynamic and temporal nature of other sources
    """
    pass

class Documentation(Documents):
    """
    documents subclass, from documents namespace, for documentation. ie.
    <documents.documentation.method>(arg1, arg2)

    Documentation, such as official manuals, guides, and API references:
    1. Offers comprehensive details on projects, platforms, and protocols.
    2. Is essential for developers, researchers, and anyone seeking technical understanding or how-to knowledge.

    Searches within documentation should be precise to find the most relevant and specific information.
    """
    def search(keywords: List[str], best_match: str):
        """
        Search within documentation, accepts the following arguments

        usage:
        <documents.documentation.search>(["smart contract", "optimization"], "best practices for gas saving")
        arguments:
          keywords: list of keywords to focus the search on
          best_match: natural language description for best matching documents
        """
        pass

class Reports(Documents):
    """
    documents subclass, from documents namespace, for reports. ie.
    <documents.reports.method>(arg1, arg2)

    Reports, including industry analyses, quarterly updates, and research papers:
    1. Provide structured and detailed insights into various aspects of the crypto space.
    2. Are invaluable for investors, analysts, and stakeholders looking for data-driven decision-making.

    The search for reports demands a focus on relevancy and the extraction of comprehensive analyses.
    """
    def search(keywords: List[str], best_match: str):
        """
        Search within reports, accepts the following arguments

        usage:
        <documents.reports.search>(["market trends", "Q4"], "crypto market analysis Q4")
        arguments:
          keywords: list of keywords to focus the search on
          best_match: natural language description for best matching reports
        """
        pass


class AnalysisType(Enum):
    DESCRIPTIVE = "descriptive_analysis"
    DIAGNOSTIC = "diagnostic_analysis"

class SourcesType(Enum):
    METRICS = "metrics"
    NEWS = "news"
    GOVERNANCE = "governance"
    DOCUMENT = "document"

class Requirement(BaseModel):
    """ an individual, standalone requirement state that captures users intention for each requirement, for illustrative purpose:
      requirements: 
        - analysis_type: "descriptive" # two types
          keywords: ["BTC", "Bitcoin", "Crypto"]
          sources: "metrics"
          analysis_description: "Describe current market conditions for Bitcoin based on its price, looking at price movements, swings and momentum indicator to understand its direction"

      requirement output you give MUST be YAML compatible, do not give any other output aside from YAML structured output that can be consumed. Do not add comments
    """
    analysis_type: AnalysisType = Field(description="types of analysis to the user would like you to research")
    keywords: List[str] = Field(description="some selected keywords that might be relevant topic for analysis, can be tickers like BTC, or full name like Bitcoin, or category descriptors like DeFi, tolerate up to 4 keywords")
    sources: SourcesType = Field(description="there are 4 major types of sources. These are metrics- quantitative and useful for numerical analysis eg. price and charts, 2) news, useful for getting latest events captured by the mainstream, 3) governance, these are info, discussions and voting from within governance proposal and forums before and after it goes into effects, good for capturing qualitative and internal discussions, lastly 4) document, these are static posts, whitepapers, specs, reports and documentations that are static factual information about asset or project that arennt changing quickly")
    analysis_description: str = Field(description="more detailed description of the analysis that the user would like to perform, keep this concise and within 3-4 sentences at most, this will be used within semantic search to find the best match, so add as much intention and meaning as possible")

# declare prompt instruction and how to use each class
def gen_prompt_template(namespace: str, subclass: str, variation_seed, namespace_cls, subclass_cls):
    return f"""
        you are a synthetic data-set GPT. Your task is to generate synthetic datasets
        You are given a namespace: {namespace}, and its subclass: {subclass}.
        You will create a made-up requirements set, whereby a given namespace and its subclass will be most useful and appropriate for.

        ### the response format will be the following yaml:
        {inspect.getsource(Requirement)}

        ### an example for illustration purpose:
        given a namespace: abc and its detail, and its subclass xyz and its detail
        your response:
        requirements:
          - analysis_type: "x"
            keywords: ["x", "xx", "xxxxx"]
            sources: "abc"
            analysis_description: "some description about the analyses that abc.xyz subclass will optimally be useful for"

        ### guidance:
        - DO NOT output an answer any other than the expected response format
        - DO NOT add additional comment outside of the response format
        - DO NOT give more than a single requirement in a message
        - Each message should be different and have variations
        - DO NOT create more than one requirements YAML at a time. Each requirement should have only ONE analysis, keyword, sources and analyses description. Each message should only contain a single YAML requirement with one node
        - Keep each requirement concise and target a very specific type of analysis in mind, more detail the better
        ### The Namespace Source
        the following is the namespace and subclass
        {inspect.getsource(namespace_cls)}
        {inspect.getsource(subclass_cls)}

        make sure the requirements are centered around {variation_seed}
        Next, its your turn to generate appropriate requirement messages
    """

# create a shared prompt template to be used by all prompts and synthetic data

def append_json_to_file(data, filename="composer-dataset.jsonl"):
    with open(filename, 'a') as f:
        json_line = json.dumps(data) + "\n"  # Convert dict to JSON string and add newline
        f.write(json_line)

def read_jsonl_to_list(file_path):
    json_objects = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):  # Enumerate for line tracking
            try:
                json_object = json.loads(line)
                json_objects.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e} - {line}")
    return json_objects

def incr_count():
    def _inner(memory: Memory):
        if memory.state is not None:
            if hasattr(memory.state, 'counts'):
                setattr(memory.state, "counts", memory.state.counts + 1)
            else:
                raise AttributeError("counts attribute does not exist in the state object.")
        return PromptChain(memory)
    return _inner

def append_requirement():
    def _inner(memory: Memory):
        if memory.state is not None and hasattr(memory.state, 'messages'):
            if memory.messages and hasattr(memory.messages[-1], 'content'):
                memory.state.messages.append(memory.messages[-1].content)
                print('adding requirement')
            else:
                raise AttributeError("No messages to append or last message has no content.")
        return PromptChain(memory)
    return _inner

def generate_synt_requirements():
    _namespace_name = "CryptoGovernance"
    _namespace = CryptoGovernance
    _subcls_name = "Snapshot"
    _subcls = Snapshot
    iteration_per_seed = 10
    variation_seeds = variations_table[_subcls_name]
    for v in variation_seeds:
        templ = gen_prompt_template(_namespace_name, _subcls_name, v, _namespace, _subcls)
        first_msg = Message("system", templ)
        initial_memory = Memory(messages=[first_msg], state=SyntheticDataset())
        initial_chain = add_message(None)(initial_memory)
        # run generation molangchain, exit on nth iteration
        synth_stream = stream(
            oai_chat_complete(model="gpt-3.5-turbo-16k"),
            log_last_message(),
            append_requirement(),
            incr_count(),
        )

        synth_loop = do_while(stream=synth_stream, exit_on=assert_state("counts", iteration_per_seed))
        synthetic_gpt = initial_chain | synth_loop
        if synthetic_gpt.error:
            print('error messages:')
            print(synthetic_gpt.error)
            print(synthetic_gpt.stacktrace)
        print(f"final requirements: \n {getattr(synthetic_gpt.memory.state, 'messages', [''])}")
        for m in synthetic_gpt.memory.state.messages:
          variation_synths_data = {'namespace': _namespace_name, 'subclass': _subcls_name, 'requirement': m, 'variation_seed': v}
          append_json_to_file(variation_synths_data)

def gen_method_prompt_templ(requirement, namespace, subclass):
    return f"""
    You are a helpful dataset generation bot. You will help me generate a dataset. 

    ## You will be given:
    1. a set of requirements
    2. a class and namespace definitions that you will try to convert the requirements into a function call.
    3. the function and method call will follow a proprietary DSL format. the certain structure can be seen here: `<namespace.sub_class.method>(arg1, arg2, arg...)`

    You will write, in a single message after this, the function call and its argument in plain text

    ## For instance:

    Input:
    Requirements:
      - ... some semantic definition
    class SomeNamespace(BaseModel):
    ...

    class SomeSubclass(SomeNamespace)
        def some_method(arg1)

    Output:
    <some_name.space.some_subclass.some_method>(derived_output_from_requirement)

    Guidelines:
    - Do not make any additional comments or writings other than the method call input
    - follow the code and inline comment for the class and do your best to convert that instruction into the method call
    - Attempt to retain the most semantic meaning from what is given as requirement inputs and convert them into function arguments

    Input:
    requirement:
    {requirement}

    namespace:
    {namespace}
    subclass:
    {subclass}
    Output:
    """

def generate_methods(to_file="composer-dataset-methods.jsonl"):
    dataset_obj = read_jsonl_to_list("composer-dataset.jsonl")
    for data in dataset_obj:
        # resolve class from cls string name
        namespace_name = data["namespace"]
        class_name = data["subclass"]
        resolved_namespace = globals().get(namespace_name)
        resolved_class = globals().get(class_name)

        if not resolved_class or not resolved_namespace:
            print(f"Class {class_name} or {namespace_name} Namespace not found. skipping")
            continue

        # build prompt template
        templ = gen_method_prompt_templ(data["requirement"], inspect.getsource(resolved_namespace), inspect.getsource(resolved_class))
        first_msg = Message("system", templ)
        initial_memory = Memory(messages=[first_msg], state={})
        initial_chain = add_message(None)(initial_memory)
        chat_with_method = initial_chain | oai_chat_complete() | log_last_message()
        method = chat_with_method.memory.messages[-1]
        data["function"] = method
        append_json_to_file(data, "composer-dataset-methods.jsonl")
  

def convert_to_message_structure(json_data):
    # Construct the messages
    messages = [
        {
            "role": "system",
            "content": "You are a custom function dispatcher."
        },
        {
            "role": "system",
            "content": "Your input is {}".format(json_data['requirement'].replace("\n", " "))
        },
        {
            "role": "assistant",
            "content": json_data["function"][1]
        }
    ]
    
    # Return the new structure
    return {"messages": messages}

def convert_messages_for_finetuning():
    data_obj = read_jsonl_to_list("composer-dataset-methods.jsonl")
    for data in data_obj:
        msg = convert_to_message_structure(data)
        append_json_to_file(msg, "composer-finetune.jsonl")

# if __name__ == "__main__":
#     convert_messages_for_finetuning()