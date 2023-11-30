import json
import re

from langchain.agents import AgentOutputParser
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.output_parsers.json import parse_json_markdown as _parse_jsonmd
from langchain.schema import AgentAction, AgentFinish

from json.decoder import JSONDecodeError


def parse_json(json_string: str) -> dict:
    """
    Parse a JSON dict from a string.

    Args:
        json_string: The string.

    Returns:
        The parsed JSON object as a Python dictionary.
    """
    json_str = json_string

    # Strip whitespace and newlines from the start and end
    json_str = json_str.strip()

    # handle newlines and other special characters inside the returned value
    # json_str = _custom_parser(json_str)

    # Parse the JSON string into a Python dictionary
    parsed = json.loads(json_str)

    return parsed


class JsonOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> AgentAction | AgentFinish:
        _text = self.handle_model_specifics(text)
        # print(_text)
        try:
            # this will work IF the text is a valid JSON with function and parameters
            json_resp = parse_json(_text)
            func, params = json_resp["function"], json_resp["parameters"]
            if func.lower().replace(" ", "_") == "final_answer":
                # this means the agent is finished so we call AgentFinish
                return AgentFinish({"output": params["answer"]}, _text)
            # otherwise the agent wants to use an action, so we call AgentAction
            return AgentAction(func, params, _text)
        except KeyError as ke:
            _ke = str(ke).strip()
            if isinstance(json_resp, dict) and _ke != "'function'":
                # LLM did manage to respond a json parsable dict but failed to generate the expected format
                # lets try to handle it any way
                func = json_resp.pop("function")
                params = json_resp
                if func.lower().replace(" ", "_") == "final_answer":
                    # this means the agent is finished so we call AgentFinish
                    return AgentFinish({"output": params["answer"]}, _text)
                # otherwise the agent wants to use an action, so we call AgentAction
                return AgentAction(
                    func, params, f"KeyError: Missing key: {_ke}\nLLM Response: {_text}"
                )
        except JSONDecodeError as jsde:
            # LLM failed to respond a json parsable dict
            return AgentFinish(
                {"output": _text},
                f"JSONDecodeError: Could not parse output: {str(jsde)}\nLLM Response: {_text}",
            )

    def handle_model_specifics(self, model_output: str) -> str:
        """
        Remove special tokens from the given output and perform any necessary pre-processing steps.
        """
        model_output = model_output.split("<|im_stop|>")[0]
        # model_output = model_output.split("<s>[INST]")[0]
        # model_output = model_output.split("</s>")[0]
        # model_output = model_output.replace(
        #     "```\n\n```", "```</s> | <s>[INST] This hallucination will be discarded [/INST] ```"
        #     ).split(" | ")[0].removesuffix('<s>')
        # model_output = model_output.split("[/INST]")[0].strip()
        # model_output = model_output.split("[INST]")[0].strip()
        # text = text.replace("""</s>""", "")
        # text = text.replace("\n", '')
        # text = text.replace("\t", '')
        # text = text.replace("\r", '')
        # text = text.replace(" ", '')
        # text = text.replace("```json", '')
        # text = text.replace("```", '')
        # model_output = model_output.strip("\n")
        while model_output.endswith("<|im_stop|>"):
            model_output = model_output.removesuffix("<|im_stop|>")
        return model_output

    @property
    def _type(self) -> str:
        return "conversational_chat"


if __name__ == "__main__":
    js_text = [
        """{ "function": "final_answer", "answer": "L'écran a été effacé. Je suis prêt à vous aider si vous avez besoin d'aide ou de questions." }""",
        """{ "function": "final_answer", "parameters": {"answer": "L'écran a été effacé. Je suis prêt à vous aider si vous avez besoin d'aide ou de questions."} }""",
    ]
    for text in js_text:
        json_dict = parse_json(text)
        try:
            function, parameters = json_dict["function"], json_dict["parameters"]
        except KeyError:
            function = json_dict.pop("function")
            parameters = json_dict
        
        print(f"{function=}")
        print(f"{parameters=}")
