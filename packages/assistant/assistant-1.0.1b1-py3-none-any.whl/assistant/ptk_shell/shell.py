import os, sys
import time
import xonsh.tools as xt
import subprocess

from io import StringIO
from contextlib import redirect_stderr, redirect_stdout
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import merge_completers
from xonsh.events import events
from xonsh.jobs import jobs
from xonsh.ptk_shell.shell import PromptToolkitShell
from xonsh.base_shell import Tee
from xonsh.built_ins import XSH
from assistant import ASSISTANT_PATH
from assistant.nlp.interface import AssistantInterface
from assistant.ptk_shell.completer import AssistantCompleter
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.execer import AssistantExecer
from assistant import codecache
from assistant.procs.specs import AssistantSubprocSpec
from assistant.procs.pipelines import AssistantCommandPipeline

class AssistantShell(PromptToolkitShell):
    console = Console()
    error_console = Console(stderr=True, style="bold red")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        callbacks = []
        is_debug = bool(XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False))
        if is_debug:
            callbacks.append(InputOutputAsyncCallbackHandler())
        self.kernel_interface = AssistantInterface(verbose=is_debug, callbacks=callbacks)
        self.pt_completer = merge_completers([self.pt_completer, AssistantCompleter()])
        self.execer = AssistantExecer()
        self.subproc_spec_cls = AssistantSubprocSpec
        jobs.pipeline_class = AssistantCommandPipeline
        

    def default(self, line, raw_line=None):
        """Implements code execution."""
        line = line if line.endswith("\n") else line + "\n"
        if not self.need_more_lines:  # this is the first line
            if not raw_line:
                self.src_starts_with_space = False
            else:
                self.src_starts_with_space = raw_line[0].isspace()
        src, code = self.push(line)
        if code is None:
            return # Should probably feed src to LM instead

        events.on_precommand.fire(cmd=src)

        env = XSH.env
        hist = XSH.history  # pylint: disable=no-member
        ts1 = None
        enc = env.get("XONSH_ENCODING")
        err = env.get("XONSH_ENCODING_ERRORS")
        tee = Tee(encoding=enc, errors=err)
        ts0 = time.time()
        try:
            with StringIO() as stdout_buf, \
            StringIO() as stderr_buf, \
            redirect_stdout(stdout_buf), \
            redirect_stderr(stderr_buf):
                exc_info = codecache.run_compiled_code(code, self.ctx, None, "single")
                _out = stdout_buf.getvalue() or stderr_buf.getvalue()
            if exc_info != (None, None, None):
                raise exc_info[1]
            ts1 = time.time()
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 0  # returncode for success
        except xt.XonshError as e:
            if str(e.args[0]).strip() != "":
                self.log_error(str(e.args[0]).strip())
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        except (SystemExit, KeyboardInterrupt) as err:
            raise err
        except BaseException:
            xt.print_exception(exc_info=exc_info)
            if hist is not None and hist.last_cmd_rtn is None:
                hist.last_cmd_rtn = 1  # return code for failure
        finally:
            ts1 = ts1 or time.time()
            tee_out = tee.getvalue() or _out
            if hist.last_cmd_rtn == 0:
                if tee_out.strip() != "":
                    self.log_response(Markdown(f"""```text
{tee_out.strip()}
```"""))
            else:
                # Subbproc command failed check stdout/err to find why.
                t = tee_out.split(": ")
                if all(item in t for item in ['xonsh', 'subprocess mode', 'command not found']):
                    # Xonsh: subprocess mode: did not found command
                    if self.kernel_interface.is_nlp_server_up():
                        # Assistant: LM is up
                        tee_out = self.kernel_interface.assistant(raw_line.strip())
                        if tee_out != "":
                            hist.last_cmd_rtn = 0
                            self.log_response(Markdown(tee_out.strip()))
            self._append_history(
                inp=src,
                ts=[ts0, ts1],
                spc=self.src_starts_with_space,
                tee_out=tee_out,
                cwd=self.precwd,
            )
            self.accumulated_inputs += src
            # if (
            #     tee_out
            #     and env.get("XONSH_APPEND_NEWLINE")
            #     and not tee_out.endswith(os.linesep)
            # ):
            #     print(os.linesep, end="")
            tee.close()
            self._fix_cwd()
        if XSH.exit:  # pylint: disable=no-member
            self.set_last_seen()
            return True

    def cmdloop(self, intro=None):
        """Enters a loop that reads and execute input from user."""
        if intro:
            self.log_response(Markdown(intro))
        auto_suggest = AutoSuggestFromHistory()
        while not XSH.exit:
            try:
                line = self.singleline(auto_suggest=auto_suggest)
                if not line:
                    self.emptyline()
                else:
                    raw_line = line
                    line = self.precmd(line)
                    self.default(line, raw_line)
            except SystemExit:
                self.reset_buffer()
            except KeyboardInterrupt:
                self.reset_buffer()
                self.log_error(Markdown("# KeyboardInterrupt\n[Ctrl] + [C]: cannot be used to exit a shell.\n\nTry to ask nicely with exit or be rude: [Ctrl] + [D]"))
                continue
            except EOFError:
                if XSH.env.get("IGNOREEOF"):
                    print('Use "exit" to leave the shell.', file=sys.stderr)
                else:
                    break
            except (xt.XonshError, xt.XonshCalledProcessError) as xe:
                self.handle_xonsh_error(xe, raw_line)
            except NameError as ne:
                # Handle the NameError, you can use your LLM here to answer the query.
                self.handle_name_error(ne, raw_line)
            except SyntaxError as se:
                # Handle the SyntaxError, you can use your LLM here to provide guidance.
                self.handle_syntax_error(se, raw_line)
            except Exception as e:
                # Handle other exceptions as needed.
                self.handle_other_exceptions(e, raw_line) 
            

    def set_last_seen(self):
        last_seen_file = os.path.join(ASSISTANT_PATH, "history", ".last_seen")
        try:
            os.mkdir(os.path.join(ASSISTANT_PATH, "history"))
        except FileExistsError:
            pass
        with open(last_seen_file, "w") as f:
            f.write(subprocess.check_output(["date"]).decode("utf-8").strip())
    
    def log_query(self, query):
        self.console.print(query, style="italic blue", justify="right")

    def log_response(self, response):
        self.console.print(response, style="bold white", justify="left")

    def log_error(self, error):
        self.error_console.print(error, style="bold red", justify="left")

    def handle_xonsh_error(self, error, raw_line):
        # Handle the NameError here using your LLM or any other logic.
        self.log_error(Markdown(f"# Xonsh\nYou said '{raw_line}' but {error}"))

    def handle_name_error(self, error, raw_line):
        # Handle the NameError here using your LLM or any other logic.
        self.log_error(Markdown(f"# NameError\nYou said '{raw_line}' but {error}"))

    def handle_syntax_error(self, error, raw_line):
        # Handle the SyntaxError here using your LLM or provide guidance.
        self.log_error(Markdown(f"# SyntaxError\nYou said '{raw_line}' but {error}"))

    def handle_other_exceptions(self, error, raw_line):
        # Handle other exceptions as needed using your logic.
        self.log_error(Markdown(f"# Exception\nYou said '{raw_line}' but {error}"))

