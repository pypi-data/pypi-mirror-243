from prompt_toolkit.styles import Style

def style_generator():

    style = {
		"window.border": "#FF7600",
		"menu-bar": "bg:#FF7600 #000000",
		"menu-bar.selected-item": "bg:#FFA900 #000000",
		"menu": "bg:#FF7600 #000000",
		"menu.border": "#aaaaaa",
		"window.border shadow": "#52006A",
		"focused  button": "bg:#52006A #FFA900 noinherit",
		# Styling for Dialog widgets.
		"button-bar": "bg:#52006A",
		"status": "bg:#FF7600",
		"shadow": "bg:#52006A",
		'dialog': 'bg:#52006A',
		'dialog frame.label': 'bg:#FF7600 #000000',
		'dialog.body':  'bg:#FF7600 #000000',
		'dialog shadow': 'bg:#52006A',
		'user_color': "#aaaaaa",
		'agent_color': "#FF7600",
	}

    return Style.from_dict(style)