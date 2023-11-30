import sys

from prompt_toolkit.shortcuts import clear, set_title
from assistant.manager.nlu import *

def main(ARGS):

	set_title("Manager:Assistant")

	clear()

	print("Welcome to Data Manager for Assistant.")

	if ARGS.sync_all or (
		not ARGS.ex_stt
		and not ARGS.ex_tts
		and not ARGS.im_stt
		and not ARGS.im_tts
	):
		print("\n")
		print("Synchronizing all data.")
		sync_all_flag = True
	else:
		sync_all_flag = False

	if ARGS.ex_stt or sync_all_flag:
		print("\n") #clear()
		print("Exporting NLU data to STT.")
		set_title("Manager:Assistant:Export:STT")
		from assistant.manager.nlu_to_stt import export_nlu_stt
		export_nlu_stt()

	if ARGS.ex_tts or sync_all_flag:
		print("\n") #clear()
		print("Exporting NLU data to TTS.")
		set_title("Manager:Assistant:Export:TTS")
		print("Kidding there's nothing to do!")

	if ARGS.im_stt or sync_all_flag:
		print("\n") #clear()
		print("Importing STT data to NLU.")
		set_title("Manager:Assistant:Import:STT")
		print("Kidding there's nothing to do!")

	if ARGS.im_tts or sync_all_flag:
		print("\n") #clear()
		print("Importing TTS data to NLU.")
		set_title("Manager:Assistant:Import:TTS")
		print("Kidding there's nothing to do!")
	
	print("\n") #clear()
	print("There is nothing left to do.")
	print("Check out outputed logs above to get more info.")
	
	set_title("Manager:Assistant")
	print("")
	if USERNAME and sync_all_flag:
		print(f"Manager:Assistant -> Contratulate {USERNAME.capitalize()}")

	print("Achieved -> Manager:Assistant")
	sys.exit(0)

def run():
	import argparse
	parser = argparse.ArgumentParser(description="Data Manager for Assistant")

	# Sync data
	parser.add_argument('-a', '--sync_all', action="store_true", help="sync all your data")

	# Data exporter
	parser.add_argument('-S', '--ex_stt', action="store_true", help="export your NLU data to STT")
	parser.add_argument('-T', '--ex_tts', action="store_true", help="export your NLU data to TTS")

	# Data importer
	parser.add_argument('-s', '--im_stt', action="store_true", help="import NLU data from STT")
	parser.add_argument('-t', '--im_tts', action="store_true", help="import NLU data from TTS")

	ARGS = parser.parse_args()
	try:
		main(ARGS)
	except KeyboardInterrupt:
		print(f"{USERNAME}: \'[Ctrl] + [C]\' as Keyboard Interupt -> Manager:Assistant")
		sys.exit(1)
	sys.exit(0)

if __name__ == '__main__':
	run()	
