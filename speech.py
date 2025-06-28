import pyttsx3
import speech_recognition as sr
import threading

class SpeechProcessor:
    def __init__(self, message_callback=None):
        self.message_callback = message_callback or print
        self.setup_speech()
    
    def setup_speech(self):
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        except Exception as e:
            self.message_callback(f"⚠️ Speech setup failed: {str(e)}")
    
    def speak(self, text):
        def tts():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
        
        threading.Thread(target=tts, daemon=True).start()
    
    def listen(self):
        try:
            self.message_callback("🎤 Listening...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            self.message_callback("⏰ No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            self.message_callback("❌ Could not understand the audio. Please speak clearly.")
            return None
        except Exception as e:
            self.message_callback(f"❌ Voice recognition error: {str(e)}")
            return None
