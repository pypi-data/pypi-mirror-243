import warnings
from langchain.tools import Tool, BaseTool
from langchain.utilities import WikipediaAPIWrapper

from xonsh.built_ins import XSH
from rich.markdown import Markdown

# Filter out the GuessedAtParserWarning warning
warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')


encyclopedia = WikipediaAPIWrapper()

class WikipediaTool(BaseTool):
    name = "search_wikipedia"
    description = """\
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).\
"""
    

    def _run(self, input: str, **kwargs):
        try:
            shell = XSH.shell.shell
            shell.kernel_interface.spinner.info(f"Searching Wikipedia for: {input}")
            output = encyclopedia.run(f"{input}")
            # TODO: get answer here and print it and return it instead.
            # if output:
            #     shell.log_response(Markdown(output))
        except Exception as e:
            print(f"Searching Wikipedia for: {input}")
            output = encyclopedia.run(input)
            # TODO: get answer here and print it and return it instead.
            # if output:
            #     print(output)
        return output or ""
    
    async def _arun(self):
        pass

def get_tool():
    wiki = WikipediaTool()
    return [
            Tool(
                name="search_wikipedia",
                func=wiki.run,
                description="""\
    description: This tool performs search on Wikipedia (only in english).
    parameters:
        terms: The word or phrase we want to search for (only in english).\
"""
                )
            ]