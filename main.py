import json
import os
import importlib

from core.speech_reco import SpeechRecognizer

def load_config(config_file="config.json"):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def load_modules(modules_config):
    modules = {}
    for module_name, module_info in modules_config.items():
        if module_info.get('enabled') == True:
            module = importlib.import_module(f'modules.{module_name}')
            modules[module_name] = module.Module(module_info)
    return modules

def load_user(cofig):
    user_info = cofig['user']
    return user_info

def main():
    config = load_config('config.json')
    modules = load_modules(config['modules'])
    user = load_user(config)

    print(f"Modules loaded: {list(modules.keys())}")

    recognizer = SpeechRecognizer(language="en-US")

    while True:
        audio = recognizer.listen()
        if audio:
            text = recognizer.recognize(audio)

if __name__ == '__main__':
    main()