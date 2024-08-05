import speech_recognition as sr
from core.logger_config import setup_logger

logger = setup_logger(__name__, 'logs/speech_recognition.log')

# Classe di riconoscimento vocale
class SpeechRecognizer:
    def __init__(self, language="en-US"):
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
    recognizer = SpeechRecognizer(language="en-US")

    text = ""

    while text.lower() != "addio":
        audio = recognizer.listen()
        if audio:
            text = recognizer.recognize(audio)
            print(f"Recognized text: {text}")