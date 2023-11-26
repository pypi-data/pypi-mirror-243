from owega.utils import get_home_dir, info_print
from owega.utils import debug_print as dp_internal
import os
import openai
import json5 as json

baseModels = [
	"gpt-3.5-turbo-16k",
	"gpt-4",
	"gpt-4-1106-preview",
]
baseConf = {
	"api_key": "",
	"organization": "",
	"temperature": 0.8,
	"top_p": 1.0,
	"frequency_penalty": 0.0,
	"presence_penalty": 0.0,
	"max_tokens": 3000,
	"available_models": baseModels,
	"model": baseModels[0],
	"debug": False,
	"commands": False,
	"estimation": True,
}


def debug_print(text: str) -> None:
	return dp_internal(text, baseConf.get("debug", False))


# loads the config from a config file
def get_conf(conf_path=""):
	if not conf_path:
		conf_path = get_home_dir() + "/.owega.json"
		debug_print(f"conf_path is {conf_path}")
	if (os.path.exists(conf_path)):
		with open(conf_path) as f:
			conf_dict = json.load(f)
			for k, v in conf_dict.items():
				baseConf[k] = v
	if baseConf.get("api_key", "") != "":
		openai.api_key = baseConf["api_key"]


# list available models
def list_models():
	info_print("Available models:")
	for index, model in enumerate(baseConf.get("available_models", [])):
		info_print(f"    [{index}]: {model}")
