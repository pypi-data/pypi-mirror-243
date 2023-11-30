from langchain.tools import Tool, BaseTool, DuckDuckGoSearchRun

from xonsh.built_ins import XSH
from rich.markdown import Markdown

class SearchTool(BaseTool):
    name = "search_web"
    description = """\
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.\
"""
    engine = DuckDuckGoSearchRun()
    
    def _run(self, terms: str, **kwargs):
        try:
            shell = XSH.shell.shell
            shell.kernel_interface.spinner.info(f"Searching the Web for: {terms}")
            # TODO: get answer here and print it and return it instead.
            output = self.engine.run(terms)
#             if output:
#                 shell.log_response(Markdown(f"""```text
# {output}
# ```"""))
        except Exception:
            print(f"Searching the Web for: {terms}")
            output = self.engine.run(terms)
            # TODO: get answer here and print it and return it instead.
            # if output:
            #     print(output)
        return output or ""
    
    # async def _arun(self):
    #     pass

def get_tool():
    search = SearchTool()
    return [
            Tool(
                name="search_web",
                func=search.run,
                description="""\
    description: This tool performs search on the web.
    parameters:
        terms: The word or phrase we want to search for.\
"""
                ),
            ]