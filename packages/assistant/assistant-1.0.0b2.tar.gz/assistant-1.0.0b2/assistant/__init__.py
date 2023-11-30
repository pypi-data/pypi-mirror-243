#from xonsh.main import setup
import os

__version__="1.0.0b2"

USERNAME = os.environ.get("USER", 'root')
HOME = os.environ.get('HOME', f'/home/{USERNAME}' if USERNAME != 'root' else '/root')
ASSISTANT_PATH = f"{HOME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"
LANG = os.environ.get('LANG', "en_EN.UTF-8")
try:
    I18N, L10N = (x for x in LANG.split(".")[0].split("_"))
except ValueError:
    I18N, L10N = ("en", "EN")
LANGUAGE = f"{I18N} ({L10N})"
LANGUAGE_CODE = f"{I18N}_{L10N}"
