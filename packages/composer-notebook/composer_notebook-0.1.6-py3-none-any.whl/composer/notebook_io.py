import datetime
import threading
import time
from molang.models import *
from molang.helper import *
from molang.core import *
from IPython.display import display, HTML
import ipywidgets as widgets

planner_log_output = widgets.Output(layout={'border': '1px solid black', 'width': '30%', 'height': '300px', 'overflow': 'auto'})
planner_chat_output = widgets.Output(layout={'border': '1px solid black', 'width': '70%', 'height': '300px', 'overflow': 'auto'})
analyst_log_output = widgets.Output(layout={'border': '1px solid black', 'width': '30%', 'height': '300px', 'overflow': 'auto'})
analyst_chat_output = widgets.Output(layout={'border': '1px solid black', 'width': '70%', 'height': '300px', 'overflow': 'auto'})

class LookupError(Exception):
    pass

# Define the nested dictionary
outputs = {
    "planner": {
        "log": planner_log_output,
        "chat": planner_chat_output
    },
    "analyst": {
        "log": analyst_log_output,
        "chat": analyst_chat_output
    }
}

def table_get_output(role, target):
    # Check if the role exists
    if role not in outputs:
        raise LookupError(f"Role '{role}' not found")

    # Check if the target exists for the given role
    if target not in outputs[role]:
        raise LookupError(f"Target '{target}' not found for role '{role}'")

    # Return the corresponding widget output object
    return outputs[role][target]

def add_message_to_log(log_message, role):
    """Outputs a log message with a timestamp."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] {log_message}"
    preformatted_html = HTML(f"<pre>{formatted_message}</pre>") # Wrap in preformatted HTML
    table_get_output(role, "log").append_display_data(preformatted_html)

def add_message_to_chat(message_content, role, sender="user"):
    """Adds a message to the specified output area with a specific style."""
    formatted_message = message_content.replace("\n", "<br>")

    if sender == "user":
        html_content = HTML(f"<div style='text-align: left; margin: 5px; padding: 5px; border: 1px solid gray; border-radius: 5px;'> 👤 <br> {formatted_message}</div>")
    else:
        html_content = HTML(f"<div style='text-align: left; margin: 5px; padding: 5px; border: 1px solid yellow; border-radius: 5px;'> 🤖 <br> {formatted_message}</div>")
    table_get_output(role, "chat").append_display_data(html_content)

def add_last_message_chat(sender, role):
    def _inner(memory: Memory):
        add_message_to_chat(memory.messages[-1].content, role, sender)
        return PromptChain(memory)
    return _inner

def add_last_message_log(role):
    def _inner(memory: Memory):
        add_message_to_log(memory.messages[-1].content, role)
        return PromptChain(memory)
    return _inner

def create_planner_chat_interface(memory):
    ui = widgets.VBox([widgets.HBox([planner_chat_output, planner_log_output])])
    display(ui)

def create_analyst_chat_interface(memory):
    ui = widgets.VBox([widgets.HBox([analyst_chat_output, analyst_log_output])])
    display(ui)
