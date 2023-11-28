import os
from serpapi import GoogleSearch

from molang.models import *
from molang.helper import *
from molang.core import *

def cms_load_endpoint():
    return os.getenv("cms_endpoint")

base_cms = cms_load_endpoint()
import os
import requests

def post_article(headline, body):
    if not base_cms:
        raise ValueError("CMS API base URL not found in environment variables")

    url = f"{base_cms}/v1/cms"  # Appending the path to the base URL
    data = {
        "article": {
            "headline": headline,
            "body": body
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    print(data)
    response = requests.post(url, json=data, headers=headers)
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
    except RequestException as e:
        # Handle any requests-related issues (e.g., network errors, timeouts)
        return f"An error occurred: {e}"
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (non-200 responses)
        return f"HTTP error: {e}, Response content: {response.content}"

    return response.json()

def generate_cms_post(requirement_node):
    # pass the output into llm to generate a headline
    analyst_sys = """
    you are a headline synthesizer, you are given a body of text.
    generate a nice, concise, readable headline that conveys the main message and highlight of the text.
    headline will be use in a short-form blog-style content, sort of like a heading of the main message
    keep the lengths within a sentence or two. Only output a headline
    You will be given a body of text in the next message
    DO NOT:
    - make comments about the headline
    - write 'headline' within the message
    """
    cms_msg = Message("system", analyst_sys)
    input_msg = Message("user", requirement_node.get('content'))
    initial_memory = Memory(messages=[cms_msg, input_msg])
    initial_chain = add_message()(initial_memory)
    cms_chain = initial_chain | oai_chat_complete()
    if cms_chain.error:
        raise ValueError(f"error executing:, {cms_chain.error}, trace: {cms_chain.stacktrace}")
    
    headline = cms_chain.memory.messages[-1].content
    print(headline)
    post_article(headline, requirement_node.get('content'))
    print(response)
    return requirement_node.get('id')