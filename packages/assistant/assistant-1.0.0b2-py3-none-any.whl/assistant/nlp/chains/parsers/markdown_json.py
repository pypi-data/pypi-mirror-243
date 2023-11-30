import json
import re

from langchain.agents import AgentOutputParser
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.output_parsers.json import parse_json_markdown as _parse_jsonmd
from langchain.schema import AgentAction, AgentFinish

from json.decoder import JSONDecodeError


def parse_json_markdown(json_string: str) -> dict:
    """
    Parse a JSON string from a Markdown string.

    Args:
        json_string: The Markdown string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    # Try to find JSON string within triple backticks
    match = re.search(r"```(json)?(.*)```", json_string, re.DOTALL)

    # If no match found, assume the entire string is a JSON string
    if match is None:
        json_str = json_string
    else:
        # If match found, use the content within the backticks
        json_str = match.group(2)

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    # handle newlines and other special characters inside the returned value
    # json_str = _custom_parser(json_str)

    # Parse the JSON string into a Python dictionary
    parsed = json.loads(json_str)

    return parsed

class MarkdownOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> AgentAction | AgentFinish:
        _text = self.handle_model_specifics(text)
        # print(_text)
        try:
            # this will work IF the text is a valid JSON with action and action_input
            response = parse_json_markdown(_text)
            action, action_input = response["action"], response["action_input"]
            # print(f"Detected Aciton: {action} with input: {action_input}")
            if action == "Final Answer":
                # print("Final Answer:")
                # this means the agent is finished so we call AgentFinish
                return AgentFinish({"output": action_input}, _text)
            else:
                # print(f"Running action {action} with input {action_input}.")
                # otherwise the agent wants to use an action, so we call AgentAction
                return AgentAction(action, action_input, _text)
        
        except Exception as e:
            try:
                response = _parse_jsonmd(_text)
                action, action_input = response["action"], response["action_input"]
                # print(f"Detected Aciton: {action} with input: {action_input}")
                if action == "Final Answer":
                    # print("Final Answer:")
                    # this means the agent is finished so we call AgentFinish
                    return AgentFinish({"output": action_input}, _text)
                else:
                    # otherwise the agent wants to use an action, so we call AgentAction
                    return AgentAction(action, action_input, _text)
            except Exception as _e:
                # print("Not a final answer:")
                return AgentFinish({"output": _text}, _text)

    def handle_model_specifics(self, text):
        #text = text.split("\n\n### ")[0]
        text = text.split("<s>[INST]")[0]
        text = text.split("</s>")[0]
        text = text.replace(
            "```\n\n```", "```</s> | <s>[INST] This hallucination will be discarded [/INST] ```"
            ).split(" | ")[0].removesuffix('<s>')
        text = text.split("[/INST]")[0].strip()
        text = text.split("[INST]")[0].strip()
        #text = text.replace("""</s>""", "")
        # text = text.replace("\n", '')
        # text = text.replace("\t", '')
        # text = text.replace("\r", '')
        # text = text.replace(" ", '')
        # text = text.replace("```json", '')
        # text = text.replace("```", '')
        text = text.strip("\n")
        return text

    @property
    def _type(self) -> str:
        return "conversational_chat"

if __name__ == "__main__":
    text = """```json
{"action": "Final Answer",
 "action_input": "Je suis Assistant, un assistant intelligent. Je suis là pour vous aider avec vos questions et vos besoins. Je suis programmé pour être poli, respectueux et efficace. Je suis à votre disposition pour vous aider dans vos projets et vos activités. Je suis heureux de vous aider dans n'importe quelle situation.",
 "observation": "User has seen this message."                                     
 }
```"""
    response = parse_json_markdown(text)
    action, action_input = response["action"], response["action_input"]
    if response.get("observation"):
        observation = response["observation"]
    else:
        observation = None
    
    print(f"{action=}")
    print(f"{action_input=}")
    print(f"{observation=}")