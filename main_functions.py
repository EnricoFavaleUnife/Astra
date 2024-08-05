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

    def load_user(self):
        user_info = self.config['user']
        return user_info

    def get_wake_word(self):
        return self.config.get('system', {}).get('wake_word', {}).get('word', '')
    
    def get_standby_word(self):
        return self.config.get('system', {}).get('standby_word', {}).get('word', '')
    
    def get_shutdown_word(self):
        return self.config.get('system', {}).get('shutdown_word', {}).get('word', '')
    
    def enter(self):
        while True:
            audio = self.recognizer.listen()
            if audio:
                text = self.recognizer.recognize(audio).lower()

                if text.startswith(self.wake_word.lower()):

                    if text == self.wake_word.lower() + " " + self.standby_word:
                        return "standby"
                    
                    if text == self.wake_word.lower() + " " +  self.shutdown_word:
                        return "sleep"

                    self.tts.text_to_speech(f"You said: {text}")
    
    def start(self):
        self.config = self.load_config('config.json')

        self.modules = self.load_modules(self.config['modules'])

        self.user = self.load_user()
        self.wake_word = self.get_wake_word()
        self.standby_word = self.get_standby_word()
        self.shutdown_word = self.get_shutdown_word()

        self.tts.text_to_speech(f"Hi {self.user.get('name')}. When you are ready to start, say {self.wake_word}")

        while True:
            audio = self.recognizer.listen()
            if audio:
                text = self.recognizer.recognize(audio)

                if self.wake_word.lower() in text.lower():
                    self.tts.text_to_speech(f"Hello {self.user.get('name')}.")
                    if self.modules != []: self.tts.text_to_speech(f"I have loaded the following modules: {', '.join(self.modules.keys())}")
                    self.tts.text_to_speech("What can I do for you?")
                    exit = self.enter()

                    if exit == "standby":
                        self.tts.text_to_speech("For now, I'm in standby mode. Call me when you're ready.")

                    if exit == "sleep":
                        self.tts.text_to_speech("Shutting down. Goodbye!")
                        break
                    

if __name__ == '__main__':
    Main_Functions.start()