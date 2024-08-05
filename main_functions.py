import json
import os
import importlib

from core.speech_reco import SpeechRecognizer
from core.talk import TextToSpeech

class Main_Functions:
    def __init__(self):
        self.recognizer = SpeechRecognizer(language="en-US")
        self.tts = TextToSpeech(language='en')

    def load_config(self, config_file="config.json"):
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config

    def load_modules(self, modules_config):
        modules = {}
        for module_name, module_info in modules_config.items():
            if module_info.get('enabled') == True:
                module = importlib.import_module(f'modules.{module_name}')
                modules[module_name] = module.Module(module_info)
        return modules

    def load_user(self, cofig):
        user_info = cofig['user']
        return user_info

    def get_wake_word(self, config):
        return config.get('system', {}).get('wake_word', {}).get('word', '')
    
    def enter(self, wake_word, user):
        while True:
            audio = self.recognizer.listen()
            if audio:
                text = self.recognizer.recognize(audio).lower()

                if text.startswith(wake_word.lower()):

                    if text == wake_word.lower() + " standby":
                        return "standby"
                    
                    if text == wake_word.lower() + " go to sleep":
                        return "sleep"

                    self.tts.text_to_speech(f"You said: {text}")
    
    def start(self):
        config = self.load_config('config.json')

        modules = self.load_modules(config['modules'])

        user = self.load_user(config)
        wake_word = self.get_wake_word(config)

        self.tts.text_to_speech(f"Hi {user.get('name')}. When you are ready to start, say {wake_word}")

        while True:
            audio = self.recognizer.listen()
            if audio:
                text = self.recognizer.recognize(audio)

                if wake_word.lower() in text.lower():
                    self.tts.text_to_speech(f"Hello {user.get('name')}.")
                    if modules != []: self.tts.text_to_speech(f"I have loaded the following modules: {', '.join(modules.keys())}")
                    self.tts.text_to_speech("What can I do for you?")
                    exit = self.enter(wake_word, user)

                    if exit == "standby":
                        self.tts.text_to_speech("For now, I'm in standby mode. Call me when you're ready.")

                    if exit == "sleep":
                        self.tts.text_to_speech("Shutting down. Goodbye!")
                        break
                    

if __name__ == '__main__':
    Main_Functions.start()