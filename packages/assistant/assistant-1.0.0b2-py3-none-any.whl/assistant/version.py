import sys
from datetime import date
from prompt_toolkit import print_formatted_text
from xonsh import __version__ as __xonsh_version__
from assistant.ptk_shell.strformat_utils import get_ftext_banner
# from assistant.as_client import nlp_intent_hello_version
from assistant import __version__ as __assistant_version__

def print_version():
    xonsh_version = "/".join(("xonsh", __xonsh_version__))
    version = "#".join(("assistant", __assistant_version__))
    print_formatted_text(get_ftext_banner())
    print(xonsh_version)
    print(version)
    print()
    print(f"Copyright © {str(date.today().year)}, Danny Waser")
    sys.exit()