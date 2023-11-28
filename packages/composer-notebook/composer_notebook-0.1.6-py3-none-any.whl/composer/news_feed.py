import os
from serpapi import GoogleSearch

from molang.models import *
from molang.helper import *
from molang.core import *

def serp_load_api_key():
    return os.getenv("serp_key")

serp_api_key = serp_load_api_key()

def do_search_news(search_term: str):

    params = {
      "engine": "google",
      "q": search_term,
      "google_domain": "google.com",
      "tbs": "as_qdr=d30",
      "tbm": "nws",
      "num": "20",
      "hl": "en",
      "gl": "us",
      "location": "United States",
      "api_key": serp_load_api_key() or serp_api_key,
    }
    search = GoogleSearch(params)
    return search.get_dict()["news_results"]

def format_news_results(search_term, news_results):
    formatted_text = "News results about {}\n".format(search_term)
    for result in news_results:
        formatted_text += "{}. {} from {} [{}]\n".format(
            result["position"],
            result["title"],
            result["source"],
            result["date"],
            result["snippet"]
        )
    return formatted_text

def gen_news_feed_output(search_term: str):
    results = do_search_news(search_term)
    fmt_results = format_news_results(search_term, results)
    analyst_sys = """
    you are a Crypto market analyst that summarizes data from Google Search about a certain topic
    Your goal is to summarize data in a way that retains the original information as much as possible.

    You will: 
    - highlight and surface the most important news
    - ignore news that you deemed are noises or from an unverified and non-reputable sources
    - craft a coherent narrative around all the different news snippets
    - do your best to mention where the sources are from and how many days ago.
    - package your output message in short paragraphs style, starting with a headline and body of paragrahs

    you will now be given search data of a specific search term in the next message,
    """
    feed_output_message = Message("system", fmt_results)
    initial_memory = Memory(messages=[Message("system", analyst_sys), feed_output_message], state={})
    initial_chain = add_message()(initial_memory)
    serp_chain = initial_chain | oai_chat_complete()

    if serp_chain.error:
        raise ValueError(f"error executing:, {serp_chain.error}, trace: {serp_chain.stacktrace}")
    
    return serp_chain.memory.messages[-1].content
    
  