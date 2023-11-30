import os
import colorama
import xonsh
import builtins
import requests
import json

from requests.exceptions import RequestException
from pathlib import Path
from prompt_toolkit.formatted_text.html import HTML
from prompt_toolkit.formatted_text import FormattedText
from typing import Sequence, Tuple

from assistant.as_client import request_conversation
from assistant import history
#from assistant.environ import *
from assistant.icons import *
#from assistant.nlp import *

HEADLINE = """



     \\                _)        |                  |   
    _ \\     __|   __|  |   __|  __|   _` |  __ \\   __| 
   ___ \\  \\__ \\ \\__ \\  | \\__ \\  |    (   |  |   |  |   
 _/    _\\ ____/ ____/ _| ____/ \\__| \\__._| _|  _| \\__|                                                                           
"""

NLP_HOST, NLP_PORT = "0.0.0.0", "5068"
USER = os.environ.get("USERNAME", 'user').lower()

def centered(string_lines):
    wxh = os.get_terminal_size()
    total_width = int(wxh.lines) # XSH.env.get('WIDTH', 0)  # get_app().output.get_size().columns
    centered_string_lines = ""

    for l in string_lines.split("\n"):
        centered_string_lines += l.center(total_width) + "\n"

    return centered_string_lines

def is_in_dir(CWD, DIR):
	return os.path.commonprefix([CWD, DIR]) == DIR

def is_in_home_dir(CWD, default="~"):
	home = os.path.abspath(default)
	return is_in_dir(CWD, home)

def display_dir(CWD):
	icon = None
	if not is_in_home_dir(CWD):
		icon = FOLDERS_ICON
		dir_to_display = str(icon) + " /" + os.path.basename(CWD)
		if os.path.isdir(CWD):
			dir_to_display += "/"
		elif os.path.isfile(CWD):
			icon = FILE_ICON
			dir_to_display = str(icon) + "  " + os.path.basename(CWD)
	else:
		icon = HOME_ICON
		dir_to_display = str(icon + " ")
	return dir_to_display

def display_parent_dir(CWD):
	if is_in_home_dir(CWD):
		name = display_dir(CWD)
	else:
		cwp = os.path.dirname(CWD)
		name = display_dir(cwp)
	return name

def get_highlighted_text(
    string: str,
    include_intervals: Sequence[Tuple[int, int]],
    included_exscape = colorama.Fore.BLUE,
    excluded_exscape = colorama.Fore.RESET,
    ending_escape = colorama.Fore.RESET
) -> str:
    """Applies ANSI escape values to highlight text inside certain intervals.
    Args:
        string: The string we wish created a highlighted version of
        include_intervals: A list of (start, end) intervals. Things in the
            interval will be highlighted. For example [(1, 4), (7, 10)] would
            highlight characters [1, 4) and [7, 10)
        included_exscape: The chars to add when starting somethign that is
            in the intervals
        excluded_exscape: The chars to add when starting something outside
            the intervals
        ending_escape: The escape to apply at the end of the string so that way
            the style of the last character won't bleed through
    """
    cur_ind = 0
    out_str_builder = []
    for i, (start, end) in enumerate(include_intervals):
        if start != 0:
            out_str_builder.append(excluded_exscape)
        out_str_builder.append(string[cur_ind:start])
        out_str_builder.append(included_exscape)
        out_str_builder.append(string[start:end])
        cur_ind = end
    if cur_ind != len(string):
        out_str_builder.append(excluded_exscape)
        out_str_builder.append(string[cur_ind:len(string)])
    out_str_builder.append(ending_escape)
    return "".join(out_str_builder)


def get_only_text_in_intervals(
    string: str,
    include_intervals: Sequence[Tuple[int, int]],
    exclude_filler = " "
) -> str:
    """Gets only the parts of string in intervals adding in filler for parts
    not in the intervals
    Args:
        string: The string we wish pull out the parts in the interval
        include_intervals: A list of (start, end) intervals.
        exclude_filler: The char to fill in for parts not in the interval
    """
    cur_ind = 0
    out_str_builder = []
    for i, (start, end) in enumerate(include_intervals):
        out_str_builder.append(exclude_filler * (start - cur_ind))
        out_str_builder.append(string[start:end])
        cur_ind = end
    if cur_ind != len(string):
        out_str_builder.append(exclude_filler * (len(string) - cur_ind))
    return "".join(out_str_builder)

def get_ftext_banner():
    banner = "\n".join(centered("<orange>" + HEADLINE + "</orange>").split("\n"))
    
    stext = banner + "\n"
    
    return HTML(stext)

def get_ftext_conversation():
	# request conversation for user
	user = os.environ.get("USERNAME", 'user').lower()
	ftext_banner = [("class:agent_color", f"{h}\n") for h in HEADLINE.split("\n")]
	data, text = request_conversation(user)

	# format to string
	if data:
		conversations = data.get('conversation', [])
		n = 0
		text_array = ftext_banner
		if conversations:
			for c in conversations:
				m = c.get('message', None)
				if m and m not in [" ", "  ", "  ", "\n", "\n\n", "\t"] and len(m) > 1 and type(m) == str:
					s = f"{str(m)}\n"
					n+=len(s.split("\n")) - 1
					if c.get('messenger', None) in ['user', user]:
						text_array.append(("class:user_color", s))
					else:
						text_array.append(("class:agent_color", s))
		# return list of html formatted string
		return FormattedText(text_array), n - 1
	return HTML(text), len(text.split("\n"))