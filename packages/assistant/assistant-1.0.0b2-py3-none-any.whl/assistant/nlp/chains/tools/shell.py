import sys
import subprocess
from io import StringIO
from contextlib import redirect_stderr, redirect_stdout 
from langchain.tools import Tool, BaseTool
# from langchain.utilities import BashProcess

from prompt_toolkit.shortcuts import clear
from xonsh.built_ins import XSH

from rich.markdown import Markdown

from assistant.codecache import run_code_with_cache

ASSISTANT = "Assistant"

def exit_shell(salutation: str,
    verbose: bool | None = None,
    start_color: str | None = "green",
    color: str | None = "green",
    callbacks = None,
    **kwargs):
    #spinner.stop()
    try:
        XSH.exit = True
        if hasattr(XSH.shell.shell, 'kernel_interface'):
            if hasattr(XSH.shell.shell.kernel_interface, "spinner"):
                XSH.shell.shell.kernel_interface.spinner.info(f"Exiting shell...")
                XSH.shell.shell.kernel_interface.spinner.stop()
        if tool_input and tool_input != "None" and salutation and salutation != "None" and salutation.lower().strip() != "exiting shell...":
            XSH.shell.shell.log_response(Markdown(salutation))
    except Exception:
        # print(f"Exiting shell...")
        if salutation and salutation != "None" and salutation.lower().strip() != "exiting shell...":
            print(salutation)
    finally:
        sys.exit(0)
        
class ClearScreenTool(BaseTool):
    name = "clear"
    description = """\
    description: This tool allows you to clear the screen / start a new fresh conversation.
"""

    def _run(self, fortune: str | None = None, **kwargs):
        #spinner.stop()
        try:
            shell = XSH.shell.shell
            if hasattr(shell, 'kernel_interface'):
                if hasattr(shell.kernel_interface, "spinner"):
                    shell.kernel_interface.spinner.info(f"Clearning screen...")
                    shell.kernel_interface.spinner.stop()
            clear()
            # if fortune and fortune != "None": shell.log_response(Markdown(fortune))
        except Exception:
            print(f"Clearning screen...")
            clear()
            # if fortune and fortune != "None": print(fortune)
    
    async def _arun(self):
        #spinner.stop()
        clear()

class ShellTool(BaseTool):
    name = "shell"
    description = """\
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.\
"""
    def _run(self, code: str, **kwargs):
        # input_parse = XSH.shell.shell.parser.parse(code)
        try:
            shell = XSH.shell.shell
            shell.kernel_interface.spinner.info(f"Executing shell command: {code}")
            output = []
            with StringIO() as stdout_buf, \
            StringIO() as stderr_buf, \
            redirect_stdout(stdout_buf), \
            redirect_stderr(stderr_buf):
                exc_info = run_code_with_cache(code + "\n", display_filename="<xonsh-stdin>", execer=shell.execer, glb=shell.ctx, mode='single')
                stdout, stderr = stdout_buf.getvalue(), stderr_buf.getvalue()
            if exc_info != (None, None, None):
                output.append(str(exc_info[1]).strip())
            if stdout != "":
                output.append(stdout.strip())
            if stderr != "":
                output.append(stderr.strip())
        except Exception as e:
            # print(str(e).strip())
            output.append(str(e).strip())
        return "\n".join(output) if output else subprocess.run(code, shell=True, capture_output=True).stdout.decode("utf-8")
    
    async def _arun(self):
        #spinner.stop()
        pass

def get_tool():
    # persistent_process = BashProcess(persistent=True)
    shell = ShellTool()
    clear_tool = ClearScreenTool()
    return [
            Tool(
                name="shell",
                func=shell.run,
                description="""\
    description: This tool allows you to execute and evaluate shell code.
    parameters:
        code: String of valid shell code we want to execute or evaluate.\
""",
            ),
            Tool(
                name="exit",
                func=exit_shell,
                description="""\
    description: This tool allows you to exit the session / end the conversation. Use it only if the User ask you to.
    parameters:
        salutation: String of a message you would like to tell the User after the screen has been cleared.\
""",
            ),
            Tool(
                name="clear",
                func=clear_tool.run,
                description="""\
    description: This tool allows you to clear the screen / start a new fresh conversation. Use it only if the User ask you to.
""",
            ),
        ]
