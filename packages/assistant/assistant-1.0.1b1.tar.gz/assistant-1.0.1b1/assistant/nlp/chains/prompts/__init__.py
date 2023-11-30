import os
import subprocess
from langchain.prompts import StringPromptTemplate #, ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.schema import BaseRetriever
from typing import Callable

from assistant import ASSISTANT_PATH
from assistant.nlp.chains.tools import get_all_tools
from assistant.nlp.chains.embeddings import get_embeddings
from assistant.nlp.chains.prompts.json import (
    get_structured_template,
    get_structured_template_with_memory
)
from assistant.nlp.chains.schema.vectorstore import get_agi_retriever #, AGIRetriever

class AgentPromptTemplate(StringPromptTemplate):
    # The template to use
    template: str
    # The list of tools available
    tools_getter: Callable
    retriever: BaseRetriever #AGIRetriever

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        user_input = kwargs["input"]

        if intermediate_steps:
            _thoughts = []
            for action, observation in intermediate_steps:
                _thoughts.append(f"""<|im_start|>assistant
{{
    "function": "{action.tool}",
    "parameters": "{action.tool_input}"
}}<|im_end|>
<|im_start|>observation
You and the User have observed the following from {action.tool}.

```{action.tool}
{observation}
```

Use this information to comment it in context of the User input.
<|im_end|>""")
            thoughts = "\n" + "\n".join(_thoughts) + "\n"
        else:
            thoughts = ""

        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts

        kwargs["guide"] = self.get_guide_from_query(user_input)

        tools = self.tools_getter()
        # tools = self.tools_getter(kwargs["input"])
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}:\n{tool.description}" for tool in tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in tools])

        # # Add environment variables from printenv
        kwargs["env"] = self.get_environ()

        # Format the template
        return self.template.format(**kwargs)

    def get_guide_from_query(self, query):
        # Get the guide from the query
        documents = self.retriever.get_relevant_documents(query=query)
        if documents:
            return documents[0].page_content
        return "No relevant guide for the query where found. Do what you can; with what you have."

    def get_environ(self):
        # Get the environment variables from printenv
        # return subprocess.check_output(["printenv"]).decode("utf-8")
        LANG = os.environ.get("LANG", "en_US.UTF-8")
        USER = os.environ.get("USER", "root")
        HOME = os.environ.get("HOME", "/root")
        PWD=os.environ.get("PWD", "/root")
        date = subprocess.check_output(["date"]).decode("utf-8").strip()
        os.environ['DATE'] = date
        DATE = date
        LAST_SEEN = self.last_seen()
        return f"""```env
{USER=}
{HOME=}
{PWD=}
{LANG=}
{DATE=}
{LAST_SEEN=}
```"""

    def last_seen(self):
        # last saw the user
        last_seen_file = os.path.join(ASSISTANT_PATH, "history", ".last_seen")
        if os.path.exists(last_seen_file):
            with open(last_seen_file, "r") as f:
                last_seen = f.read()
            os.environ['LAST_SEEN'] = last_seen
            return last_seen
        return None

template = get_structured_template()
memory_template = get_structured_template_with_memory()
embeddings = get_embeddings()
agi_retriever = get_agi_retriever(embeddings)
del embeddings # unload embeddings from memory after vector db initialisation

def get_prompt(template=template, retriever=agi_retriever):
    return AgentPromptTemplate(
        template=template,
        tools_getter=get_all_tools,
        #tools_getter=get_relevant_tools_from_query,
        # This omits the `agent_scratchpad`, `env`, `tools`, `tool_names` and `guide` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps", "guide"],
        retriever=retriever,
    )

def get_prompt_with_memory(template=memory_template, memory_key="chat_history", retriever=agi_retriever):
    return AgentPromptTemplate(
        template=template,
        tools_getter=get_all_tools,
        #tools_getter=get_relevant_tools_from_query,
        # This omits the `agent_scratchpad`, `env`, `tools`, `tool_names` and `guide` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=[memory_key, "input", "intermediate_steps"],
        retriever=retriever,
    )
