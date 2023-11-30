import attr
import requests
import random
import threading

from xonsh.built_ins import XSH

from halo import Halo

from assistant.nlp.chains.session import SessionAssistant
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.nlp.think import let_me_think_about_it, sorry_unable_to_think

class ModernHalo(Halo):
    def start(self, text=None):
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """
        if text is not None:
            self.text = text
        if self._spinner_id is not None:
            return self
        if not (self.enabled and self._check_stream()):
            return self
        self._hide_cursor()

        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self.render)
        self._spinner_thread.set_daemon = True
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()
        return self


@attr.s(auto_attribs=True, frozen=True)
class PredictReturn:
    success: bool
    unparse: str = None
    error_message: str = None

def get_random_thinking_sentence():
    """
    Returns a random sentence to indicate that the assistant is thinking about a response.
    """
    return random.choice(let_me_think_about_it)

def get_random_sorry_sentence():
    """
    Returns a random sentence to indicate that the assistant is unable to think about a response.
    """
    return random.choice(sorry_unable_to_think)

class AssistantInterface:
    host = "localhost"
    port = "5085"
    interface = None
    models_path = None

    def __init__(self, host=host, port=port, verbose=False, callbacks=[], **kwargs):
        self.host = host
        self.port = port
        self.spinner = ModernHalo(spinner="dots13", text="...", color="cyan")
        self.set_assistant(verbose=verbose, callbacks=callbacks)

    def set_assistant(self, verbose=False, callbacks=[]):
        self.session_assistant = SessionAssistant(
            temperature=0.0, max_tokens=1000, verbose=verbose, callbacks=callbacks
        )  # , callbacks=[InputOutputAsyncCallbackHandler()])

    def is_nlp_server_up(self):
        try:
            r = requests.get(f"http://{self.host}:{self.port}")
            if r.status_code == 200:
                return True
            else:
                raise Exception("NLP Server is not up.")
        except (requests.ConnectionError, Exception) as e:
            return False

    def assistant(self, query):
        try:
            if self.is_nlp_server_up():
                self.spinner.text = f"{get_random_thinking_sentence()}..."
                self.spinner.start()
                return self.session_assistant(query)
            else:
                return None
        except requests.exceptions.ConnectionError:
            return None
        finally:
            self.spinner.stop()

    def get_intro(self, prompt_into = "Assistant?"):
        """
        Returns the introduction prompt for the assistant.

        Returns:
        str: The introduction prompt for the assistant.
        """
        
        return (
            self.assistant(prompt_into)
            or get_random_sorry_sentence()
        )
