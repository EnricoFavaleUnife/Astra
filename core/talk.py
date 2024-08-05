import os
from gtts import gTTS
import pygame
import tempfile
from core.logger_config import setup_logger

# Configurazione del logger
logger = setup_logger(__name__, 'logs/talk.log')

class TextToSpeech:
    def __init__(self, language="en-US"):
        self.language = language
        pygame.mixer.init()

    def text_to_speech(self, text):
        try:
            logger.info("Converting text to speech...")
            tts = gTTS(text=text, lang=self.language, tld="us", slow=False, lang_check=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name
                tts.save(temp_filename)
                logger.info(f"Audio saved as temporary file {temp_filename}")

            self.play_audio(temp_filename)

            os.remove(temp_filename)
            logger.info(f"Temporary file {temp_filename} deleted")
            
        except Exception as e:
            logger.error(f"Error during text to speech conversion: {e}")
            return None

    def play_audio(self, file='output.mp3'):
        try:
            logger.info(f"Playing audio file {file}")
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            logger.error(f"Error during audio playback: {e}")

# Esempio di utilizzo
if __name__ == "__main__":
    tts = TextToSpeech(language='en')
    tts.text_to_speech("Hi, how can I help you?")
    
