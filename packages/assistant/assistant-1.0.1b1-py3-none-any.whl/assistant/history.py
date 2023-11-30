import pickle
from pathlib import Path
from datetime import datetime
from xonsh.history.json import JsonHistory
from prompt_toolkit.history import History
from typing import Iterable, List, Optional, Sequence, Tuple

from assistant.time import now
#from assistant.environ import *

def latest_file(path: Path, pattern: str = "*"):
    files = path.glob(pattern)
    return max(files, key=lambda x: x.stat().st_ctime)

def get_current_xh_sessionid(xonsh_data_dir: Path, number_of_minutes_afterwhich_the_last_conversation_is_no_longer_the_current_one_anymore=3):
	sessionid=None

	lastest_session_file_created = latest_file(Path(f'{xonsh_data_dir}/history_json/'), 'xonsh-*.json')

	if ((now() - datetime.fromtimestamp(lastest_session_file_created.stat().st_mtime)).total_seconds() / 60.0) < number_of_minutes_afterwhich_the_last_conversation_is_no_longer_the_current_one_anymore:
		sessionid = lastest_session_file_created.as_posix().split("/")[-1].replace("xonsh-", "").replace(".json", "")

	return sessionid

class XonshJsonHistory(JsonHistory):
	"""Xonsh history backend implemented with JSON files.

    JsonHistory implements an extra action: ``diff``
    """

	pass
	

	# history = None
	# history_path = None

	# number_of_minutes_afterwhich_the_last_conversation_is_no_longer_the_current_one_anymore = 3

	# def __init__(self, history_path):
	# 	self.history_path = history_path
	# 	self.history = self.load()

	# def load(self):
	# 	try:
	# 		with open(self.history_path, 'rb') as f:
	# 			self.history = pickle.load(f)
	# 			f.close()
	# 			return self.history
	# 	except Exception as e:
	# 		return []

	# def dump(self):
	# 	with open(self.history_path, 'wb') as f:
	# 		pickle.dump(self.history, f)
	# 		f.close()
	# 	return self.history

	# def save_conversation(self, conversation, is_created=True):
	# 	if is_created:
	# 		self.history.append(conversation)
	# 	else:
	# 		self.history[-1] = conversation
	# 	self.dump()
	# 	return conversation


	# def journalize(self, utterance, timestamp=None, character="assistant", context=None):
	# 	try:
	# 		if timestamp == None:
	# 			timestamp = now()

	# 		journal_entry = {
	# 			'timestamp': timestamp,
	# 			'utterance': utterance,
	# 			'character': character,
	# 			'context': context
	# 		}

	# 		if not self.history:
	# 			self.load()  # [ #this is a list of all conversations
			
	# 		current_conversation, is_conv_created = self.get_current_conversation()  # [ #this is a list of utterances inside a conversation
	# 		current_conversation.append(journal_entry)
	# 		#CONV.append(journal_entry)
	# 		self.save_conversation(current_conversation, is_created=is_conv_created)
	# 	except Exception as e:
	# 		print("Error in journalize")
	# 		raise(e)



class PtkHistoryFromXonsh(History):
    """
    :class:`.History` class that loads a list of all strings from xonsh history.
    In order to prepopulate the history, it's possible to call either
    `append_string` for all items or pass a list of strings to `__init__` here.
    """

    def __init__(self, xhistory: Optional[XonshJsonHistory] = None) -> None:
        super().__init__()
        # Emulating disk storage.
        if xhistory is None:
            self._storage = []
        else:
            self._storage = list(xhistory.inps) if xhistory.inps else []

    def load_history_strings(self) -> Iterable[str]:
        yield from self._storage[::-1]

    def store_string(self, string: str) -> None:
        pass #self._storage.append(string) # no need to store strings since we import saved commands from xonsh history
		# we could prehaps reload the history data