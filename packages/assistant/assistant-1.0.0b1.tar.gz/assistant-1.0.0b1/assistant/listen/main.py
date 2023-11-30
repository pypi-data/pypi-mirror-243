import os, sys
import json
# import websockets
import asyncio
import signal
from time import sleep
# from websockets.exceptions import ConnectionClosedOK
from rich.console import Console
from rich.markdown import Markdown

try:
    from listen import mic
    #from listen.STT import enable_service_now as listen_now
    from listen.Wav2Vec import utils as stt_utils
except (ModuleNotFoundError, ImportError) as e:
    print(e)
    print("To speak with Assistant, you need to install the listen module.")
    print("Run the following command:\n```shell\npip install -r stt-listen\n```")
    sys.exit(1)

try:
    from say.TTS.as_client import _say
    from say.TTS import utils as tts_utils
    # from num2words import num2words
except (ModuleNotFoundError, ImportError) as e:
    print(e)
    print("To speak with Assistant, you need to install the say module.")
    print("Run the following command:\n```shell\npip install -r tts-say\n```")
    sys.exit(1)

from assistant.nlp.chains.session import SessionAssistant

STT_CONFIG = stt_utils.get_config_or_default()
is_allowed_to_listen = stt_utils.is_allowed_to_listen(STT_CONFIG)
if is_allowed_to_listen:
    #listen_now()
    pass
else:
    print("System has not user autorization to listen.")
    sys.exit(1)

TTS_CONFIG = tts_utils.get_config_or_default()
is_allowed_to_speak = tts_utils.is_allowed_to_speak(TTS_CONFIG)
if is_allowed_to_speak:
    pass
else:
    print("System has not user autorization to speak.")
    #sys.exit(1)

signal.signal(signal.SIGINT, signal.SIG_DFL)

HOST = "0.0.0.0"
PORT = "5068"

USER = os.environ.get("USERNAME", 'user').lower()
I18N = os.environ.get("LANG", 'en_US').split("_")[0].lower()

console = Console()

assistant = SessionAssistant(temperature=0.0, max_tokens=500, verbose=False)



def answer_with_natural_language(query: str):
    return assistant(query)


def main():
    try:
        console.print(Markdown("### Spech Recognition Service\nYou can now speak with Assistant."))

        while True:
            source = mic.Microphone()
            query = source.transcribe(forever=False)
            del source
            if query:
                console.print(Markdown(f"{USER.capitalize()} said:\n> {query}"))
                response = answer_with_natural_language(query)
                # console.print(Markdown(f"Assistant said:\n**{response}**"))
                try:
                    asyncio.run(_say(response.split("\n"), language=f"fr-fr" if I18N == "fr" else I18N.lower(), style_wav=f"{TTS_CONFIG['tts']['speaker_wav']}", enable_interpretation=False, disable_interpretation=True))
                    sleep(0.5)
                except Exception as e:
                    print(e)

    except Exception as e:
        raise e

if __name__ == "__main__":
    main()