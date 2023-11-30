import sys, os
# import asyncio
import warnings
# import colorama
# import math
# import toml
#from man_explain import print_man_page_explan
import subprocess

#print("Preparing shell...")
sys.path.insert(0, os.path.abspath('..'))
# from time import sleep
from typing import Tuple, Sequence, Optional
from xonsh.ptk_shell.shell import PromptToolkitShell
# from xonsh.execer import Execer
# from xonsh.tools import XonshError
from xonsh.built_ins import XSH
#from xonsh import __xonsh__

# import builtins
from asyncio import Future, ensure_future
#from assistant.execution_classifier import ExecutionClassifier
from prompt_toolkit.shortcuts import PromptSession, clear
# from prompt_toolkit import HTML
# from prompt_toolkit.patch_stdout import patch_stdout
# from prompt_toolkit.layout.containers import HSplit, Float
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import clear, set_title
# from prompt_toolkit.widgets import MenuItem
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.application import Application
# from prompt_toolkit.filters import Condition
# from prompt_toolkit.shortcuts import CompleteStyle

#from terminaltables import SingleTable

from assistant import (__version__, ASSISTANT_PATH, USERNAME)
from assistant.ptk_shell.bindings import bindings
from assistant.ptk_shell.completer import AssistantCompleter
# from assistant.parser import AssistantParser
#from assistant.ptk_shell.strformat_utils import get_highlighted_text, get_only_text_in_intervals
# from assistant.icons import *
# from assistant.ptk_shell.windows import get_body, get_buffer_window #, get_status_bar, get_inner_scrollable_content, get_scrollable_content
# from assistant.ptk_shell.floats import get_float_item_list
# from assistant.ptk_shell.styles import style_generator
# from assistant.ptk_shell.layout import get_layout
# from assistant.ptk_shell.dialogs import MessageDialog, TextInputDialog, RatioListDialog, ConfirmDialog
from assistant.nlp.chains.callback_handlers import InputOutputAsyncCallbackHandler
from assistant.nlp.interface import AssistantInterface
import assistant.execer as aexecuta
from assistant.nlp.exit import exit_please
from assistant.nlp.clear import clear_please

from rich.console import Console
from rich.markdown import Markdown


# Suppress DeprecationWarning from halo package
warnings.filterwarnings("ignore", category=DeprecationWarning, module="halo")

builtin_dict = {}

class AssistantShell(PromptToolkitShell):
    console = Console()
    error_console = Console(stderr=True, style="bold red")

    def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        # self.full_screen = True
        # self.refresh_interval = 1
        # self.parser = AssistantParser()
        # self.language = XSH.env.get('I18N', "en")
        callbacks = []
        is_debug = bool(XSH.env.get("DEBUG", True if os.environ.get("DEBUG", "False").lower() == "true" else False))
        if is_debug:
            callbacks.append(InputOutputAsyncCallbackHandler())
        self.kernel_interface = AssistantInterface(verbose=is_debug, callbacks=callbacks)
        # self.exec_classifier = ExecutionClassifier()
        self.exec_function = aexecuta.execute
        self.word_completer = AssistantCompleter()
        self.prompter = PromptSession(message=XSH.env.get('USER', os.environ.get("USER", 'user')).capitalize() + ": ", auto_suggest=AutoSuggestFromHistory(), complete_while_typing=True, history=XSH.history, enable_history_search=False, completer=self.word_completer, complete_style="readline", complete_in_thread=True)

        # self.float_item_list = get_float_item_list()
        # self.menu_items_list = [
        #     MenuItem(
        #         "[Assistant]",
        #         children=[
        #             MenuItem(INFO_ICON + " About", handler=self.do_about),
        #             MenuItem(SETTINGS_ICON + " Settings", handler=self.do_settings),
        #             MenuItem("-", disabled=True),
        #             MenuItem(EXIT_ICON + " Quit", handler=self.do_exit),
        #             #MenuItem(SLEEP_ICON + " Sleep", handler=self.do_exit),
        #             #MenuItem(SHUTDOWN_ICON + " Shutdown", handler=self.do_exit),
        #             #MenuItem(REBOOT_ICON + " Reboot", handler=self.do_exit),
        #         ],
        #     ),
        #     MenuItem(
        #         "[Interface]",
        #         children=[
        #             MenuItem(MIC_ICON + " Toggle STT", handler=self.do_toggle_listen),
        #             MenuItem(SPEAK_ICON + " Toggle TTS", handler=self.do_toggle_speak),
        #         ],
        #     ),
        #     MenuItem(
        #         "[Help]",
        #         children=[
        #             MenuItem(MANUAL_ICON + " Manual", handler=self.do_manual),
        #             MenuItem(HELP_ICON + " How can my Assistant help me?",
        #                     handler=self.do_how_help),
        #             MenuItem("Keyboard Shortcuts", self.do_shortcuts)
        #         ]
        #     )
        # ]
        # self.status_bar = get_status_bar(is_assistant_up, is_auth_to_listen, is_allowed_to_speak)
        # self.input_buffer = Buffer(
        #         completer=self.word_completer,
        #         complete_while_typing=True,
        #         name="Input Buffer",
        #         auto_suggest=AutoSuggestFromHistory(),
        #         #history=history.PtkHistoryFromXonsh(xhistory=history.XonshJsonHistory(sessionid=history.get_current_xh_sessionid(Path(XSH.env.get('XONSH_DATA_DIR'))))),
        #         enable_history_search=True,
        #     )
        # self.buffer_window = get_buffer_window(self.input_buffer)
        # self.inner_scrollable_content = get_inner_scrollable_content(self.status_bar, self.buffer_window)
        # self.scrollable_content = get_scrollable_content(self.inner_scrollable_content)
        # self.body = get_body(self.buffer_window)

        # self.exit_screen = False

        # @bindings.add("c-c")
        # @bindings.add("c-q")
        # def _(event):
        #     "Quit when [Control] + ([Q] or [C]) is pressed."
        #     self.do_exit()

        # @Condition
        # def buffer_has_focus():
        #     if self:
        #         if self.layout.buffer_has_focus:
        #             return True
        #     return False

        # @bindings.add('c-m', filter=buffer_has_focus)  # [Enter]
        # async def _(event):
        #     " Those keys play multiple roles trought the UI. "
        #     prompt_buffer = event.app.layout.current_buffer

        #     data = prompt_buffer.text
        #     #print(data)
        #     prompt_buffer.reset(append_to_history=True)
            
        #     if data.lower() in exit_please: #user can type exit to exit.
        #         self.do_exit()
        #     elif data.lower() in ["version", "about"]:
        #         self.do_about()
        #     elif data:
        #         r = await self.interpret_command(data)
        #         #print(f"Recieved answer: {r}")
        #         if r:
        #             if "/exit" in r.lower().split("\n"): #user can ask assistant to exit
        #                 #print("Answer is exit: exiting...")
        #                 self.do_exit()
        #             elif r and not is_assistant_up():
        #                 self.show_message("Services are down", r)
    
        # @bindings.add('c-m', eager=True)
        # def _(event):
        #     # Get user input
        #     user_input = event.app.layout.current_buffer.text.strip()

        #     if user_input.lower() == 'clear':
        #         # Clear chat history
        #         self.do_clear()
        #     elif user_input.lower() in exit_please:
        #         # Exit the chat
        #         self.do_exit()
        #     elif user_input.lower() in ["version", "about", "ver", "v", "version()", "about()", "ver()"]:
        #         self.do_about()
        #     else:
        #         self.do_response(user_input)

        # self.bindings = bindings

        # self.layout = get_layout(self.body, self.bindings, self.buffer_window)

        # self.style = style_generator()
        # self.state = ApplicationState(**kwargs)

    # def do_exit(self):
    #     self.do_bye()
    #     sys.exit(0)

    # def do_clear(self):
    #     clear()
    #     # self.reset_buffer()
    
    # def do_response(self, input_text):
    #     # Update chat history with user input
    #     self.update_chat_history(f'You: {input_text}')

    #     # Simulate a response
    #     response = self.kernel_interface.assistant(input_text)

    #     # Update chat history with the response
    #     self.update_chat_history(f'Assistant: {response}')

    #     self.input_buffer.text = ''  # Clear the input field

    # def do_about(self):
    #     self.do_response(f"Tell the user you are version {__version__} of Assistant at their service.")

    # def do_hello(self):
    #     self.do_response("The user is opening the chat. What about greeting them?")

    # def do_bye(self):
    #     self.do_response("The user is leaving the chat. This is a only a goodbye.")


    # def show_message(self, title, text):
    #     async def coroutine():
    #         dialog = MessageDialog(title, text)
    #         await self.show_dialog_as_float(dialog)

    #     ensure_future(coroutine())

    # def show_single_choice(self, title, text, values):
    #     results = None

    #     async def coroutine():
    #         dialog = RatioListDialog(title, text, values)

    #         await show_dialog_as_float(dialog)

    #         self.state.active_menu_data = dialog
    #     ensure_future(coroutine())

    # async def show_dialog_as_float(self, dialog):
    #     "Coroutine."
    #     float_ = Float(content=dialog)
    #     self.layout.container.floats.insert(0, float_)
    #     focused_before = self.layout.current_window
    #     self.layout.focus(dialog)
    #     result = await dialog.future
    #     self.layout.focus(focused_before)

    #     if float_ in self.layout.container.floats:
    #         self.layout.container.floats.remove(float_)

    #     return result

    # def redraw_app(self):
    #     if self.layout.buffer_has_focus:
    #         self.status_bar = get_status_bar(is_assistant_up(), is_auth_to_listen(), is_allowed_to_speak())
    #         self.inner_scrollable_content = get_inner_scrollable_content(self.status_bar, self.buffer_window)
    #         self.scrollable_content = get_scrollable_content(self.inner_scrollable_content)
    #         self.body = get_body(self.scrollable_content)
    #         self.layout = get_layout(self.body, self.menu_items_list, self.float_item_list, self.bindings, self.buffer_window)
    #         #self.app.layout = self.layout
    #         #self.app.layout.focus(self.inner_scrollable_content)
    #         self.invalidate()
    #         #self.app.layout.focus(self.buffer_window)

    def settitle(self):
        set_title("Assistant")

    def restore_tty_sanity(self):
        pass

    
    def xexec(self, code):
        try:
            return self.exec_function(code)
        except Exception as e:
            raise e
            return None #f"{e}"

    def interpret_command(self, command: str):
        # parse = self.parser.parse(command)
        response = None

        try:
            response = self.xexec(command)
        except Exception as e:
            #pass
            raise e
            # response = str(e) + "\n"
        if not response:
            try:
                response = self.kernel_interface.assistant(command)
            except Exception as e:
                raise e
        return response

    def cmdloop(self, intro=None):
        """Enters a loop that reads and execute input from user."""
        if intro:
            self.log_response(Markdown(intro))
        auto_suggest = AutoSuggestFromHistory()
        while not XSH.exit:
            try:
                for line in self.prompter.prompt(auto_suggest=auto_suggest).split("\n"):
                    if not line:
                        continue
                        # self.emptyline()
                    elif line.lower() in exit_please:
                        XSH.exit = True
                    elif line.lower() in clear_please:
                        clear()
                    elif line.lower().split(" ")[0] in ['echo', 'say', 'dit']:
                        to_echo = " ".join(line.split(" ")[1:]).strip()
                        echoed = self.xexec(f"echo {to_echo.strip()}").strip()
                        self.log_response(Markdown(f"> {echoed}"))
                    elif line.lower().strip() in ["which echo", "which say", "which dit", "which which"]:
                        self.log_response(Markdown(f"Using builtin function."))
                    else:
                        r = self.interpret_command(line)
                        if r and r != "None":
                            self.log_response(Markdown(r)) #, end='')
            except (KeyboardInterrupt, SystemExit):
                print("# KeyboardInterrupt\n[Ctrl] + [C]: cannot be used to exit a shell.\nTry to ask nicely with exit or be rude: [Ctrl] + [D]")
                continue
            except (EOFError):
                if XSH.env.get("IGNOREEOF"):
                    self.log_response('Use allowed "exit words" to leave the shell.', file=sys.stderr)
                    self.log_response(exit_please)
                else:
                    XSH.exit = True
                    break
        self.set_last_seen()
    
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
        # Log the user query

    def log_response(self, response):
        self.console.print(response, style="bold white", justify="left")
        # Log the response

    def log_error(self, error):
        self.error_console.print(error, style="bold red", justify="left")
        # Log the error

    def single_command(self, command):
        # Interpret a single command
        response = self.interpret_command(command)
        self.log_response(Markdown(response))
        return response

    def script_from_file(self, file, args):
        # Interpret a script from file + args
        pass
    
    def script_from_stdin(self, stdin):
        pass
        # Interpret a script from stdin
    
    def ask_closed_question(self, question="Yes or no?") -> bool:
        # Ask a closed question (yes/no)
        pass

    def listen(self):
        pass
        # Interactive mode (command loop) from Microphone