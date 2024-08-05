import speech_recognition as sr
import logging

# Configurazione del logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Creazione di un gestore per il file di log
file_handler = logging.FileHandler('speech_recognition.log')
file_handler.setLevel(logging.INFO)

# Creazione di un gestore per la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Creazione di un formatter e aggiunta al gestore
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Aggiunta dei gestori al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Classe di riconoscimento vocale
class SpeechRecognizer:
    def __init__(self, language="it-IT"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            logger.info("Listening...")
            try:
                audio = self.recognizer.listen(source)
                return audio
            except Exception as e:
                logger.error(f"Error during listening: {e}")
                return None
    
    def recognize(self, audio):
        if audio is None:
            return "No audio detected"

        try:
            logger.info("Recognizing...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            logger.error("Google Speech Recognition could not understand the audio.")
            return "Could not understand the audio."
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
            return "Could not request results from the service."
        
if __name__ == "__main__":
    recognizer = SpeechRecognizer(language='it-IT')

    text = ""

    while text.lower() != "addio":
        audio = recognizer.listen()
        if audio:
            text = recognizer.recognize(audio)
            print(f"Recognized text: {text}")