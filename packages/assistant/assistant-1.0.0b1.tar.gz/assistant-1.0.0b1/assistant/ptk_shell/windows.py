import random
import xonsh

from pathlib import Path
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl

from prompt_toolkit.layout.scrollable_pane import ScrollablePane
from prompt_toolkit.layout.containers import Window, HSplit
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import CompleteStyle

from xonsh.built_ins import XSH

#from assistant.completer import word_completer
from assistant.ptk_shell.strformat_utils import get_ftext_conversation, centered
from assistant.icons import *
#from assistant.environ import *
#from assistant.conditions import is_nlp_server_up
#from assistant import history 

def get_buffer_window(buff):
	return ScrollablePane(
		Window(
			BufferControl(
				buffer=buff
			),
			dont_extend_height=True,
			height=1,
			style="class:right",
			wrap_lines=True,
		),
		height=1,
		show_scrollbar=False
	)

def get_inner_scrollable_content(status_bar, buffer_window):
	ftext_conversation, row_position = get_ftext_conversation()
	#return HSplit(ftext_conversation)
	return HSplit([
				Window(FormattedTextControl(text=ftext_conversation, focusable=False, show_cursor=False), wrap_lines=True),
				status_bar,
				buffer_window
			])

def get_scrollable_content(inner_scrollable_content):
	return ScrollablePane(
		inner_scrollable_content,
	)

def get_tip(is_nlp, is_listen) -> str:
	if is_nlp and is_listen:
		listening = random.choice(["You can speak now", "I'm listening.", "I'm listening ..", "I'm listening ..."])
		tip = [("class:grey", f"{listening}")]
	elif is_nlp:
		typeing = random.choice(["You can type something", "You can type with your keyboard.", "You can type now.", "You can type now ..", "You can type now ..."])
		tip = [("class:grey", typeing)]
	elif not is_nlp:
		waiting = random.choice(["Please wait", "Please wait for NLP models to load.", "NLP models are loading ..", "NLP models are loading ..."])
		tip = [("class:grey", waiting)]
	
	return tip


def get_statusbar(is_nlp, is_listen, is_speak):
	SB_KEYBOARD_ICON = ("class:orange", KEYBOARD_ICON_ACTIVE) if is_nlp else ("class:grey", KEYBOARD_ICON)
	SB_MIC_ICON = ("class:orange", MIC_ICON_ACTIVE) if is_listen else ("class:grey", MIC_ICON)
	SB_SPEAK_ICON = ("class:orange", SPEAK_ICON_ACTIVE) if is_speak else ("class:grey", SPEAK_ICON)
	SPACE = ("class:grey", "  ")
	tip = get_tip(is_nlp, is_listen)
	_sb = [SB_KEYBOARD_ICON, SPACE, SB_MIC_ICON, SPACE, SB_SPEAK_ICON, ("class:grey", " | ")] + tip
	return FormattedText(_sb)

def get_status_bar(is_nlp, is_listen, is_speak):
	return Window(
		FormattedTextControl(
			text=get_statusbar(is_nlp, is_listen, is_speak)
		),
		height=1
	)

def get_body(scrollable_content):
	return HSplit(
			[
				scrollable_content,
				Window(FormattedTextControl(text=centered("[Tab] to open menu | [Ctrl] + [Q] or [C] to quit")), height=1, style="bg:#FF7600 #000000")
			],
		)