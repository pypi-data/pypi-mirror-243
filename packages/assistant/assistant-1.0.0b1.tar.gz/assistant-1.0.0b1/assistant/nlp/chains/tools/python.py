from langchain.tools import Tool, BaseTool
# from langchain.utilities import PythonREPL
from io import StringIO
from contextlib import redirect_stderr, redirect_stdout
from xonsh.built_ins import XSH

from assistant.codecache import run_code_with_cache
from rich.markdown import Markdown

#python_repl = PythonREPL()

class PythonTool(BaseTool):
    name = "python"
    description = """\
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.\
"""
    
    def _run(self, code: str, **kwargs):
        try:
            shell = XSH.shell.shell
            shell.kernel_interface.spinner.info(f"Executing python command: {code}")
            output = []
            with StringIO() as stdout_buf, \
            StringIO() as stderrr_buf, \
            redirect_stdout(stdout_buf), \
            redirect_stderr(stderrr_buf):
                # _, code = shell.compile(code)
                exc_info = run_code_with_cache(code, display_filename="<xonsh-stdin>", execer=shell.execer, glb=shell.ctx, mode='single')
                stdout, stderr = stdout_buf.getvalue(), stderrr_buf.getvalue()
            if exc_info != (None, None, None):
                if exc_info[1] is not None:
                    output.append(str(exc_info[1]).strip())
            if stdout != "":
                output.append(stdout.strip())
            if stderr != "":
                output.append(f"{stderr.strip()}")
        except Exception as e:
            output.append(str(e).strip())
        return "\n".join(output) if output else ""
    
    async def _arun(self):
        pass

python = PythonTool()

def get_tool():
    return [
        Tool(
            name="python",
            func=python.run,
            description="""\
    description: This tool allows you to execute and evaluate python code.
    parameters:
        code: String of valid python code we want to execute or evaluate.\
"""
            ),
        ]
