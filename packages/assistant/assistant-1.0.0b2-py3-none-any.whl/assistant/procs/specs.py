import contextlib
import xonsh.platform as xp
import xonsh.tools as xt
from xonsh.built_ins import XSH
from xonsh.procs.specs import SubprocSpec

class AssistantSubprocSpec(SubprocSpec):
    def _run_binary(self, kwargs):
        if not self.cmd[0]:
            raise xt.XonshError("xonsh: subprocess mode: command is empty")
        bufsize = 1
        try:
            if xp.ON_WINDOWS and self.binary_loc is not None:
                # launch process using full paths (https://bugs.python.org/issue8557)
                cmd = [self.binary_loc] + self.cmd[1:]
            else:
                cmd = self.cmd
            p = self.cls(cmd, bufsize=bufsize, **kwargs)
        except PermissionError as ex:
            e = "xonsh: subprocess mode: permission denied: {0}"
            raise xt.XonshError(e.format(self.cmd[0])) from ex
        except FileNotFoundError as ex:
            is_nlp_server_up = XSH.shell.shell.kernel_interface.is_nlp_server_up()
            if is_nlp_server_up:
                answer = XSH.shell.shell.kernel_interface.assistant(" ".join(self.cmd))
                with contextlib.suppress(OSError):
                    return self.cls(
                        ["echo", f"'{answer}'"], bufsize=bufsize, **kwargs
                    )
            else:
                cmd0 = self.cmd[0]
                if len(self.cmd) == 1 and cmd0.endswith("?"):
                    if self.cmd0.lower() == "assistant?":
                        e = "Assistant: Sorry, I'm unable to reach Linguistic Services at the moment."
                        e += "\nXonsh is here to answer any of your commands."
                        e += "\nTo enable Linguistic Services, type:\npython -m assistant.as_services in another shell session."
                        raise xt.XonshError(e) from ex
                    else:
                        with contextlib.suppress(OSError):
                            return self.cls(
                                ["man", cmd0.rstrip("?")], bufsize=bufsize, **kwargs
                            )
                e = f"xonsh: subprocess mode: command not found: {repr(cmd0)}"
                env = XSH.env
                sug = xt.suggest_commands(cmd0, env)
                if len(sug.strip()) > 0:
                    e += "\n" + xt.suggest_commands(cmd0, env)
                if XSH.env.get("XONSH_INTERACTIVE"):
                    events = XSH.builtins.events
                    events.on_command_not_found.fire(cmd=self.cmd)
                raise xt.XonshError(e) from ex
        return p