import os
import sys
import pickle
import yaml
import toml
import json
import time
import glob
import re

from pathlib import Path

I18N, L10N = (x for x in os.environ.get('LANG', "en_EN.UTF-8").split(".")[0].split("_"))

USERNAME = os.environ.get("USERNAME", 'root')
ASSISTANT_PATH = f"/home/{USERNAME}/.assistant" if USERNAME != "root" else "/usr/share/assistant"
HOME = os.environ.get('HOME')
TRAINER_PATH = os.environ.get('TRAINER_PATH', f"{HOME}/.trainer") if USERNAME != "root" else "/usr/share/trainer"

def read_yaml(yaml_filepath):
	#print(f"Checking {yaml_filepath} for intents")
	with open(yaml_filepath, 'r') as yf:
		yml = yaml.load(yf, Loader=yaml.SafeLoader)
		yf.close()
		return yml
	return None

def read_toml(toml_filepath):
	if os.path.isfile(toml_filepath):
		with open(toml_filepath, 'r') as tf:
			tml = toml.load(tf)
			tf.close()
			return tml
	return None

def save_toml(data, file_path):
	with open(file_path, 'w') as tf:
		toml.dump(data, tf)

def get_nlu_or_none(filepath):
	y = read_yaml(filepath)
	if y:
		n = y.get('nlu', None)
		if n:
			#print(f"Found intent(s) in {filepath}")
			return n
	return None

def load_pickle(filepath, or_else=None):
	if os.path.isfile(filepath):
		with open(filepath, 'rb') as f:
			p = pickle.load(f)
			f.close()
			if p:
				return p
	return or_else

def save_pickle(data, filepath):
	with open(filepath, 'wb') as f:
		pickle.dump(data, f)
		f.close()
	return

def read_json(file_path):
	with open(file_path, 'r') as f:
		return json.load(f)

def save_json(data, file_path):
	with open(file_path, 'w') as f:
		json.dump(data, f)



def export_verified_intent_examples_to_toml(answers_path):
	bad_apples = [
		"no don\"t want this",
		"[",
		"]",
		# Add more if needed.
		# ""
	]
	answers = read_toml(answers_path) or {}
	verified_intents_examples = load_verified_intents_examples()
	for sentence, vote in verified_intents_examples.get(f'{I18N}', {}).items():
		if sentence in bad_apples:
			continue

		try:
			answers[sentence]['true' if vote == True else 'false']+=1
		except KeyError:
			if not answers.get(sentence, False):
				answers[sentence] = {
					'true': 1 if vote == True else 0,
					'false': 1 if vote == False else 0
				}
			answers[sentence]['lang'] = I18N
	
	os.system(f"cd '{Path(answers_path).parent.as_posix()}' ; git branch develop && git switch develop")
	save_toml(answers, answers_path)
	os.system(f"cd '{Path(answers_path).parent.as_posix()}' ; git add reviews.toml; git commit -m '{USERNAME} has voted' ")

def create_pull_request(local_git_repo_path):
	source = "wasertech/verified_sentences_stt"
	body = f'''
	Assistant: {USERNAME} has authorized me to pull this request.
	'''
	title = f"{USERNAME} has valided new sentences."
	os.system(f"cd {local_git_repo_path} && gh pr create --title '{title}' --body '{body}' ")

def gh_auth_login():
	return os.system("gh auth login")

def download_most_verified_answers(reviews_path=f"{TRAINER_PATH}/STT/helpers/data/reviews.toml"):
	path = Path(reviews_path).parent
	posix_path = path.as_posix()
	if path.exists():
		os.system(f"rm -r '{posix_path}'")
	os.system(f"git clone 'https://github.com/wasertech/verified_sentences_stt.git' '{posix_path}' ")
	return reviews_path

def export_answers():
	# clone verified answer
	answers_path = download_most_verified_answers()
	# export_to_toml to replace clone answers
	export_verified_intent_examples_to_toml(answers_path)
	# push pr
	gh_auth_login()
	create_pull_request(Path(answers_path).parent.as_posix())

def upload_verified_answers():
	export_answers()

def import_reviews(reviews_path):
	# import reviews_path as toml
	reviews = read_toml(reviews_path)
	for sentence, votes in reviews.items():
		if I18N not in votes.get('lang', []):
			continue

		false_votecount = votes.get('false', 0)
		true_votecount = votes.get('true', 0)
		if true_votecount + false_votecount < 1:
			# No vote on this sentence yet.
			continue
		elif true_votecount > false_votecount:
			save_verification(sentence)
		elif false_votecount > true_votecount:
			save_verification(sentence, reject=True)
		else:
			# Tie or error dont save this sentence
			continue
	
	return load_verified_intents_examples()

def get_verified_from_reviews(verified_sentences_path):
	# git clone tmp pole repo if exists
	reviews_path = download_most_verified_answers()
	
	return import_reviews(reviews_path)

def load_verified_intents_examples(from_reviews=False):
	verified_sentences_path = f"{TRAINER_PATH}/STT/helpers/.stt.verified.management"
	empty = {}
	if os.path.isfile(verified_sentences_path):
		ex = load_pickle(verified_sentences_path, or_else=empty)
		return ex
	elif from_reviews and user_wants_verified_from_answers():
		return get_verified_from_reviews(verified_sentences_path)
		
	return empty

def _format_for_training(s: str):
	s = s.lower()

	s = s.replace("\n", "")
	s = s.replace(".", "")
	s = s.replace(",", "")
	s = s.replace(":", "")
	s = s.replace(";", "")
	s = s.replace("!", "")
	s = s.replace("?", "")
	
	s = s.replace("$", " dollars ")
	s = s.replace("€", " euros ")
	s = s.replace("£", " pounds ")

	s = s.replace("_", " ")
	s = s.replace("-", " ")
	s = s.replace("\"", "")
	s = s.replace("\\", "")
	
	# Set standards
	_S = []
	standards = {
		'okay': "o k",
		'ok': "o k",
		'nevermind': "never mind",
		'anytime': "any time",
		'everybody': "every body",
		'anywhere': "any where",
		'anyone': "any one",
	}

	for w in s.split():
		if standards.get(w):
			_S.append(standards.get(w))
		else:
			_S.append(w)

	s = " ".join(_S)

	# Remove whitespaces
	s = s.replace("  ", " ")
	if s.startswith(" "):
		s = s[1:]
	if s.endswith(" "):
		s = s[:-1]
	s = " ".join([w.lower() for w in s.split()])

	return s

def get_loaded_entities():
	en = load_pickle(f"{TRAINER_PATH}/STT/helpers/.stt.entites.management", or_else={})
	return en

def load_transcribed_intents_examples():
	inex = load_pickle(f"{TRAINER_PATH}/STT/helpers/.stt.export.testset.management", or_else={})
	return inex

def load_domains_lm():
	lm = load_pickle(f"{TRAINER_PATH}/STT/helpers/.stt.export.lm.management", or_else={})
	return lm

def set_transcribed_intents_examples(transcribed_intents_examples):
	save_pickle(transcribed_intents_examples, f"{TRAINER_PATH}/STT/helpers/.stt.export.testset.management")

def set_verified_intents_examples(verified_intents_examples):
	save_pickle(verified_intents_examples, f"{TRAINER_PATH}/STT/helpers/.stt.verified.management")

def set_loaded_entites(loaded_entites):
	save_pickle(loaded_entites, f"{TRAINER_PATH}/STT/helpers/.stt.entites.management")

def set_test_set(test_set):
	set_transcribed_intents_examples(test_set)

def set_domains_lm(lm):
	save_pickle(lm, f"{TRAINER_PATH}/STT/helpers/.stt.export.lm.management")

def load_entities():
	loaded_entites = get_loaded_entities()	
	return loaded_entites.get(f'{I18N}', {})

def save_entity_example(entity_type, entity_example, context):
	loaded_entites = get_loaded_entities()
	loaded_entities_lang = loaded_entites.get(f'{I18N}', {})
	loaded_entity_type = loaded_entities_lang.get(entity_type, {})
	loaded_entity_examples = loaded_entity_type.get('examples', [])
	loaded_entity_context = loaded_entity_type.get('context', [])
	
	if context not in loaded_entity_context:
		if not loaded_entities_lang:
			loaded_entites[I18N] = {}
		if not loaded_entity_type:
			loaded_entites[I18N][entity_type] = {}
		if not loaded_entity_examples:
			loaded_entites[I18N][entity_type]['examples'] = []
		loaded_entites[I18N][entity_type]['examples'].append(entity_example)
		if not loaded_entity_context:
			loaded_entites[I18N][entity_type]['context'] = []
		loaded_entites[I18N][entity_type]['context'].append(context)
		set_loaded_entites(loaded_entites)

def get_nlu_examples():
	intents_examples = []
	data_path = f"{ASSISTANT_PATH}/data/{I18N}/NLU"
	nlu_path = f"{data_path}/nlu"
	Path(nlu_path).mkdir(parents=True, exist_ok=True)
	nlu_files = glob.glob(nlu_path + "/*/*.yml", recursive=True)
	for f in nlu_files:
		nlu = get_nlu_or_none(f)
		if nlu:
			for i in nlu:
				e = i.get('examples', None)
				if e:
					_e = e.replace("- ", ",")
					_e = _e.replace("\n", "")
					_e = _e.split(",")
					if _e:
						for u in _e:
							if not any([
								u.startswith(":"),
								u.startswith("/"),
								u.startswith("."),
								u.startswith("?"),
								u.startswith("!")
							]):
								intents_examples.append(u)
								for matched_entity in re.finditer(
									r'\[([a-zàâçéèêëîïôûùüÿñæœ .-]+)\]\([a-zàâçéèêëîïôûùüÿñæœ .-]+\)',
									u
								):
									# sentence has entity
									matched_entity_raw = matched_entity.group()
									matched_entity_type = re.findall(r'\(([a-zàâçéèêëîïôûùüÿñæœ .-_]+)\)', matched_entity_raw)[0]
									matched_entity_example = re.findall(r'\[([a-zàâçéèêëîïôûùüÿñæœ .-_]+)\]', matched_entity_raw)[0]
									save_entity_example(matched_entity_type, matched_entity_example, u)
								
	return intents_examples

def load_intent_and_entites():
	intents_examples = get_nlu_examples()
	entities = load_entities()
	return (intents_examples, entities)

def expanded_intents_examples():
	intents_examples, entities = load_intent_and_entites()

	expanded_intents_examples = intents_examples
	
	for entity_type, entity_dict in entities.items():
		entity_context = entity_dict.get('context', [])
		entity_examples = entity_dict.get('examples', [])
		for context in entity_context:
			_context = []
			for entity_example in entity_examples:
				_c = context.replace(f"[{entity_example}]({entity_type})", entity_example)
				if _c not in _context:
					_context.append(_c)
			if _context not in expanded_intents_examples:
				expanded_intents_examples.extend(context)
	
	return expanded_intents_examples

def load_intents():
	return expanded_intents_examples()
