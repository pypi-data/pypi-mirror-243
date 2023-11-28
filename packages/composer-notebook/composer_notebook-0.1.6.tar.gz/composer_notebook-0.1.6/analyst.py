import yaml
from enum import Enum
from typing import List, Any
from pydantic import BaseModel, Field

from .dsl import *
from .cms_post_feed import *
from molang.models import *
from molang.helper import *
from molang.core import *
from . import notebook_io

load_api_key()

ROLE = "analyst"
FAILED_GENERATE_METHOD = "FAILED_GENERATE_METHOD"
FUNCTION_TUNED_MODEL=""
# generate feeds and chat with the users, parse requirements, and allow user to chat

class DSLFixerState(BaseModel):
    failed_attempts: List[str] = Field(description="all failed attempts at fixing dsl")
    success_dsl: str = Field(default="", description="successful_dsl")

def fix_dsl_prompt(requirement: dict, classes: Dict[str, Type], instruct: str):
    requirements_str = yaml.dump(requirement)
    
    # Iterate through the namespace_to_class_map to generate class details
    class_details = ""
    for namespace, cls in namespace_to_class_map.items():
        # Use inspect.getsource to get the class definition source code
        class_source = inspect.getsource(cls)
        class_details += f"\nNamespace: {namespace}\n{class_source}\n"
    return f""" 
    You are an expert at fixing a custom DSL. You will be given:
    1. original requirement for the end user
    2. all the available classes that the DSL could resolve to, and how you can call one

    Guidance
    - You must return a single line, single method call, your DSL output should look like the following:
      example: <namespace.class.method>(arg1, arg2)
      note that function arguments needs to be surrounded by `()` and separated by `,` 
      note that namespace, class and method needs to be surrounded by `<>`
    - each class definitions contain the usage guidance and argument
    - do not make up your own DSL that is not available, use the correct namespace, class name, method, and type arguments
    - try your best to resolve DSL in such way that the original requirement for user is met
    - IMPORTANT: do not write a comment about the fixes, issues or talk about fixing,
    ONLY PROVIDE THE FIXED DSL IN THE NEXT MESSAGE

    Following are your inputs:
    User requirement:
    {requirements_str}

    All available classes data:
    {class_details}

    Below is additional instruction from user, prioritize this custom instruction above the original requirement above
    {instruct}
    """.strip()

def add_failed_attempts_msgs():
    def _inner(memory: Memory):
        failed_dsls_str = '\n'.join(memory.state.failed_attempts)
        failed_prompt = f"""
        the following are all the failed attempts at building dsl, do not try these:
        {failed_dsls_str}
        """
        return add_message(Message("user", failed_prompt))(memory)
    return _inner

def validate_method_from_last_msg():
    def _inner(memory: Memory):
        last_msg_content = memory.messages[-1].content
        notebook_io.add_message_to_log("validating function sig", ROLE)
        try:
            parse_and_resolve(last_msg_content)
            return True
        except ValueError:
            return False
    return _inner

def set_success_from_last_msg():
    def _inner(memory: Memory):
        setattr(memory.state, "success_dsl", memory.messages[-1].content)
        return PromptChain(memory)
    return _inner

def add_failed_attmpt_from_last_msg():
    def _inner(memory: Memory):
        last_msg_content = memory.messages[-1].content
        memory.state.failed_attempts.append(last_msg_content)
        return PromptChain(memory)
    return _inner

def terminate_dsl_cond(total_attmpts):
    def _inner(memory: Memory) -> bool:
        if memory.state.success_dsl != "":
            return True
        if len(memory.state.failed_attempts) >= total_attmpts:
            return True
        else:
            return False
    return _inner

def attempt_fix_dsl(requirement: dict, failing_dsl: str, instruct: str = "", total_retries=6) -> str:
    prmpt = fix_dsl_prompt(requirement, namespace_to_class_map, instruct)
    dsl_state = DSLFixerState(
        failed_attempts=[failing_dsl],
        success_dsl="",
    )
    initial_memory = Memory(messages=[Message("system", prmpt)], state=dsl_state)
    initial_chain = PromptChain(initial_memory)
    fix_block = stream(
        add_failed_attempts_msgs(),
        oai_chat_complete("gpt-3.5-turbo-16k"),
        notebook_io.add_last_message_log(ROLE),
        condition(
            func=validate_method_from_last_msg(),
            _do=set_success_from_last_msg(),
            _else=add_failed_attmpt_from_last_msg()
        ),
    )
    fix_loop = do_while(stream=fix_block, exit_on=terminate_dsl_cond(total_retries))
    fix_dsl_chain = initial_chain | fix_loop
    if fix_dsl_chain.error:
        notebook_io.add_message_to_log(f"error executing dsl fixes: {fix_dsl_chain.error}, {fix_dsl_chain.stacktrace}, {fix_dsl_chain.memory.messages}", ROLE)

    if fix_dsl_chain.memory.state.success_dsl != "":
        return fix_dsl_chain.memory.state.success_dsl
    else:
        notebook_io.add_message_to_log(fix_dsl_chain.memory.state.failed_attempts, ROLE)
        raise ValueError("DSL Fix Attempt Failed")


    # do while: either success case found, or total tries exhausted
    # return dsl, or raise errors

def generate_method_from_requirement_node(requirement: dict, instruc: str = "") -> str:
    first_msg = Message("system", yaml.dump(requirement))
    second_msg = Message("system", fix_dsl_prompt(yaml.dump(requirement), namespace_to_class_map, instruc))
    initial_memory = Memory(messages=[first_msg, second_msg], state={})
    initial_chain = add_message(None)(initial_memory)
    chain = initial_chain | oai_chat_complete("gpt-4")
    unvalidated_method = chain.memory.messages[-1].content
    try:
        # prettify_log("SYSTEM", "validating function call", "blue")
        notebook_io.add_message_to_log("validating function call", ROLE)
        parse_and_resolve(unvalidated_method)
        return chain.memory.messages[-1].content
    except ValueError as e:
        try:
            notebook_io.add_message_to_log(f"found issue with dsl {unvalidated_method}, automating fix", ROLE)
            fixed_method = attempt_fix_dsl(requirement, unvalidated_method, instruc)
            notebook_io.add_message_to_log(f"fix found:{fixed_method}", ROLE)
            return fixed_method
        except ValueError:
            # If attempt_fix also raises ValueError, raise a new generic ValueError.
            notebook_io.add_last_message_log("fixes not found for generated DSL")
            # FIXME: return error, result as tuple and match that instead of matching string value on error case 
            return FAILED_GENERATE_METHOD

def run_feeds_on_requirements(requirements_yaml: str) -> List[Dict]:
    # Process each requirement dictionary to generate function calls.
    requirements = yaml.safe_load(requirements_yaml)['requirements']

    function_calls = [generate_method_from_requirement_node(req) for req in requirements]
    function_outputs = []

    # Collect the outputs for each function call.
    for i, func in enumerate(function_calls):
        try:
            if func == FAILED_GENERATE_METHOD:
                out = f"Error generating analysis for id: {i+1}, please check logs"
            else:
                out = generate_func_output(func)
            notebook_io.add_message_to_log(f"generated output for {func}", ROLE)
            function_outputs.append({"id": i+1, "method_call": func, "content": out})
        except ValueError as e:
            error_message = f"Error: {e}"
            function_outputs.append({"id": i+1, "method_call": func, "content": error_message})

    return function_outputs

def generate_yaml_output(function_outputs: List[Dict], requirements_yaml: str) -> str:
    # Parse YAML string into Python dictionaries
    requirements = yaml.safe_load(requirements_yaml)['requirements']
    
    # Combine the requirements and their corresponding function outputs into a YAML formatted string.
    yaml_data = {"requirements": []}
    
    for req, output in zip(requirements, function_outputs):
        combined = {**req, **output}  # Merge dictionaries
        yaml_data["requirements"].append(combined)
    
    return yaml.dump(yaml_data, sort_keys=False, default_flow_style=False)



def msg_prefixed_with(prefix): 
    """ check if last message is y"""
    def _inner(memory: Memory) -> bool:
        last_msg = (memory.messages[-1])
        return last_msg.content.startswith(prefix)
    return _inner
  
class ConvoState(BaseModel):
    done: bool = Field(default=False, description="conversation is set to done")
    yaml_conf: str = Field(default="", description="latest yaml configuration state representing all feeds")

def write_feeds_to_file(filename: str):
    def _inner(memory: Memory) -> bool:
        notebook_io.add_message_to_log("saving state to file", ROLE)
        with open(filename, 'w') as f:
            f.write(memory.state.yaml_conf)
        return PromptChain(memory)
    return _inner

def feed_output_prompts(feed_outputs): 
    parsed_yaml = yaml.safe_load(feed_outputs)
    content = f"""
    the following are the analyses performed by the application:
    """
    for node in parsed_yaml['requirements']:
        content += f" <b>ID: {node['id']}</b> \n content: {node['content']} \n"
    return content

def parse_msg_action(action: str):
    def _inner(memory: Memory):
        # parse just the last message
        msg = f"the following is a question/message/instruction from user: {action} command \n"
        parts = memory.messages[-1].content.split()
        for i, part in enumerate(parts):
            if part == action:
                # Join all the parts after ":explain" to form the output
                msg += ' '.join(parts[i:])
        return add_message(Message("user", msg))(memory)
    return _inner

def parse_msg_with_args(message: str, action:str):
    # Split the message on whitespace and find the ":edit" command
    parts = message.split(maxsplit=2)  # split into at most 3 parts
    if parts[0] == action:
        # Assign command and first argument
        command, arg1 = parts[0], parts[1]
        # Assign second argument if present, otherwise default to empty string
        arg2 = parts[2] if len(parts) > 2 else "" 
        return command, arg1, arg2
    else:
        return "Invalid format", "", ""

def set_feed_content(_id: str, update: str):
    def _inner(memory: Memory):
        parsed_yaml = yaml.safe_load(memory.state.yaml_conf)
        for requirement in parsed_yaml['requirements']:
            if requirement.get('id') == int(_id):
                requirement['content'] = update
                break
        setattr(memory.state, "yaml_conf", yaml.dump(parsed_yaml, sort_keys=False))
        return PromptChain(memory)
    return _inner

def run_generate_with_id():
    def _inner(memory: Memory):
        (_, _id, method_instruction) = parse_msg_with_args(memory.messages[-1].content, ":generate")
        # if user propose a new method, we regenerate method from requirement and overwrite it
        if method_instruction:
            new_method = generate_method_from_requirement_node(memory.state.yaml_conf, method_instruction)
            notebook_io.add_message_to_log(f"new method call generated with custom instruction: {new_method}", ROLE)
            # print(f"new method call generated with custom instruction: {new_method}")
            parsed_yaml = yaml.safe_load(memory.state.yaml_conf)
            for requirement in parsed_yaml['requirements']:
                if requirement.get('id') == int(_id):
                    requirement['method_call'] = new_method
                    break
            setattr(memory.state, "yaml_conf", yaml.dump(parsed_yaml, sort_keys=False))

        # find the requirement with id
        parsed_yaml = yaml.safe_load(memory.state.yaml_conf)
        for requirement in parsed_yaml['requirements']:
            if requirement.get('id') == int(_id):
                method = requirement.get('method_call', '')
        notebook_io.add_message_to_log(f"generating feed with ID: {_id}", ROLE)
        new_content = generate_func_output(method)
        new_content_msg = f"the following is a new output for {_id}: {new_content}"
        notebook_io.add_message_to_chat(f"generated new output, if you are satisfied- hit :confirm", ROLE, sender="bot")
        return (
            add_message(Message("assistant", new_content_msg))(memory)
            | notebook_io.add_last_message_chat("bot", ROLE)
            | add_user_input()
            | notebook_io.add_last_message_chat("user", ROLE)
            | condition(
                func=msg_prefixed_with(":confirm"),
                _do=set_feed_content(_id, new_content),
                _else=nothing(),
            )
        )
    return _inner 

def run_edit_with_id():
    def _inner(memory: Memory):
        (_, _id, msg) = parse_msg_with_args(memory.messages[-1].content, ":edit")
        # find the requirement with id
        content = ""
        parsed_yaml = yaml.safe_load(memory.state.yaml_conf)
        for requirement in parsed_yaml['requirements']:
            if requirement.get('id') == int(_id):
                content = requirement.get('content', '')
        notebook_io.add_message_to_log(f"making copy edit for feed with ID: {_id}", ROLE)
        old_content_msg = f"""
            the following is the old content from the content id that the I requested for you to make edits for: \n{content}\n
            create a new version in the next message, make sure to retain the core analytical data of the old content
            do not make comments about the edit, make sure the only thing you wrote in the next message is a new version of the content
        """

        new_content_chain = (
            add_message(Message("system", old_content_msg))(memory)
            | oai_chat_complete()
            | notebook_io.add_last_message_log(ROLE)
        )
        new_content = new_content_chain.memory.messages[-1].content
        notebook_io.add_message_to_chat(f"generated edits, if you are satisfied- hit :confirm", ROLE)

        return (
            new_content_chain
            | add_user_input()
            | notebook_io.add_last_message_chat("user", ROLE)
            | condition(
                func=msg_prefixed_with(":confirm"),
                _do=set_feed_content(_id, new_content),
                _else=nothing(),
            )
        )
    return _inner
def post_msgs_cms():
    def _inner(memory: Memory):
        # parse the requirements nodes into a list of body of texts
        parsed_yaml = yaml.safe_load(memory.state.yaml_conf)
        results = []
        for node in parsed_yaml['requirements']:
            try:
                results.append(generate_cms_post(node)) 
            except ValueError as e:
                raise ValueError(f"failed to generate content on cms, {e}")
        print(results)
        for r in results:
            notebook_io.add_last_message_log(f"successfully post content to CMS: id {r}")
        return PromptChain(memory)
    return _inner

def welcome_feed_chat_msg():
    welcome_txt = """
    Welcome to our chat with the analysis agent, our agent will run through the provided analysis requirements, please be patient
    """
    notebook_io.add_message_to_chat(welcome_txt, ROLE, sender="bot")

def analyses_success_chat_msg():
    txt = """
    All analyses has been successfully performed.
    Here is a guide for all the different commands you can use to interact with the analysis feeds:

    :edit <id> <instruction> -- ask the analysis agent to edit the feed copy with a given instruction
        after the analysis is generated, you will be prompted to type :confirm

    :generate <id> <instruction> -- ask the analysis agent to regenerate the feed of a certain ID, 
        instruction can be used to overwrite existing requirement, should you want to alter the requirement
        after the analysis is generated, you will be prompted to type :confirm

    :save -- save the state of the analysis for later consumption

    :explain <instruction> --ask the analysis agent to explain something about the generated feeds
    You can read through each analysis and each of their ID below:

    :post -- ask the analysis agent to post the analysis on the reader app for further consumptions
    providng additional metadata and chart in a rich text format
    """
    notebook_io.add_message_to_chat(txt, ROLE, sender="bot")

def run_feed_chat(path=None, requirements=""):
    # load and run all in the beginning
    notebook_io.create_analyst_chat_interface("")
    welcome_feed_chat_msg()
    if path and requirements == "":
        with open(path, 'r') as file:
            try:
                final_yaml_output = file.read()
            except yaml.YAMLError as exc:
                raise ValueError(f"error loading from path: {path}")
    else:
        feed_outputs = run_feeds_on_requirements(requirements)
        final_yaml_output = generate_yaml_output(feed_outputs, requirements)

    analyses_success_chat_msg()
    feed_output_messages = Message("system", feed_output_prompts(final_yaml_output))
    initial_memory = Memory(messages=[Message("system", "you are a helpful document assistant bot"), feed_output_messages], state=ConvoState(yaml_conf=final_yaml_output))
    initial_chain = add_message()(initial_memory)


    explain_stream = stream(
        parse_msg_action(":explain"),
        oai_chat_complete(),
        notebook_io.add_last_message_chat("bot", ROLE),
    )

    save_stream = stream(
        # write the entire yaml to local file
        write_feeds_to_file('feeds.yaml'),
        set_state("done", True),
    )
    
    convo_stream = stream(
        add_user_input(),
        notebook_io.add_last_message_chat("user", ROLE),
        condition(
            func=msg_prefixed_with(":edit"),
            _do=run_edit_with_id(),
            _else=nothing(),
        ),
        condition(
            func=msg_prefixed_with(":generate"),
            _do=run_generate_with_id(),
            _else=nothing(),
        ),
        condition(
            func=msg_prefixed_with(":explain"),
            _do=explain_stream,
            _else=nothing(),
        ),
        condition(
            func=msg_prefixed_with(":save"),
            _do=save_stream, # saves state and quit
            _else=nothing(),
        ),
        condition(
            func=msg_prefixed_with(":post"),
            _do=post_msgs_cms(),
            _else=nothing(),
        )
    )

    convo_loop = do_while(stream=convo_stream, exit_on=assert_state("done", True))
    return initial_chain | notebook_io.add_last_message_chat("bot", ROLE) | convo_loop