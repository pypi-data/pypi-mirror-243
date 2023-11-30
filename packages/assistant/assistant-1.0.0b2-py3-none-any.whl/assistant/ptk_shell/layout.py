from prompt_toolkit.layout.layout import Layout

def get_layout(body, bindings, buffer_window):
	return Layout(container=body)#, key_bindings=bindings)
