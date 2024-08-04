import speech_recognition as sr
import os

class SpeechRecognizer:
    def __init__(self, language="it-IT"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                print("Listening...")
                audio = self.recognizer.listen(source)
                return audio
            except Exception:
                return None
    
    def recognize(self, audio):
        if audio is None:
            return "No audio detected"

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return "Could not request results from the service."
        
if __name__ == "__main__":
    recognizer = SpeechRecognizer(language='it-IT')

    text = ""

    while text.lower() != "addio":
        audio = recognizer.listen()
        if audio:
            text = recognizer.recognize(audio)
            print(f"Recognized text: {text}")