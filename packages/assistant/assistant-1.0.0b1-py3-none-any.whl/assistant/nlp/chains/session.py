import os
# from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import LLMSingleActionAgent, AgentExecutor, initialize_agent
# from langchain.memory import ConversationBufferMemory

from assistant.nlp.chains.agents import get_initialized_agent
from assistant.nlp.chains.prompts import get_prompt_with_memory
from assistant.nlp.chains.tools import get_all_tools
from assistant.nlp.chains.models import get_llm
from assistant.nlp.chains.parsers import get_output_parser
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.nlp.chains.memory.conversation_buffer import AssistantConversationBufferMemory

class SessionAssistant:
    def __init__(
            self,
            name="Assistant",
            max_tokens=2048,
            temperature=0.0,
            streaming=False,
            callbacks=[],
            verbose=False,
        ):
        self.name = name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.streaming = streaming
        self.callbacks = callbacks
        self.verbose = verbose
        self.memory_key = "chat_history"
        
        self._initialize_llm()
        self._initialize_prompt()
        self._initialize_output_parser()
        self._initialize_memory()
        self._initialize_chain()
        self._initialize_tools()
        self._initialize_agent()
          
    def _initialize_llm(self):
        self.llm = get_llm(max_tokens=self.max_tokens, temperature=self.temperature, streaming=self.streaming, callbacks=self.callbacks)

    def _initialize_prompt(self):
        self.prompt = get_prompt_with_memory(memory_key=self.memory_key)
    
    def _initialize_output_parser(self):
        self.output_parser = get_output_parser()
    
    def _initialize_memory(self):
        self.memory = AssistantConversationBufferMemory(memory_key=self.memory_key, input_key="input", output_key="output", human_prefix="User", ai_prefix="Assistant")

    def _initialize_chain(self):
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def _initialize_tools(self):
        self.tools = get_all_tools()

    def _initialize_agent(self, max_iterations=20):
        tool_names = [tool.name for tool in self.tools]
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["<|im_stop|>", "<|im_start|>"],
            allowed_tools=tool_names
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(agent=self.agent, tools=self.tools, verbose=self.verbose, max_iterations=max_iterations, memory=self.memory)

    def __call__(self, message: str):
        return self.process_output(self.agent_executor.run(input=message))
    
    def prompt_llm(self, promt_query: str, raw=False):
        """
        Execute the `llm` method with the given `promt_query` and process the output based on the `raw` flag.

        Parameters:
            promt_query (str): The prompt query string to be passed to the `llm` method.
            raw (bool, optional): If True, returns the raw output from `llm`. If False (default), processes the output using `process_output`.

        Returns:
            str: The processed output if it exists and `raw` is False. If `raw` is True, returns the raw output. Returns an empty string if no output is available.
        """
        txt = self.llm(promt_query)
        if txt and not raw:
            return self.process_output(txt)
        elif raw and txt:
            return txt
        else:
            return ""
    
    def process_output(self, output):
        """
        Remove special tokens from the given output and perform any necessary pre-processing steps.

        Args:
            output (str): The output to be processed.

        Returns:
            str: The processed output.
        """
        #output = output.split("```")[0]
        # output = output.split("</s>")[0]
        # output = output.replace("```\n\n```", "```</s> | <s>[INST] This hallucination will be discarded [/INST] ```").split(" | ")[0].removesuffix('<s>')
        # output = output.split("[/INST]")[0]
        # output = output.split("<|im_stop|>")[0]
        # dirty hack remove once model is ready
        # output = output.replace("Use the following input to take an action:", "")
        # Add other pre-processing steps here
        #return output.strip("\n")
        return output
    
    def __str__(self):
        return f"{self.name}: {self.max_tokens} tokens @{self.temperature}°"
    
    def export_conversation(self):
        """
        Export the conversation from the memory buffer.

        Returns:
            str: The conversation from the memory buffer.
        """
        return None #self.memory.export_conversation()

if __name__ == "__main__":
    assistant = SessionAssistant(temperature=0.0, max_tokens=200, verbose=True, callbacks=[InputOutputAsyncCallbackHandler()])
    
    while True:
        query = input(">>> ")
        if query == "exit":
            break
        print(assistant(query))
