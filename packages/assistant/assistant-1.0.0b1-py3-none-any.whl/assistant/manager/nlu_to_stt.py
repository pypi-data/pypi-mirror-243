try:
	from listen import mic
	from listen.STT import utils
except ImportError as e:
	explanation="""
	Install listen using pip:\n
	pip install git+https://gitlab.com/waser-technologies/technologies/pyaudio.git git+https://gitlab.com/waser-technologies/technologies/listen.git\n
	And start the server and wait for the models to load.
	python -m listen.STT.as_service
	You can now retry once you have given access to your microphone.
	"""
	raise ImportError(explanation)

from asyncio.tasks import wait
import os, glob
import sys
import pickle
import yaml
import toml
import json
import csv
import subprocess #psutil
import time
import re
import random
import requests

from pathlib import Path
from halo import Halo
from tqdm import tqdm
from prompt_toolkit.shortcuts import clear, radiolist_dialog, set_title, yes_no_dialog
from prompt_toolkit.styles import Style
#from prompt_toolkit.formatted_text.html import HTML
from pydub import AudioSegment
from pydub.playback import play
from assistant.manager.nlu import (
 	HOME, TRAINER_PATH, I18N, USERNAME,
 	_format_for_training,
	load_intents,
	load_verified_intents_examples,
	set_verified_intents_examples,
	upload_verified_answers,
	load_domains_lm,
	load_transcribed_intents_examples,
	set_transcribed_intents_examples,
	set_domains_lm,
)

STT_SETTINGS_PATH = utils.CONFIG_PATH 
STT_SETTINGS = utils.get_config_or_default()

STYLE = Style.from_dict(
	{
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
	}
)

def wait_till_ready_to_speak(text: str):
	v = radiolist_dialog(
		values=[
			("rec", "Start recording"),
			("next", "Next utterance"),
		],
		title="Manager:Assistant:Export:STT",
		text=f"Say: {text}",
		cancel_text="Quit",
		ok_text="Confirm",
		style=STYLE
	).run()
	print(f"{USERNAME}: {v if v else 'Quit -> Manager:Assistant:Export:STT'}")

	if not v:
		sys.exit(1)

	return v


def is_sentence_admissible_for_stt_training(sentence: str):
	explanation = """
Explanation:
    Determine if the above sentence can be used for training.
    Conditions for rejecting this sentence:
    -    [] Ortograph is incorrect
    -    [] Grammar is incorrect
    -    [] Syntax is incorrect
    -    [] You fear this sentence will hinder training results
    -    [] This sentence does not meet the requirements to be used for training
    If one of those is true, reject this sentence.
    Conditions for this sentence to be used for training:
    -    [] Must not meet any condition to be rejectable
    -    [] Must be pronounceable
    -    [] You agree it could be used either:
            -    in written form in the language model,
            -    or as a transcription of speech in the test set
    All of the above condition must be true for this sentence to be admissible for training.
    Otherwise reject the sentence."""
	v = radiolist_dialog(
		values=[
			("reject", "Flag for rejection"),
			("accept", "Accept for training"),
		],
		title="Manager:Assistant:Export:STT",
		text=f"Sentence: {sentence} {explanation}",
		cancel_text="Quit",
		ok_text="Confirm",
		style=STYLE
	).run()
	print(f"{USERNAME}: {v if v else 'Quit -> Manager:Assistant:Export:STT'}")

	if not v:
		sys.exit(1)

	return v

def user_wants_verified_from_answers():
	return yes_no_dialog(
			"Manager:Assistant:Export:STT ? Data Import",
			"Assistant: Do you want to import sentences from our repo of most verified sentences?\n\n{i}: It seams you have not verified any sentence yet.\n   : Importing your jumpstart data is a good idea to spend less time validating sentences.\n\n\n{i}: Checkout the ~/.trainer/helpers directory to see availible data.",
			yes_text="Allow",
			no_text="Deny",
			style=STYLE
		).run()

def user_wants_to_share_reviews():
	return not yes_no_dialog(
			"Manager:Assistant:Export:STT ? Data Export",
			"Assistant: Do you want to share the sentences you verified to our repo?\n\n{i}: It can make it easier next time.\n   : Exporting your data is a good idea to spend less time validating sentences.\n\n\n<a>: https://github.com/wasertech/verified_sentences_stt",
			yes_text="Deny",
			no_text="Allow",
			style=STYLE
		).run()

def set_is_speech_recognition_enabled(is_speech_recognition_enabled: bool):
	fr = open(STT_SETTINGS_PATH, 'r')
	STT_SETTINGS = toml.load(fr)
	fr.close()

	STT_SETTINGS['stt']['is_allowed'] = is_speech_recognition_enabled

	fw = open(STT_SETTINGS_PATH, 'w')
	toml.dump(STT_SETTINGS, fw)
	fw.close()

def get_latest_wav(wpd):
	wav_files = glob.glob(f"{wpd}/*.wav")
	latest_wav_file = max(wav_files, key=os.path.getctime)
	return latest_wav_file

def play_wav(wav_file_path):
	_wav = AudioSegment.from_wav(file=wav_file_path)
	play(_wav)

def record_wav(txt_to_rec):
	print(f"{USERNAME}: Record Example -> Manager:Assistant:Export:STT")
	sr_path = f"{TRAINER_PATH}/STT/extracted/{I18N}/data/Assistant"
	_last_modified = os.path.getmtime(sr_path)
	last_modified = _last_modified
	set_is_speech_recognition_enabled(True)
	print("Start Listening -> Manager:Assistant:Export:STT")
	source = mic.Microphone(save_wav=sr_path)
	print("\n")
	print(f"Say: '{txt_to_rec}' now.")
	transcription = source.transcribe()
	while last_modified == _last_modified:
		last_modified = os.path.getmtime(sr_path)
	set_is_speech_recognition_enabled(False)
	last_wav_path = get_latest_wav(sr_path)
	return last_wav_path

def is_speech_correct(wav_path, transcript):
	print(f"Manager:Assistant:Export:STT ? \'{transcript}\'")
	v = radiolist_dialog(
		values=[
			("play", "Replay audio"),
			("accept", "Accept audio & Save transcription"),
			("rec", "Discard & Record again"),
		],
		title=f"Manager:Assistant:Export:STT ? '{transcript}'",
		text=f"Speech path: {wav_path}\n\nTranscript: {transcript}\n\n\n(?): Does the recorded audio match the transcription?\n\n\nAssistant: What would you like to do?",
		cancel_text="Quit",
		ok_text="Decide",
		style=STYLE
	).run()
	print(f"{USERNAME}: {v.capitalize() if v else 'Quit'} -> Manager:Assistant:Export:STT")

	if not v:
		sys.exit(1)

	return v

def get_file_byte_size(file):
	stat_cmd = ["stat", "-c%s", file]
	p = subprocess.Popen(stat_cmd, stdout=subprocess.PIPE)
	r = p.communicate()
	if r[1] == None: # no errors
		return r[0].decode('UTF8', 'ignore').replace("\n", "")
	#stat -c%s "$f"

def create_csv(csv_path, header=None):
	with open(csv_path,'w') as fd:
		writer = csv.writer(fd)
		
		if not header:
			row = []
		else:
			row = header
		
		writer.writerow(row)
		fd.close()

def update_csv(csv_path, audio_path, transcription):
	size = get_file_byte_size(audio_path)
	with open(csv_path,'a') as fd:
		row = [str(audio_path.split("/")[-1]), size, transcription]
		writer = csv.writer(fd)
		writer.writerow(row)
		fd.close()

def save_transcription(transcription, wav_path, skip=False):
	sr_path = f"{TRAINER_PATH}/STT/extracted/{I18N}/data/Assistant"
	if not skip:
		if not os.path.exists(f"{sr_path}/train_test.csv"):
			create_csv(csv_path, header=["wav_filename","wav_filesize","transcript"])
		update_csv(f"{sr_path}/train_test.csv", wav_path, transcription)
	# save in pickle
	transcribed_intents_examples = load_transcribed_intents_examples()
	tie_lang = transcribed_intents_examples.get(I18N, {})
	if not tie_lang:
		transcribed_intents_examples[f'{I18N}'] = {}
	if not tie_lang.get(f'{transcription}', False):
		transcribed_intents_examples[f'{I18N}'][f'{transcription}'] = wav_path
	set_transcribed_intents_examples(transcribed_intents_examples)

def save_verification(transcript, reject=False):
	accepted = not reject
	verified_intents_examples = load_verified_intents_examples()
	if not verified_intents_examples.get(I18N):
		verified_intents_examples[f'{I18N}'] = {}
	verified_intents_examples[f'{I18N}'][f'{transcript}'] = accepted
	set_verified_intents_examples(verified_intents_examples)

def verify_intents_examples():
	intents = load_intents()

	verified_intents_examples = load_verified_intents_examples(from_reviews=True)

	for i in intents:
		i = _format_for_training(i)
		if len(i) >= 2 and verified_intents_examples.get(I18N, {}).get(i, None) == None:
			print(f"Manager:Assistant:Export:STT ? \'{i}\'")
			kp = is_sentence_admissible_for_stt_training(i)
			if kp:
				c = str(kp)
				if c == 'accept':
					save_verification(i)
					print(f"Transcript Saved -> Manager:Assistant:Export:STT")
				elif c == 'reject':
					save_verification(i, reject=True)
					print(f"{USERNAME}: Reject Sentence -> Manager:Assistant:Export:STT")
				else:
					return "Interpution -> Manager:Assistant:Export:STT"
			else:
				return "Interpution -> Manager:Assistant:Export:STT"
		elif not i:
			pass #print(f"Manager:Assistant:Export:STT -> intent is invalid because null ")
		elif verified_intents_examples.get(I18N, {}).get(i, None) != None:
			#print(f"Manager:Assistant:Export:STT -> \'{i}\' is already verified ")
			pass
		else:
			save_verification(i, reject=True)
			print(f"Manager:Assistant:Export:STT -> \'{i}\' is invalid because too short ")

	# Share reviews?
	if user_wants_to_share_reviews():
		upload_verified_answers()
	
	return load_verified_intents_examples()

def load_expanded_intents_examples():
	vie = verify_intents_examples()
	if type(vie) == str:
		raise Exception(vie) #User exited the manager
	elif type(vie) != dict:
		raise Exception(f"Verified Intent: {vie}") # We have not recieved a complete list of verified intents examples
	
	# We have recieved a complete list of verified intents examples
	print("Manager:Assistant:Export:STT -> NLU Data Report")
	v, t = 0, 0
	for k, d in vie.get(f'{I18N}', {}).items():
		if d:
			v+=1
		else:
			t+=1
	r = float( v / (t + v) )
	print(f"Manager:Assistant:Export:STT -> Validated {v} ({str(round(r*100, ndigits=2))}%) sentences from {I18N} NLU data")
	return vie.get(f'{I18N}', {})

def get_testset_size(test_set):
	return len(test_set)

def get_lm_size(lm):
	return len(lm)

def get_dataset_statistic(test_set, lm):
	_ts = get_testset_size(test_set)
	_lm = get_lm_size(lm)
	_sum = _ts + _lm
	if _sum > 0:
		return _ts, _lm, _sum, float(_ts/_sum)
	else:
		return _ts, _lm, _sum, 0

def split_stt_data(data):
	lm = load_domains_lm()
	domains_language_model = lm.get(I18N, [])

	ts = load_transcribed_intents_examples()
	_domains_test_set = ts.get(I18N, {}) or {}
	domains_test_set = [x for x, y in _domains_test_set.items()]

	ld = len(data)
	
	assert ld > 10, "Less than 10 sentences were found to export."
	assert ld > 100, "Less than 100 sentences were found to export."

	current_ts_size = len(domains_test_set)
	current_lm_size = len(domains_language_model)

	total_sentences = domains_language_model + domains_test_set
	_data = []
	for d in data:
		if d not in domains_test_set:
			_data.append(d)
		if d not in total_sentences:
			total_sentences.append(d)
	
	total_size = len(total_sentences)

	tagret_ratio = 0.05 if total_size > 10_000 else 0.1 # 10% or 5%
	current_ratio = float( current_ts_size / int( total_size ) ) if (total_size) > 1 else 0.

	if tagret_ratio <= current_ratio:
		print("TestSet/LM ratio already reached.")
	else:
		delta_ratio = float(tagret_ratio - current_ratio)
		k = int(delta_ratio * total_size)

		assert k < len(_data), f"{k=} is bigger than availibe amount of data ({len(_data)})"

		if k > 1:
			domains_test_set.extend(random.choices(_data, k=k))
		else:
			print("Nothing to record.")
	
	for item in data:
		# its important to make sure that 
		# test set and lm have no data in common
		if item not in domains_test_set and item not in domains_language_model:
			domains_language_model.append(item)
	
	return (domains_language_model, domains_test_set)

def is_sentence_already_recorded(sentence_to_record):
	ts = load_transcribed_intents_examples()
	_domains_test_set = ts.get(I18N, {}) or {}
	domains_test_set = [x for x, y in _domains_test_set.items()]
	wfp = _domains_test_set.get(sentence_to_record)
	if wfp and os.path.isfile(wfp):
		return True
	else:
		return False

def record_testset(domains_test_set):
	for sentence_to_record in domains_test_set:
		if not is_sentence_already_recorded(sentence_to_record):
			kp = wait_till_ready_to_speak(sentence_to_record)
			if kp:
				c = str(kp)
				if c == 'rec':
					while c == 'rec':
						w = record_wav(sentence_to_record)
						c = 'play'
						while c == 'play':
							if c == 'play':
								play_wav(w)
							c = is_speech_correct(w, sentence_to_record)
						if c == 'rec': # if user wants to discard recorded audio and record again
							os.remove(w)
							print(f"WavAudio Removed -> Manager:Assistant:Export:STT")
					if c == 'accept':
							save_transcription(sentence_to_record, w)
							print(f"Transcript Saved -> Manager:Assistant:Export:STT")
				elif c == 'next':
					print(f"{USERNAME}: Skip Example -> Manager:Assistant:Export:STT")
					save_transcription(sentence_to_record, "Skipped", skip=True)
				else:
					return "Interpution -> Manager:Assistant:Export:STT"
					sys.exit(1)
			else:
				return "Interpution -> Manager:Assistant:Export:STT"
				sys.exit(1)

def show_data_statistics(test_set_size, lm_size, total_data, data_ratio):
	print(f"Manager:Assistant:Export:STT -> Exported {total_data} sentences in total")
	print(f"Manager:Assistant:Export:STT -> Language Model: {lm_size} sentences ({round((1. - data_ratio)*100, ndigits=2)}%)")
	print(f"Manager:Assistant:Export:STT -> Test Set: {test_set_size} sentences ({round(data_ratio*100, ndigits=2)}%)")
	v = yes_no_dialog(
			"Manager:Assistant:Export:STT ? Record Test Set",
			f"Assistant: Are you ready to record the test set?\n\n{{i}}: You have exported {total_data} sentences in total.\n   : ({int(round((1. - data_ratio)*100, ndigits=0))}%) {lm_size} sentences for the language model.\n   : ({int(round(data_ratio*100, ndigits=0))}%) {test_set_size} sentences for the test set.\n\n\n(?): Are you ready record the test set out loud?\n\n   : -> Press [Enter] or click on 'Ready' to continue\n   : -> Otherwise click on 'Quit' or press [Tab] and [Enter] to abort.",
			yes_text="Ready",
			no_text="Quit",
			style=STYLE
		).run()
	
	if not v:
		sys.exit(1)

def export_intents_stt():
	print("Manager:Assistant:Export:STT -> Exporting intents")

	print("Manager:Assistant:Export:STT -> Preparing data")

	intent_examples = load_expanded_intents_examples()
	
	data = []
	
	for x, d in intent_examples.items():
		if d == True:
			data.append(x)
	
	domains_language_model, domains_test_set = split_stt_data(data)

	test_set_size, lm_size, total_data, data_ratio = get_dataset_statistic(domains_test_set, domains_language_model)

	show_data_statistics(test_set_size, lm_size, total_data, data_ratio)
	print(f"Manager:Assistant:Export:STT -> Language Model Data Ready for Importation")
	print(f"Manager:Assistant:Export:STT -> Prepare to record Test Set")
	print(record_testset(domains_test_set) or "You have successfully recorded your test set -> Manager:Assistant:Export:STT")
	
	lm = load_domains_lm()
	lm[f'{I18N}'] = domains_language_model
	set_domains_lm(lm)

	return "Achieved -> Manager:Assistant:Export:STT"

def load_settings():
	with open(STT_SETTINGS_PATH, 'r') as f:
		STT_SETTINGS = toml.load(f)
		f.close()
		return STT_SETTINGS

def get_is_speech_recognition_enabled():
	STT_SETTINGS = load_settings()
	if STT_SETTINGS.get('stt', False):
		return STT_SETTINGS['stt'].get('is_allowed', False)
	return False

def checkIfServiceEnabled(servicePath):
	if os.path.isfile(servicePath):
		return True
	return False

def checkIfServiceIsOK(host="localhost", port="5063"):
	try:
		r = requests.get(f'http://{host}:{port}')
		return r.ok
	except (ConnectionError, Exception) as e:
		return False

def get_speech_recognition_auth():
	# check for sr service
	is_proc = checkIfServiceEnabled(f'{HOME}/.config/systemd/user/default.target.wants/listen.service') or checkIfServiceIsOK()
	is_service = checkIfServiceIsOK()
	if not any([is_proc, is_service]):
		print("STT Services down -> Manager:Assistant:Export:STT")
		print("In order to export NLU data to STT, Manager needs access to the mic array.")
		print("Start Speech-To-Text Services using:")
		print("")
		print("[  systemctl --user enable --now listen  ]")
		print("")
		print("Or by using python in another shell session:")
		print("")
		print("[  python -m listen.STT.as_service  ]")
		print("")
		return any([is_proc, is_service])
	# check for auth
	is_speech_recognition_enabled = get_is_speech_recognition_enabled()
	# if not auth, last chance
	if not is_speech_recognition_enabled and any([is_proc, is_service]):
		auth = not yes_no_dialog(
			"Manager:Assistant:Export:STT ? [Mic]",
			"Assistant: Would you grant me access to the microphone array?\n\n(?): How the microphone's data is going to be used?\n\n[!]: Your voice will be recorded and stored alongside the transcription.\n{i}: This data is only availible to you. You can use your data however you see fit.\n\n\n{i}: Checkout the ~/.trainer/STT/extracted/data/Assistant directory to see availible data.",
			yes_text="Deny",
			no_text="Grant",
			style=STYLE
		).run() #the not is there so that deny is the default
	elif is_speech_recognition_enabled and any([is_proc, is_service]):
		auth = True
		print("Access Mic Authorized -> Manager:Assistant:Export:STT")
	else:
		print("Unkown Error -> Manager:Assistant:Export:STT")
		auth = False
	return auth

def this_requires_sr():
	speech_recognition_auth = get_speech_recognition_auth()
	if not speech_recognition_auth:
		print( "Invalid Auth for Mic -> Manager:Assistant:Export:STT" )
		return False
	print( "Granted Auth for Mic -> Manager:Assistant:Export:STT" )
	return True

def export_nlu_stt():
	# This requires speech recognition services
	if not this_requires_sr():
		print("Assistant: Manager requires access to the mic arrray.\nYou need to install listen.\nAuthorize listen to record and start the server.\nThen run this manager again.\nMore info about listen at https://gitlab.com/waser-technologies/technologies/listen.")
		print("Interuption -> Manager:Assistant:Export:STT")
		sys.exit(1)

	print(export_intents_stt())

