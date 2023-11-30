from asyncio import Future, ensure_future
from prompt_toolkit.formatted_text import AnyFormattedText
from typing import Any, Callable, List, Optional, Tuple, TypeVar
from prompt_toolkit.widgets import Button, Dialog, Label, TextArea, RadioList
from prompt_toolkit.layout.containers import HSplit, Float
from prompt_toolkit.layout.dimension import D

_T = TypeVar("_T")

class TextInputDialog:
	def __init__(self, title="", label_text="", completer=None):
		self.future = Future()

		def accept_text(buf):
			get_app().layout.focus(ok_button)
			buf.complete_state = None
			return True

		def accept():
			self.future.set_result(self.text_area.text)

		def cancel():
			self.future.set_result(None)

		self.text_area = TextArea(
			completer=completer,
			multiline=False,
			width=D(preferred=40),
			accept_handler=accept_text,
			password=True
		)

		ok_button = Button(text="OK", handler=accept)
		cancel_button = Button(text="Cancel", handler=cancel)

		self.dialog = Dialog(
			title=title,
			body=HSplit([Label(text=label_text), self.text_area]),
			buttons=[cancel_button, ok_button],
			width=D(preferred=80),
			modal=True,
		)

	def __pt_container__(self):
		return self.dialog


class RatioListDialog:
	def __init__(self, title: AnyFormattedText = "", text: AnyFormattedText = "", values: Optional[List[Tuple[_T, AnyFormattedText]]] = None):

		self.future = Future()

		if values is None:
			values = []

		self.radio_list = RadioList(values)
		self.radio_list.open_character = "["
		self.radio_list.close_character = "]"

		def set_done():
			self.future.set_result(self.radio_list.current_value)

		ok_button = Button(text="OK", handler=(lambda: set_done()))
		cancel_button = Button(text="Close", handler=(lambda: set_done()))

		self.dialog = Dialog(
			title=title,
			body=HSplit([Label(text=text, dont_extend_height=True),
						self.radio_list], padding=1),
			buttons=[cancel_button, ok_button],
			width=D(preferred=80),
			modal=True
		)

	def __pt_container__(self):
		return self.dialog


class MessageDialog:
	def __init__(self, title, text):
		self.future = Future()

		def set_done():
			self.future.set_result(None)

		ok_button = Button(text="OK", handler=(lambda: set_done()))

		self.dialog = Dialog(
			title=title,
			body=HSplit([Label(text=text)]),
			buttons=[ok_button],
			width=D(preferred=80),
			modal=True,
		)

	def __pt_container__(self):
		return self.dialog

class ConfirmDialog:
	def __init__(self, title, text, yes="Yes", no="No"):
		self.future = Future()

		def set_yes():
			self.future.set_result(True)

		def set_no():
			self.future.set_result(False)

		yes_button = Button(text=yes, handler=set_yes)
		no_button = Button(text=no, handler=set_no)

		self.dialog = Dialog(
			title=title,
			body=HSplit([Label(text=text)]),
			buttons=[no_button, yes_button],
			width=D(preferred=80),
			modal=True,
		)

	def __pt_container__(self):
		return self.dialog
