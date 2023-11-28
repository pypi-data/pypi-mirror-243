import pickle
from termcolor import colored
import inspect
from enum import Enum
from typing import List, Any
from pydantic import BaseModel, Field

from molang.models import *
from molang.helper import *
from molang.core import *

from .user_profile import parse_user_profile
from . import notebook_io

load_api_key()

FUNCTION_TUNED_MODEL=""

class AnalysisType(Enum):
    DESCRIPTIVE = "descriptive_analysis"
    DIAGNOSTIC = "diagnostic_analysis"
    SENTIMENT = "sentiment_analysis"

class SourcesType(Enum):
    METRICS = "metrics"
    NEWS = "news"
    GOVERNANCE = "governance"
    DOCUMENT = "document"

ROLE = "planner"

class Requirement(BaseModel):
    """ an individual, standalone requirement state that captures users intention for each requirement, for illustrative purpose:
      requirements: 
        - analysis_type: "descriptive" # two types
          keywords: ["BTC", "Bitcoin", "Crypto"]
          sources: "metrics"
          analysis_description: "Describe current market conditions for Bitcoin based on its price, looking at price movements, swings and momentum indicator to understand its direction"
        - analysis_type:
          keywords:
          sources:
          analysis_description:
        - ...

      requirement output you give MUST be YAML compatible, do not give any other output aside from YAML structured output that can be consumed. Do not add comments
    """
    analysis_type: AnalysisType = Field(description="types of analysis to the user would like you to research")
    keywords: List[str] = Field(description="some selected keywords that might be relevant topic for analysis, can be tickers like BTC, or full name like Bitcoin, or category descriptors like DeFi, tolerate up to 4 keywords")
    sources: SourcesType = Field(description="there are 4 major types of sources. These are metrics- quantitative and useful for numerical analysis eg. price and charts, 2) news, useful for getting latest events captured by the mainstream, 3) governance, these are info, discussions and voting from within governance proposal and forums before and after it goes into effects, good for capturing qualitative and internal discussions, lastly 4) document, these are static posts, whitepapers, specs, financial/quaterly reports and documentations that are static factual information about asset or project that arent changing quickly")
    analysis_description: str = Field(description="more detailed description of the analysis that the user would like to perform, keep this concise and within 3-4 sentences at most, this will be used within semantic search to find the best match, so add as much intention and meaning as possible")


class RequirementsState(BaseModel):
    satisfied: bool = Field(default=False, description="true IF user is satisfied with current requirements, else this is false")
    requirements: str = Field(default="", description="a list of requirements for the user, in YAML compatible output string. Tolerate up to a maximum of 5 requirement")
    
def output_yaml_instruct():
    def _inner(memory: Memory):
        instruct = f"""
        user is satisfied, now create a compliant YAML format that contains the synthesis of the requirements
        
        below is the class definition for requirements
        {inspect.getsource(Requirement)}

        you must ensure that:
        1. only output a compatible YAML as illustrated in the doc string above
        2. do not add comments or additional texts, your next message will be outside of the main conversation, it will be parsed by a parser
        3. that you start with requirements key, followed by necessary list of requirement as shown

        your turn now, output the YAML string in the next message:
        """
        return add_message(Message("system", instruct))(memory)
    return _inner

def set_state_from_last_msg(key: str):
    def _inner(memory: Memory):
        if memory.state is not None:
            setattr(memory.state, key, memory.messages[-1].content)
        return PromptChain(memory)
    return _inner

def satisfy_msg(): 
    """ check if last message is :confirm"""
    def _inner(memory: Memory) -> bool:
        last_msg = (memory.messages[-1])
        if last_msg.content == ":confirm":
            return True
        else:
            return False
    return _inner
    
def welcome_user_msg():
    """ welcome user to the chat, wont get put into messaging stream to save tokens"""
    welcome_txt = """
    You are in a chat with our Composer Requirement Planner Agent, to start with, provide a detail of the analysis you would like to perform.
    Our agent will begin to help you break down your requirements into tasks, then once you are satisfied with the requirement tasks, 
    Simply type out-
    :confirm
    in the chat, our Agent will save this requirement for you
    """
    notebook_io.add_message_to_chat(welcome_txt, ROLE,"bot")
    
def run_planner(profile: str = ""):
    planner_sys = f"""
    you are a crypto market analysis requirements planner. Your objective is to 
    1. have a conversation with the investor/user to understand what they want to accomplish, make sure you get to ask questions to user and know more about what user want to accomplish before proceeding to suggestions
    2. confirm with the user what are all the different analyses tasks they would like to perform. Each analysis requirement description is expressed in the python class
    2.1 there might be more than one analysis to be accomplished if the user requirement is large. You need to break down users objective into multiple requirements
    3. After the analyses drafts are confirmed, you will explicitly ask the user if they are happy with what you have planned up AND if it solves a problem for user
    4. Last step is important, make sure the user has verbally express content and intent to proceed in the message

    you are given the following requirement specification that must be filled in. 
    {inspect.getsource(AnalysisType)}
    {inspect.getsource(SourcesType)}
    {inspect.getsource(Requirement)}

    ### About the User
    {parse_user_profile(profile).format_profile() if profile else "no profile"}

    ### Guideline:
    
    Remember that your conversation with user is in 
    natural language, and should be formatted as such. Just know that these requirements must be expressed as YAML with a given format as the last stage
    once the user is content with your plan and no further changes need to be made
    Give upfront suggestions to users, they might not know how to accomplish their tasks, what type of analysis or sources are available
    
    Do NOT explicitly ask user for keywords, analysis type, sources or analysis description- you should be talking to user deeply, then constructing these arguments yourself at the end

    You can and should take multiple requirements, up to 5 specifically, with lots of variations in between- as long as it can finally answer the users objective. Be suggestive in providing additional requirements and creative
    remember that requirements are standalone unit of work. You cannot have requirement x that is dependent on combination of other requirements
    explicitly, ask the user to type out that they are happy with the plan or for you to proceed before we can move on
    
    you can ask the user if they are satisfied by asking them to send a message that is a stop phrase ':confirm', make sure to mention the keyword

    """
    first_msg = Message("system", planner_sys)
    greeter = Message("system", "if user hasn't said anything yet, start with greeting them")
    initial_memory = Memory(messages=[first_msg, greeter], state=RequirementsState())
    initial_chain = add_message(None)(initial_memory)
    convo_stream = stream(
        oai_chat_complete(model="gpt-4"),
        notebook_io.add_last_message_chat("bot", ROLE),
        add_user_input(),
        notebook_io.add_last_message_chat("user", ROLE),
        condition(
            func=satisfy_msg(),
            _do=set_state("satisfied", True),
            _else=nothing(),
        )
    )
    notebook_io.create_planner_chat_interface(initial_memory)
    initial_conversation = do_while(stream=convo_stream, exit_on=assert_state("satisfied", True))
    welcome_user_msg()

    convo = (
        initial_chain 
        | add_user_input() 
        | notebook_io.add_last_message_chat("user", ROLE)
        | initial_conversation 
        | output_yaml_instruct()
        | oai_chat_complete(model="gpt-4")
        | set_state_from_last_msg("requirements")
    )

    if convo.error:
        raise ValueError(f"error executing planner, {convo.error}, trace: {convo.stacktrace}, \n memory messages: {convo.memory.messages}")
    else:
        notebook_io.add_message_to_log(f" ✅ created requirements plan: \n {getattr(convo.memory.state, 'requirements', '')}", ROLE)
        return getattr(convo.memory.state, 'requirements', '')

if __name__ == "__main__":
    run_planner()