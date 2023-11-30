import builtins
import os, sys
import re
from xonsh.jobs import jobs
from xonsh import environ
from subprocess import CalledProcessError
from xonsh.events import events
from xonsh.tools import XonshError
from xonsh.shell import Shell
from assistant.ptk_shell.shell import AssistantShell
from assistant.procs.specs import AssistantSubprocSpec
from assistant.procs.pipelines import AssistantCommandPipeline
# from assistant.execer import Execer, AssistantExecer

@events.on_postcommand
def handle_natural_language(cmd: str, rtn: int, out: str or None, ts: list):
    if rtn != 0 and out not in ["", None]:
       print(f"A language model could help you with your query.")

@events.on_precommand
def handle_user_command(cmd, stdin, stdout, stderr):
    try:
        # Attempt to compile the command
        builtins.__xonsh_shell__.execer.compile(cmd, filename='<xonsh-input>', mode='single')

        # Execute the command using Xonsh's capabilities
        builtins.__xonsh_shell__.execer.eval(cmd, glbs={}, locs={})
    except FileNotFoundError as e:
        # This is a common exception for command not found
        # Handle this case as if the user is chitchatting
        lm_response = "I'm here to assist with commands."
        stdout.write(lm_response)
    except XonshError:
        # Other Xonsh errors can be handled as well
        lm_response = "There was an error executing the command."
        stdout.write(lm_response)

def load_custom_shell():
    os.environ.update('RAISE_SUBPROC_ERROR', False)
    # builtins.__xonsh_execer__ = AssistantExecer()
    builtins.__xonsh_shell__ = AssistantShell() #execer=builtins.__xonsh_execer__)
    events.on_postcommand.register(handle_natural_language)
    events.on_precommand.register(handle_user_command)
    builtins.__xonsh_shell__.subproc_spec_cls = AssistantSubprocSpec()
    jobs.pipeline_class = AssistantCommandPipeline
    

def unload_custom_shell():
    # Restore the original shell
    builtins.__xonsh_shell__ = Shell()
    # builtins.__xonsh_execer__ = Execer()

def xontrib_load():
    # Load the custom shell when the xontrib is loaded
    load_custom_shell()

def xontrib_unload():
    # Unload the custom shell when the xontrib is unloaded
    unload_custom_shell()
