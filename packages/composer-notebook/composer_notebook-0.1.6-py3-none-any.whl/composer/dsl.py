from pydantic import BaseModel, Field
import json
import inspect
import re
from typing import Dict, List, Tuple, Type
from molang.models import *
from molang.helper import *
from molang.core import *
from .data_model import *
from .coingecko_feed import *
from .news_feed import *

load_api_key()

# resolve to the right class and method
# checker if the correct class or method actually exists- throw error if doesnt
# parse the function caller
namespace_to_class_map: Dict[str, Type] = {
    'dune': Dune,
    'coingecko': Coingecko,
    'r_crypto': RCrypto,
    'crypto_news_sites': CryptoNewsSites,
    'forums': Forums,
    'snapshot': Snapshot,
    'documentation': Documentation,
    'reports': Reports
}

# Mapping of namespace classes to their subclasses
namespace_to_subclasses_map: Dict[str, List[str]] = {
    'metrics': ['dune', 'coingecko'],
    'news': ['r_crypto', 'crypto_news_sites'],
    'governance': ['snapshot', 'forums'],
    'documents': ['documentation', 'reports']
}

# mockup example of each return result for corresponding function

# prompt template: taking class, function definition, context.. -> running the function, creating mockup
# Adjust the parsing function to handle both lists and single string arguments
def parse_and_resolve(dsl_function: str) -> Tuple[Type, str, List]:
    # Use a regex to parse the DSL string into namespace, class, method, and argument groups
    match = re.match(r"<(\w+)\.(\w+)\.(\w+)>\((.*)\)", dsl_function)
    if match:
        namespace, class_name, method_name, args_str = match.groups()

        # Improved function to parse arguments
        def parse_arg(arg):
            arg = arg.strip()
            if arg.startswith('[') and arg.endswith(']'):
                # Handling list arguments
                return [item.strip().strip('"') for item in re.findall(r'\"(.*?)\"', arg)]
            return arg.strip('"')

        # Improved splitting logic using regular expressions
        args = re.findall(r'\[.*?\]|\".*?\"', args_str)
        arguments = [parse_arg(arg) for arg in args]

        # Check if the subclass belongs to the correct namespace
        if class_name.lower() not in namespace_to_subclasses_map.get(namespace.lower(), []):
            raise ValueError(f"Subclass {class_name} does not belong to namespace {namespace}")

        # Resolve namespace/class to the actual Python class
        class_definition = namespace_to_class_map.get(class_name.lower())
        if not class_definition:
            raise ValueError(f"Unknown class: {class_name}")

        # Ensure the method exists
        if not hasattr(class_definition, method_name):
            raise ValueError(f"Unknown method: {method_name} for class {class_name}")

        return class_definition, method_name, arguments
    else:
        raise ValueError(f"Invalid DSL function syntax. for {dsl_function}")

def test_parser_and_resolver():
    test_cases = [
        # Valid case
        ('<metrics.coingecko.compare>(["SNX", "AAVE"], ["market_cap", "price"])', True),
        # Error: Unknown class
        ('<metrics.unknown.compare>(["SNX", "AAVE"], ["market_cap", "price"])', False),
        # Error: Unknown method
        ('<metrics.coingecko.unknown>(["SNX", "AAVE"], ["market_cap", "price"])', False),
        # Error: Invalid syntax
        ('metrics.coingecko.compare(["SNX", "AAVE"], ["market_cap", "price"])', False),
        # Error: Subclass not belonging to namespace
        ('<metrics.dune.compare>(["SNX", "AAVE"], ["market_cap", "price"])', False),
        # Test case with a mix of list and single string arguments
        ('<metrics.coingecko.compare>(["BTC", "ETH"], "volume", ["1d", "7d", "30d"])', True),
        # Test case with a single string argument
        ('<metrics.coingecko.compare>("BTC", "volume", "1d")', True),
    ]

    for dsl, should_pass in test_cases:
        try:
            resolved_class, method, args = parse_and_resolve(dsl)
            if should_pass:
                print(f"Test passed for DSL: {dsl}")
            else:
                print(f"Test failed (unexpected pass) for DSL: {dsl}")
        except ValueError as e:
            if not should_pass:
                print(f"Test passed (expected failure) for DSL: {dsl} - Error: {e}")
            else:
                print(f"Test failed (unexpected error) for DSL: {dsl} - Error: {e}")

def oz_prompt_template(cls_def, args, method, ctx):
    return f"""
    You are a wizard of oz- mocked function result generator. You will take the following information:
    - class and function definitions and signature
    - the arguments to be fed into that function
    - some additional facts, ground truths, context of the world model you must take into consideration

    you will synthesize this information, and output a mocked example result- of the function being called

    ### IMPORTANT note about the output:
    - your mockup answer will be in natural language, it can be in a varied amount of length- anywhere between 3-5 sentences, or 1 or 2 paragraphs, but never more than 3 paragraphs
    - It will contain mocked facts, numbers, and either qualitative/quantitative analysis as if performed by a real analysis as an output.
    - DO NOT say that your output is a mock, describe the function, or describe your task on any meta-level. your job is to mock up the result of calling the functional analysis

    Below is the real information:
    Class definition:
    {inspect.getsource(cls_def)}

    Resolved Method: {method}()
    Arguments for resolved method: {args}

    Additional Context: {ctx or 'None'}

    Your output:

    """

# NOTE: functions other than Coingecko.get and News.search API are mocked out
def generate_func_output(dsl: str, ctx = ""):
    (cls_def, method, arg) = parse_and_resolve(dsl)
    prmpt = oz_prompt_template(cls_def, arg, method, ctx)
    if cls_def == Coingecko and method == "get":
        print(f"executing coingecko API with arg:{arg}, type: {type(arg)}")
        try:
            return gen_coingecko_feed_output(arg[0])
        except ValueError as e:
            print(f"error calling {cls_def} with method {method}, error msg: {e} \n generating mocked output")
    if cls_def == CryptoNewsSites and method == "search":
        print(f"executing news search API with arg:{arg}, type: {type(arg)}")
        try:
            return gen_news_feed_output(arg[0])
        except ValueError as e:
            print(f"error calling {cls_def} with method {method}, error msg: {e} \n generating mocked output")
    first_msg = Message("system", prmpt)
    initial_memory = Memory(messages=[first_msg], state={})
    initial_chain = add_message(None)(initial_memory)
    chain = initial_chain | oai_chat_complete(model="gpt-4")
    func_out = chain.memory.messages[-1].content
    return func_out


# if __name__ == "__main__":
#     test_dsl = '<metrics.coingecko.compare>(["SNX", "AAVE"], ["market_cap", "price"])'
#     out = generate_func_output(test_dsl)
#     print(out)
