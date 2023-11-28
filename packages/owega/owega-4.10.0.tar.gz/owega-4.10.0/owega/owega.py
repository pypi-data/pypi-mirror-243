#!/usr/bin/env python3
# Import the necessary modules
import openai
import os
import json5 as json
import getpass
import sys
import time
import re
import argparse
import prompt_toolkit as pt
import tempfile
import editor
from .changelog import OwegaChangelog
from .license import OwegaLicense
from .config import baseConf, get_conf, list_models
from .OwegaFun import existingFunctions, connectLTS, functionlist_to_toollist
from .utils import (
	get_home_dir,
	get_temp_file,
	info_print,
	do_quit,
	success_msg,
	clrtxt,
	print_help,
)
from .conversation import Conversation
import tiktoken


def play_opus(location: str) -> None:
	try:
		os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
		import pygame
	except Exception:
		pass
	pygame.mixer.init()
	sound = pygame.mixer.Sound(location)
	sound.play()
	try:
		while pygame.mixer.get_busy():
			pygame.time.delay(100)
	except KeyboardInterrupt:
		pass
	pygame.mixer.quit()


# prints an Conversation history
# TODO: move it as an Conversation method
def print_history(m: Conversation):
	for message in m.get_messages():
		if message['role'] == 'system':
			print("[ \033[92mSYSTEM\033[0m ]\033[92m")
		elif message['role'] == 'user':
			print("[ \033[96mUSER\033[0m ]\033[96m")
		elif message['role'] == 'assistant':
			print("[ \033[95mASSISTANT\033[0m ]\033[95m")
		else:
			print("[ \033[95mFUNCTION\033[0m ]\033[95m")
		print(message['content'])
		print("\033[0m")


# sometimes, GPT will give back invalid json.
# this function tries to make it valid
def convert_invalid_json(invalid_json):
	def replace_content(match):
		content = match.group(1)
		content = (
			content
			.replace('"', '\\"')
			.replace("\n", "\\n")
		)
		return f'"{content}"'
	valid_json = re.sub(r'`([^`]+)`', replace_content, invalid_json)
	return valid_json


# get a copy of owega's config
def get_oc_conf():
	return baseConf.copy()


def estimated_tokens(ppt: str, messages: Conversation, functions):
	try:
		encoder = tiktoken.encoding_for_model("gpt-4")
		req = ""
		req += ppt
		req += json.dumps(messages.get_messages())
		req += json.dumps(functions)
		tokens = encoder.encode(req)
		return len(tokens)
	except Exception as e:
		if baseConf.get("debug"):
			print(
				"An error has occured while estimating tokens:",
				file=sys.stderr
			)
			print(e, file=sys.stderr)
		return 0


# ask openAI a question
# TODO: comment a lot more
def ask(
	prompt: str = "",
	messages: Conversation = Conversation(),
	model=baseConf.get("model", ""),
	temperature=baseConf.get("temperature", 0.8),
	max_tokens=baseConf.get("max_tokens", 3000),
	function_call="auto",
	temp_api_key="",
	temp_organization="",
	top_p=baseConf.get("top_p", 1.0),
	frequency_penalty=baseConf.get("frequency_penalty", 0.0),
	presence_penalty=baseConf.get("presence_penalty", 0.0),
):
	connectLTS(messages.add_memory, messages.remove_memory, messages.edit_memory)
	old_api_key = openai.api_key
	old_organization = openai.organization
	if (prompt):
		messages.add_question(prompt)
	else:
		prompt = messages.last_question()
	if isinstance(function_call, bool):
		if function_call:
			function_call = "auto"
		else:
			function_call = "none"
	response = False
	while (not response):
		try:
			if (temp_api_key):
				openai.api_key = temp_api_key
			if (temp_organization):
				openai.organization = temp_organization
			response = openai.chat.completions.create(
				model=model,
				temperature=temperature,
				max_tokens=max_tokens,
				top_p=top_p,
				frequency_penalty=frequency_penalty,
				presence_penalty=presence_penalty,
				messages=messages.get_messages(),
				tools=functionlist_to_toollist(
					existingFunctions.getEnabled()),
				tool_choice=function_call,
			)
			if (temp_api_key):
				openai.api_key = old_api_key
			if (temp_organization):
				openai.organization = old_organization
		except openai.BadRequestError:
			messages.shorten()
		except openai.InternalServerError:
			print("[Owega] Service unavailable...", end="")
			time.sleep(1)
			print(" Retrying now...")
	# do something with the response
	message = response.choices[0].message
	while message.tool_calls is not None:
		try:
			for tool_call in message.tool_calls:
				tool_function = tool_call.function
				function_name = tool_function.name
				try:
					kwargs = json.loads(tool_function.arguments)
				except json.decoder.JSONDecodeError:
					unfixed = tool_function.arguments
					fixed = convert_invalid_json(unfixed)
					kwargs = json.loads(fixed)
				function_response = \
					existingFunctions.getFunction(function_name)(**kwargs)
				messages.add_function(function_name, function_response)
			response2 = False
			while not (response2):
				try:
					if (temp_api_key):
						openai.api_key = temp_api_key
					if (temp_organization):
						openai.organization = temp_organization
					response2 = openai.chat.completions.create(
						model=model,
						temperature=temperature,
						max_tokens=max_tokens,
						top_p=top_p,
						frequency_penalty=frequency_penalty,
						presence_penalty=presence_penalty,
						messages=messages.get_messages(),
						tools=functionlist_to_toollist(
							existingFunctions.getEnabled()),
						tool_choice=function_call,
					)
					if (temp_api_key):
						openai.api_key = old_api_key
					if (temp_organization):
						openai.organization = old_organization
				except openai.error.InvalidRequestError:
					messages.shorten()
				except openai.error.ServiceUnavailableError:
					print("[Owega] Service unavailable...", end="")
					time.sleep(1)
					print(" Retrying now...")
				message = response2.choices[0].message
		except Exception as e:
			print("Exception: " + str(e))
			print(message.tool_calls[0].function.name)
			print(message.tool_calls[0].function.arguments)
			break
	try:
		messages.add_answer(message.content.strip())
	except Exception as e:
		print("Exception: " + str(e))
	return messages


# generates the config file if it doesn't exist already
def genconfig(conf_path=""):
	if not conf_path:
		conf_path = get_home_dir() + "/.owega.json"
	is_blank = True
	if (os.path.exists(conf_path)):
		is_blank = False
		with open(conf_path, "r") as f:
			if len(f.read()) < 2:
				is_blank = True
	if is_blank:
		with open(conf_path, "w") as f:
			f.write('// vim: set ft=json5:\n')
			f.write(json.dumps(baseConf, indent=4))
		info_print(f"generated config file at {conf_path}!")
		return
	print(clrtxt('red', ' WARNING ')
		+ f": YOU ALREADY HAVE A CONFIG FILE AT {conf_path}")
	print(clrtxt('red', ' WARNING ')
		+ ": DO YOU REALLY WANT TO OVERWRITE IT???")
	inps = clrtxt("red", "   y/N   ") + ': '
	inp = input(inps).lower().strip()
	if inp:
		if inp[0] == 'y':
			with open(conf_path, "w") as f:
				f.write('// vim: set ft=json5:\n')
				f.write(json.dumps(baseConf, indent=4))
			info_print(f"generated config file at {conf_path}!")
			return
	info_print("Sorry, not sorry OwO I won't let you nuke your config file!!!")


######################
# directive handlers #
######################

# dict containing all handler functions
handler_helps = {
	"quit": "exits the program",
	"exit": "exits the program",
	"help": "shows this help",
	"genconf": "generates a sample config file",
	"history": "prints conversation history",
	"commands": "toggles command execution / file creation",
	"estimation": "toggles displaying the token estimation",
	"tokens": "changes the amount of requested tokens",
	"context": "changes the AI's behaviour",
	"save": "saves the conversation history to a file",
	"load": "loads the conversation history from a file",
	"model": "list the available models and prompt for change",
	"file_input": "sends a prompt and a file from the system",
	"temperature": "sets the temperature (0.0 - 1.0, defaults 0.8)",
	"top_p": "sets the top_p value (0.0 - 1.0, defaults 1.0)",
	"frequency": "sets the frequency penalty (0.0 - 2.0, defaults 0.0)",
	"presence": "sets the presence penalty (0.0 - 2.0, defaults 0.0)",
	"edit": "edits the history",
	"system": "adds a system prompt in the chat",
	"add_sysmem": "adds a system souvenir (permanent)",
	"del_sysmem": "deletes a system souvenir",
}


# quits the program, deleting temp_file
def handle_quit(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	do_quit(
		success_msg(),
		temp_file=temp_file,
		is_temp=temp_is_temp,
		should_del=temp_is_temp
	)
	return messages


# prints help
def handle_help(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	print_help(handler_helps)
	return messages


# generates config file
def handle_genconf(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	genconfig()
	return messages


# shows chat history
def handle_history(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	print_history(messages)
	return messages


# enables/disables command execution
def handle_commands(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	if given.lower() in ["on", "true", "enable", "enabled"]:
		baseConf["commands"] = True
		existingFunctions.enableGroup("utility.system")
		info_print("Command execution enabled.")
		return messages

	if given.lower() in ["off", "false", "disable", "disabled"]:
		baseConf["commands"] = False
		existingFunctions.disableGroup("utility.system")
		info_print("Command execution disabled.")
		return messages

	baseConf["commands"] = (not baseConf.get("commands", False))
	if baseConf.get("commands", False):
		existingFunctions.enableGroup("utility.system")
		info_print("Command execution enabled.")
	else:
		existingFunctions.disableGroup("utility.system")
		info_print("Command execution disabled.")
	return messages


# enables/disables command execution
def handle_estimation(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	if given.lower() in ["on", "true", "enable", "enabled"]:
		baseConf["estimation"] = True
		info_print("Token estimation enabled.")
		return messages

	if given.lower() in ["off", "false", "disable", "disabled"]:
		baseConf["estimation"] = False
		info_print("Token estimation disabled.")
		return messages

	baseConf["estimation"] = (not baseConf.get("estimation", False))
	if baseConf.get("estimation", False):
		info_print("Token estimation enabled.")
	else:
		info_print("Token estimation disabled.")
	return messages


# change requested tokens amount
def handle_tokens(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	if given.isdigit():
		baseConf["max_tokens"] = int(given)
		info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
		return messages
	info_print(f'Currently requested tokens: {baseConf.get("max_tokens", 3000)}')
	info_print('How many tokens should be requested?')
	new_tokens = pt.prompt(pt.ANSI(
		'\n' + clrtxt("magenta", " tokens ") + ': '
	)).strip()
	if new_tokens.isdigit():
		baseConf["max_tokens"] = int(new_tokens)
		info_print(f'Set requested tokens to {baseConf.get("max_tokens", 3000)}')
	else:
		info_print('Invalid input, keeping current requested tokens amount')
	return messages


# change owega's system prompt
def handle_context(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	if given:
		messages.set_context(given)
		info_print(f"New context: {messages.get_context()}")
		return messages
	info_print("Old context: " + messages.get_context())
	new_context = ps['context'].prompt(pt.ANSI(
		'\n' + clrtxt("magenta", " new context ") + ': ')).strip()
	if new_context:
		messages.set_context(new_context)
		info_print(f"New context: {messages.get_context()}")
	else:
		info_print("New context empty, keeping old context!")
	return messages


# saves the messages and prompt to a json file
def handle_save(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	try:
		if given:
			file_path = given
		else:
			file_path = ps['save'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " file output ") + ': ')).strip()
		messages.save(file_path)
	except (Exception, KeyboardInterrupt, EOFError):
		print(clrtxt("red", " ERROR ") + f": could not write to \"{file_path}\"")
	else:
		print(clrtxt("green", " SUCCESS ") + ": conversation saved!")
	return messages


# loads the messages and prompt from a json file
def handle_load(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	file_path = ''
	try:
		if given:
			file_path = given
		else:
			file_path = ps['load'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " file to load ") + ': ')).strip()
		messages.load(file_path)
	except (Exception, KeyboardInterrupt, EOFError):
		print(clrtxt("red", " ERROR ") + f": could not read from \"{file_path}\"")
	else:
		print(clrtxt("green", " SUCCESS ") + ": conversation loaded!")
	return messages


# changes the selected model
def handle_model(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	info_print(f"Current model: {baseConf.get('model', '')}")
	list_models()
	print()
	if given:
		new_model = given
	else:
		new_model = ps['model'].prompt(pt.ANSI(
			'\n' + clrtxt("magenta", " new model ") + ': ')).strip()
	if (new_model.isnumeric()):
		if (int(new_model) < len(baseConf.get("available_models", []))):
			mn = int(new_model)
			baseConf["model"] = baseConf.get("available_models", [])[mn]
			info_print(f"Model changed to {baseConf.get('model', '')}")
		else:
			info_print(f"Model not available, keeping {baseConf.get('model', '')}")
	elif new_model in list(baseConf.get("available_models", [])):
		baseConf["model"] = new_model
		info_print(f"Model changed to {baseConf.get('model', '')}")
	else:
		info_print(f"Model not available, keeping {baseConf.get('model', '')}")
	return messages


# get input from a file instead of the terminal
def handle_finput(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	given = given.split(' ')[0]
	if given:
		file_path = given
	else:
		file_path = ps['load'].prompt(pt.ANSI(
			clrtxt("yellow", " FILE LOCATION ") + ": ")).strip()
	if (os.path.exists(file_path)):
		user_prompt = ps['main'].prompt(pt.ANSI(
			clrtxt("yellow", " PRE-FILE PROMPT ") + ": ")).strip()
		with open(file_path, "r") as f:
			file_contents = f.read()
			full_prompt = f"{user_prompt}\n```\n{file_contents}\n```\n'"
			if baseConf.get("estimation", False):
				etkn = estimated_tokens(
					full_prompt,
					messages,
					functionlist_to_toollist(existingFunctions.getEnabled())
				)
				print(f"\033[37mestimated tokens: {etkn}\033[0m")
			if baseConf.get("debug", False):
				pre_time = time.time()
			messages = ask(
				prompt=full_prompt,
				messages=messages,
				model=baseConf.get("model", ""),
				temperature=baseConf.get("temperature", 0.8),
				max_tokens=baseConf.get("max_tokens", 3000),
				top_p=baseConf.get("top_p", 1.0),
				frequency_penalty=baseConf.get("frequency_penalty", 0.0),
				presence_penalty=baseConf.get("presence_penalty", 0.0)
			)
			if baseConf.get("debug", False):
				post_time = time.time()
				print(f"\033[37mrequest took {post_time-pre_time:.3f}s\033[0m")
			print()
			print(clrtxt("magenta", " OpenAI ") + ": ")
			print()
			print(messages.last_answer())
			if tts_enabled:
				tmpfile = tempfile.NamedTemporaryFile(
					prefix="owegatts.",
					suffix=".opus",
					delete=False
				)
				tmpfile.close()
				tts_answer = openai.audio.speech.create(
					model='tts-1',
					voice='nova',
					input=messages.last_answer()
				)
				if baseConf.get("debug", False):
					posttts_time = time.time()
					print(f"\033[37mrequest took {posttts_time-pre_time:.3f}s\033[0m")
				tts_answer.stream_to_file(tmpfile.name)
				play_opus(tmpfile.name)
				os.remove(tmpfile.name)
	else:
		info_print(f"Can't access {file_path}")
	return messages


# change temperature
def handle_temperature(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	try:
		new_temperature = float(given)
	except ValueError:
		info_print('Current temperature: '
			+ f'{baseConf.get("temperature", 1.0)}')
		info_print('New temperature value (0.0 - 2.0, defaults 0.8)')
		try:
			new_temperature = ps['float'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " temperature ") + ': ')).strip()
		except (ValueError, KeyboardInterrupt, EOFError):
			info_print("Invalid temperature.")
			return messages
	baseConf["temperature"] = float(new_temperature)
	nv = baseConf.get('temperature', 0.0)
	if nv > 2.0:
		info_print('Temperature too high, capping to 2.0')
		baseConf["temperature"] = 2.0
	if nv < 0.0:
		info_print('Temperature negative, capping to 0.0')
		baseConf["temperature"] = 0.0
	info_print('Set temperature to '
		+ f'{baseConf.get("temperature", 0.0)}')
	return messages


# change top_p value
def handle_top_p(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	try:
		new_top_p = float(given)
	except ValueError:
		info_print(f'Current top_p: {baseConf.get("top_p", 1.0)}')
		info_print('New top_p value (0.0 - 1.0, defaults 1.0)')
		try:
			new_top_p = ps['float'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " top_p ") + ': ')).strip()
		except (ValueError, KeyboardInterrupt, EOFError):
			info_print("Invalid top_p.")
			return messages
	baseConf["top_p"] = float(new_top_p)
	nv = baseConf.get('top_p', 1.0)
	if nv > 1.0:
		info_print('top_p too high, capping to 1.0')
		baseConf["top_p"] = 1.0
	if nv < 0.0:
		info_print('top_p too low, capping to 0.0')
		baseConf["top_p"] = 0.0
	info_print(f'Set top_p to {baseConf.get("top_p", 1.0)}')
	return messages


# change frequency penalty
def handle_frequency(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	try:
		new_frequency_penalty = float(given)
	except ValueError:
		info_print('Current frequency penalty: '
			+ f'{baseConf.get("frequency_penalty", 1.0)}')
		info_print('New frequency penalty value (0.0 - 2.0, defaults 0.0)')
		try:
			new_frequency_penalty = ps['float'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " frequency penalty ") + ': ')).strip()
		except (ValueError, KeyboardInterrupt, EOFError):
			info_print("Invalid frequency penalty.")
			return messages
	baseConf["frequency_penalty"] = float(new_frequency_penalty)
	nv = baseConf.get('frequency_penalty', 0.0)
	if nv > 2.0:
		info_print('Penalty too high, capping to 2.0')
		baseConf["frequency_penalty"] = 2.0
	if nv < 0.0:
		info_print('Penalty too low, capping to 0.0')
		baseConf["frequency_penalty"] = 0.0
	info_print('Set frequency penalty to '
		+ f'{baseConf.get("frequency_penalty", 0.0)}')
	return messages


# change presence penalty
def handle_presence(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	try:
		new_presence_penalty = float(given)
	except ValueError:
		info_print('Current presence penalty: '
			+ f'{baseConf.get("presence_penalty", 1.0)}')
		info_print('New presence penalty value (0.0 - 2.0, defaults 0.0)')
		try:
			new_presence_penalty = ps['float'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " presence penalty ") + ': ')).strip()
		except (ValueError, KeyboardInterrupt, EOFError):
			info_print("Invalid presence penalty.")
			return messages
	baseConf["presence_penalty"] = float(new_presence_penalty)
	nv = baseConf.get('presence_penalty', 0.0)
	if nv > 2.0:
		info_print('Penalty too high, capping to 2.0')
		baseConf["presence_penalty"] = 2.0
	if nv < 0.0:
		info_print('Penalty too low, capping to 0.0')
		baseConf["presence_penalty"] = 0.0
	info_print('Set presence penalty to '
		+ f'{baseConf.get("presence_penalty", 0.0)}')
	return messages


def handle_edit(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	for msg_id, msg in enumerate(messages.messages):
		role = msg.get('role', 'unknown')
		if role == 'user':
			print(f"[\033[0;93mUSER\033[0m] [\033[0;92m{msg_id}\033[0m]:")
			print('\033[0;37m', end='')
			print(msg.get('content', ''))
			print('\033[0m', end='')
			print()
		elif role == 'system':
			print(f"[\033[0;95mSYSTEM\033[0m] [\033[0;92m{msg_id}\033[0m]:")
			print('\033[0;37m', end='')
			print(msg.get('content', ''))
			print('\033[0m', end='')
			print()
		elif role == 'assistant':
			print(f"[\033[0;96mASSISTANT\033[0m] [\033[0;92m{msg_id}\033[0m]:")
			print('\033[0;37m', end='')
			print(msg.get('content', ''))
			print('\033[0m', end='')
			print()
	try:
		msg_id = ps['integer'].prompt(pt.ANSI(
			'\n' + clrtxt("magenta", " message ID ") + ': ')).strip()
	except (ValueError, KeyboardInterrupt, EOFError):
		info_print("Invalid message ID, cancelling edit")
		return messages

	msg_id = int(msg_id)

	if (msg_id < 0) or (msg_id >= len(messages.messages)):
		info_print("Invalid message ID, cancelling edit")
		return messages

	try:
		new_msg = editor.edit(
			contents=messages.messages[msg_id].get('content', '').encode('utf8')
		).decode('utf8')
	except UnicodeDecodeError:
		info_print("Error handling given message, edit not saved")
		return messages
	if new_msg:
		messages.messages[msg_id]['content'] = new_msg
	else:
		info_print("Message empty, deleting it...")
		messages.pop(msg_id)

	return messages


# adds a system message
def handle_system(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	if not given:
		try:
			given = ps['main'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " System message ") + ": ")).strip()
		except (KeyboardInterrupt, EOFError):
			return messages
	if given:
		messages.add_system(given)
	else:
		info_print("System message empty, not adding.")
	return messages


# adds a system message
def handle_add_sysmem(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	given = given.strip()
	if not given:
		try:
			given = ps['main'].prompt(pt.ANSI(
				'\n' + clrtxt("magenta", " System souvenir ") + ": ")).strip()
		except (KeyboardInterrupt, EOFError):
			return messages
	if given:
		messages.add_sysmem(given)
	else:
		info_print("System souvenir empty, not adding.")
	return messages


# adds a system message
def handle_del_sysmem(temp_file, messages, ps, given="", temp_is_temp=False, tts_enabled=False):
	for index, sysmem in enumerate(messages.systemsouv):
		print(f"[\033[0;95mSystem souvenir\033[0m] [\033[0;92m{index}\033[0m]:")
		print('\033[0;37m', end='')
		print(sysmem)
		print('\033[0m', end='')
		print()
	try:
		msg_id = ps['integer'].prompt(pt.ANSI(
			'\n' + clrtxt("magenta", " message ID ") + ': ')).strip()
	except (ValueError, KeyboardInterrupt, EOFError):
		info_print("Invalid message ID, cancelling edit")
		return messages

	msg_id = int(msg_id)

	if (msg_id < 0) or (msg_id >= len(messages.systemsouv)):
		info_print("Invalid message ID, cancelling edit")
		return messages

	messages.systemsouv.pop(msg_id)

	return messages


# dict containing all handler functions
handlers = {
	"quit": handle_quit,
	"exit": handle_quit,
	"help": handle_help,
	"genconf": handle_genconf,
	"history": handle_history,
	"commands": handle_commands,
	"estimation": handle_estimation,
	"tokens": handle_tokens,
	"context": handle_context,
	"save": handle_save,
	"load": handle_load,
	"model": handle_model,
	"file_input": handle_finput,
	"temperature": handle_temperature,
	"top_p": handle_top_p,
	"frequency": handle_frequency,
	"presence": handle_presence,
	"edit": handle_edit,
	"system": handle_system,
	"add_sysmem": handle_add_sysmem,
	"del_sysmem": handle_del_sysmem,
}


# bottom toolbar and style for prompt_toolkit
def main_bottom_toolbar(what: str = "toolbar"):
	if what == "style":
		msd = {
			'red':     '#000000 bg:#FF0000',  # noqa: E241
			'green':   '#000000 bg:#00FF00',  # noqa: E241
			'blue':    '#000000 bg:#0000FF',  # noqa: E241
			'yellow':  '#000000 bg:#FFFF00',  # noqa: E241
			'magenta': '#000000 bg:#FF00FF',  # noqa: E241
			'cyan':    '#000000 bg:#00FFFF',  # noqa: E241
			'white':   '#000000 bg:#FFFFFF',  # noqa: E241
		}
		msd['bottom-toolbar'] = msd['white']
		msd['bottom-even'] = msd['magenta']
		msd['bottom-odd'] = msd['cyan']
		msd['bottom-on'] = msd['green']
		msd['bottom-off'] = msd['red']
		main_style = pt.styles.Style.from_dict(msd)
		return main_style

	class tr:
		def __init__(self):
			self.table = []
			self.count = 0

		def add(self, prefix="/", txt="", color="yellow"):
			new_class = "white"
			if not isinstance(txt, str):
				txt = str(txt)
			if self.count:
				self.table.append((
					"class:blue",
					" - "
				))
			if prefix:
				if txt:
					prefix = prefix + ": "
				self.table.append((
					f"class:{new_class}",
					prefix
				))
			if txt:
				self.table.append((
					f"class:{color}",
					txt
				))
			self.count += 1

	to_ret = tr()
	to_ret.add(f"v{OwegaChangelog.version}")
	to_ret.add("model", baseConf.get("model", "unknown"))
	to_ret.add(
		"commands",
		"ON" if baseConf.get("commands") else "OFF",
		"bottom-on" if baseConf.get("commands") else "bottom-off"
	)
	to_ret.add("tokens", baseConf.get("max_tokens", "unknown"))
	to_ret.add(
		"estimation",
		"ON" if baseConf.get("estimation") else "OFF",
		"bottom-on" if baseConf.get("estimation") else "bottom-off"
	)
	to_ret.add("temperature", baseConf.get("temperature", "unknown"))
	to_ret.add("top_p", baseConf.get("top_p", "unknown"))
	to_ret.add("frequency penalty", baseConf.get("frequency_penalty", "unknown"))
	to_ret.add("presence penalty", baseConf.get("presence_penalty", "unknown"))
	return to_ret.table


# main interaction loop
def user_interaction_loop(temp_file="", input_file="", temp_is_temp=False, tts_enabled=False):
	if not temp_file:
		temp_is_temp = True
		temp_file = get_temp_file()

	# generate completion from command list (handlers)
	command_list = ['/' + command for command in handlers.keys()]

	# CTRL+N makes a new line
	main_kb = pt.key_binding.KeyBindings()

	@main_kb.add('c-n')
	def _(event):
		event.current_buffer.insert_text('\n')

	# this defines how newlines are shown
	def main_prompt_continuation(width, line_number, is_soft_wrap):
		cont = '   ' if is_soft_wrap else '...'
		if (width >= 4):
			return (' ' * (width - 4)) + cont + ' '
		else:
			return ' ' * width

	# get main style
	main_style = main_bottom_toolbar("style")

	# creates Conversation object and populate it
	messages = Conversation()
	connectLTS(
		messages.add_memory,
		messages.remove_memory,
		messages.edit_memory
	)
	if input_file:
		messages.load(input_file)

	# sets the input prompt
	input_prompt = '\n' + clrtxt("yellow", "  USER  ") + ": "

	# prompt sessions (for command history, and other parameters)
	ps = {}

	class SlashCommandCompleter(pt.completion.WordCompleter):
		def __init__(self, words, ignore_case=False):
			super().__init__(words, ignore_case=ignore_case)
			# Define a regex pattern that includes the slash as a word character
			self.pattern = re.compile(r'[^ \t\n\r\f\v]+')

		def get_completions(self, document, complete_event):
			# Use the custom pattern to find the word before the cursor
			word_before_cursor = document.get_word_before_cursor(
				pattern=self.pattern)
			for word in self.words:
				if word.startswith(word_before_cursor):
					yield pt.completion.Completion(
						word, -len(word_before_cursor))

	# keyword autocompletion
	main_completer = SlashCommandCompleter(
		words=command_list,
		ignore_case=True
	)

	# main session, for general context
	ps['main'] = pt.PromptSession(
		history=pt.history.FileHistory(
			'' + get_home_dir() + '/.owega.history'
		),
		completer=main_completer,
		complete_while_typing=True,
		complete_in_thread=True,
		auto_suggest=pt.auto_suggest.AutoSuggestFromHistory(),
		bottom_toolbar=main_bottom_toolbar,
		style=main_style,
		key_bindings=main_kb,
		prompt_continuation=main_prompt_continuation,
	)

	# context session, when editing owega's system prompt
	ps['context'] = pt.PromptSession()

	class SaveValidator(pt.validation.Validator):
		def validate(self, document):
			text = document.text

			if os.path.isdir(text):
				raise pt.validation.ValidationError(
					message='you specified a directory, not a file',
					cursor_position=len(text)
				)
			elif not os.path.isdir(os.path.dirname(text)):
				raise pt.validation.ValidationError(
					message='parent dir does not exist, cannot create file',
					cursor_position=len(text)
				)

	ps['save'] = pt.PromptSession(
		completer=pt.completion.PathCompleter(),
		validator=SaveValidator()
	)

	class LoadValidator(pt.validation.Validator):
		def validate(self, document):
			text = document.text

			if os.path.isdir(text):
				raise pt.validation.ValidationError(
					message='this is a directory, not a file',
					cursor_position=len(text)
				)

			if not os.path.isfile(text):
				raise pt.validation.ValidationError(
					message='file does not exist',
					cursor_position=len(text)
				)

	ps['load'] = pt.PromptSession(
		completer=pt.completion.PathCompleter(),
		validator=LoadValidator()
	)

	# file session, with file completion
	ps['file'] = pt.PromptSession(
		completer=pt.completion.PathCompleter()
	)

	# file session with file completion for file_input directive
	ps['file_input'] = pt.PromptSession(
		completer=pt.completion.PathCompleter()
	)

	# model session, for model selection
	# TODO: add model completion
	ps['model'] = pt.PromptSession()

	class IntegerValidator(pt.validation.Validator):
		def validate(self, document):
			text = document.text

			try:
				int(text)
			except ValueError:
				raise pt.validation.ValidationError(
					message='This input contains non-numeric characters',
					cursor_position=len(text)
				)

	class FloatValidator(pt.validation.Validator):
		def validate(self, document):
			text = document.text

			try:
				float(text)
			except ValueError:
				raise pt.validation.ValidationError(
					message='This input is not a valid floating-point number',
					cursor_position=len(text)
				)

	ps['integer'] = pt.PromptSession(validator=IntegerValidator())
	ps['float'] = pt.PromptSession(validator=FloatValidator())

	# bootup info
	info_print("===== Owega =====")
	info_print(f"Owega v{OwegaChangelog.version}")
	info_print('Type "/help" for help')
	info_print(f"Default model is {baseConf.get('model', '')}")
	info_print(f"temp file is {temp_file}")

	# API key detection
	if baseConf.get("api_key", "").startswith("sk-"):
		openai.api_key = baseConf.get("api_key", "")
	else:
		# if key not in config: ask for key only if not already set (ie envvar)
		try:
			if not openai.api_key.startswith("sk-"):
				openai.api_key = getpass.getpass(prompt="OpenAI API Key: ")
		except AttributeError:
			openai.api_key = getpass.getpass(prompt="OpenAI API Key: ")
		baseConf["api_key"] = openai.api_key

	# Organization detection
	if baseConf.get("organization", "").startswith("org-"):
		openai.organization = baseConf.get("organization", "")

	# main interaction loop:
	while True:
		# save temp file
		messages.save(temp_file)

		# get user input, and strip it (no excess spaces / tabs / newlines
		user_input = ps['main'].prompt(pt.ANSI(input_prompt)).strip()

		command_found = False
		if user_input.startswith('/'):
			uinp_spl = user_input.split(' ')
			given = ' '.join(uinp_spl[1:])
			command = uinp_spl[0][1:]
			if command in handlers.keys():
				command_found = True
				current_handler = handlers.get(command, handle_help)
				messages = current_handler(
					temp_file,
					messages,
					ps,
					given,
					temp_is_temp,
					tts_enabled
				)
		if not command_found:
			if baseConf.get("estimation", False):
				etkn = estimated_tokens(
					user_input,
					messages,
					functionlist_to_toollist(existingFunctions.getEnabled())
				)
				print(f"\033[37mestimated tokens: {etkn}\033[0m")
			if baseConf.get("debug", False):
				pre_time = time.time()
			messages = ask(
				prompt=user_input,
				messages=messages,
				model=baseConf.get("model", ''),
				temperature=baseConf.get("temperature", 0.8),
				max_tokens=baseConf.get("max_tokens", 3000),
				top_p=baseConf.get("top_p", 1.0),
				frequency_penalty=baseConf.get("frequency_penalty", 0.0),
				presence_penalty=baseConf.get("presence_penalty", 0.0)
			)
			if baseConf.get("debug", False):
				post_time = time.time()
				print(f"\033[37mrequest took {post_time-pre_time:.3f}s\033[0m")

			# Print the generated response
			print()
			print(clrtxt("magenta", " OpenAI ") + ": ")
			print()
			print(messages.last_answer())

			if tts_enabled:
				tmpfile = tempfile.NamedTemporaryFile(
					prefix="owegatts.",
					suffix=".opus",
					delete=False
				)
				tmpfile.close()
				tts_answer = openai.audio.speech.create(
					model='tts-1',
					voice='nova',
					input=messages.last_answer()
				)
				if baseConf.get("debug", False):
					posttts_time = time.time()
					print(f"\033[37mrequest took {posttts_time-pre_time:.3f}s\033[0m")
				tts_answer.stream_to_file(tmpfile.name)
				play_opus(tmpfile.name)
				os.remove(tmpfile.name)


# parse command-line arguments
def parse_args():
	parser = argparse.ArgumentParser(description="Owega main application")
	parser.add_argument("-d", "--debug", action='store_true',
		help="Enable debug output")
	parser.add_argument("-c", "--changelog", action='store_true',
		help="Display changelog and exit")
	parser.add_argument("-l", "--license", action='store_true',
		help="Display license and exit")
	parser.add_argument("-v", "--version", action='store_true',
		help="Display version and exit")
	parser.add_argument("-f", "--config-file", type=str,
		help="Specify path to config file")

	parser.add_argument("-i", "--history", type=str,
		help="Specify the history file to import")

	parser.add_argument("-a", "--ask", type=str,
		help="Asks a question directly from the command line")

	parser.add_argument("-o", "--output", type=str,
		help="Saves the history to the specified file")

	parser.add_argument("-t", "--tts", action='store_true',
		help="Enables TTS generation when asking")
	parser.add_argument("-s", "--ttsfile", type=str,
		help="Outputs a generated TTS file single-ask mode")

	return parser.parse_args()


# finds if any element in the list a is present in the list b
def is_la_in_lb(a, b):
	for e in a:
		if e in b:
			return True
	return False


# ask a single question (with a new context)
def single_ask(user_prompt, temp_file="", input_file="", temp_is_temp=False, tts_enabled=False, should_print=False):
	if not temp_file:
		temp_is_temp = True
		temp_file = get_temp_file()
	messages = Conversation()
	connectLTS(
		messages.add_memory,
		messages.remove_memory,
		messages.edit_memory
	)
	if input_file:
		messages.load(input_file)
	messages = ask(
		prompt=user_prompt,
		messages=messages,
		model=baseConf.get("model", ''),
		temperature=baseConf.get("temperature", 0.8),
		max_tokens=baseConf.get("max_tokens", 3000),
		top_p=baseConf.get('top_p', 1.0),
		frequency_penalty=baseConf.get('frequency_penalty', 0.0),
		presence_penalty=baseConf.get('presence_penalty', 0.0)
	)
	if should_print:
		print(messages.last_answer())
	if tts_enabled:
		tmpfile = tempfile.NamedTemporaryFile(
			prefix="owegatts.",
			suffix=".opus",
			delete=False
		)
		tmpfile.close()
		tts_answer = openai.audio.speech.create(
			model='tts-1',
			voice='nova',
			input=messages.last_answer()
		)
		tts_answer.stream_to_file(tmpfile.name)
		play_opus(tmpfile.name)
		os.remove(tmpfile.name)
	return messages.last_answer()
	if not temp_is_temp:
		messages.save(temp_file)


# main function, runs if __name__ is "__main__" ;)
def main():
	args = parse_args()

	if (args.debug):  # bypass before loading conf
		baseConf["debug"] = True

	if args.changelog:
		print(OwegaChangelog.log)
	if args.license:
		print(OwegaLicense)
	if args.version:
		print(f"Owega v{OwegaChangelog.version}")
	if (args.changelog or args.license or args.version):
		do_quit(value=1)

	input_history = ""
	if (args.history):
		input_history = args.history

	temp_file = get_temp_file()
	temp_is_temp = True
	if (args.output):
		temp_is_temp = False
		temp_file = args.output

	get_conf(args.config_file)
	if baseConf.get("commands", False):
		existingFunctions.enableGroup("utility.system")
	else:
		existingFunctions.disableGroup("utility.system")

	if (args.debug):  # bypass after loading conf
		baseConf["debug"] = True

	if (args.ask):
		answer = single_ask(args.ask, temp_file, input_history, temp_is_temp, args.tts, True)
		if (args.ttsfile):
			tts_answer = openai.audio.speech.create(
				model="tts-1",
				voice="nova",
				input=answer
			)
			if (("opus" not in args.ttsfile)
				and ("mp3" not in args.ttsfile)
				and ("aac" not in args.ttsfile)
				and ("flac" not in args.ttsfile)):
				args.ttsfile = args.ttsfile + '.opus'
			tts_answer.stream_to_file(args.ttsfile)
	else:
		try:
			user_interaction_loop(
				temp_file=temp_file,
				input_file=input_history,
				temp_is_temp=temp_is_temp,
				tts_enabled=args.tts
			)
		except EOFError:
			do_quit(
				success_msg(),
				temp_file=temp_file,
				is_temp=temp_is_temp,
				should_del=temp_is_temp
			)
		except KeyboardInterrupt:
			do_quit(
				success_msg(),
				temp_file=temp_file,
				is_temp=temp_is_temp,
				should_del=False
			)


if __name__ == "__main__":
	main()
