from subprocess import CalledProcessError
from xonsh.procs.pipelines import CommandPipeline
from xonsh.built_ins import XSH
class AssistantCommandPipeline(CommandPipeline):
    """Represents a subprocess-mode command pipeline."""

    def _raise_subproc_error(self):
        """Raises a subprocess error, if we are supposed to."""
        spec = self.spec
        rtn = self.returncode

        if rtn is None or rtn == 0 or not XSH.env.get("RAISE_SUBPROC_ERROR"):
            return

        try:
            raise CalledProcessError(rtn, spec.args, output=self.output)
        finally:
            # this is need to get a working terminal in interactive mode
            self._return_terminal()