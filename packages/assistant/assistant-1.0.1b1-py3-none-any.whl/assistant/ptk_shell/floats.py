from prompt_toolkit.layout.containers import Float
from prompt_toolkit.layout.menus import CompletionsMenu

def get_float_item_list():
	return [
		Float(
			xcursor=True,
			ycursor=True,
			content=CompletionsMenu(max_height=3, scroll_offset=1),
		),
	]