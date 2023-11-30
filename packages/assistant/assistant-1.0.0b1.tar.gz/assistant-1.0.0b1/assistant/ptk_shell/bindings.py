from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous

# Global key bindings.
bindings = KeyBindings()
bindings.add("tab")(focus_next)
bindings.add("s-tab")(focus_previous)


@bindings.add("c-a")
def _(event):
	"Focus menu."
	event.app.layout.focus(event.app.layout.container)


# @bindings.add("c-c")
# @bindings.add("c-q")
# def _(event):
# 	"Quit when [Control] + ([Q] or [C]) is pressed."
# 	#PROC.kill()
# 	event.app.exit()


@bindings.add('escape')
def _(event):
	"Focus text input buffer on esc"
	focus_previous(event)

@bindings.add('c-s')
def _(event):
	"Toggle TTS"
	event.app.do_toggle_speak()

@bindings.add('c-l')
def _(event):
	"Toggle STT"
	event.app.do_toggle_listen()

# @bindings.add('space')
# def _(event):
#    " Reset selection. "
#    event.current_buffer.start_selection()


