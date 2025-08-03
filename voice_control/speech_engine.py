"""
Speech Engine Module
Handles speech recognition with multiple fallback options
"""

import threading
import time
from typing import Optional, Callable, Dict, Any
import logging

# Fix for Python 3.13 aifc module issue
try:
    from . import aifc_fix
except ImportError:
    pass

# Initialize speech recognition flags
SPEECH_AVAILABLE = False
WHISPER_AVAILABLE = False

# Try to import speech recognition with fallback
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Speech recognition not available: {e}")

# Try to import alternative speech recognition
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    pass

class SpeechEngine:
    """Advanced speech recognition engine with multiple backends"""
    
    def __init__(self, wake_words: list = None, callback: Callable = None):
        self.wake_words = wake_words or ["xizo", "hey xizo", "listen xizo"]
        self.callback = callback
        self.is_listening = False
        self.is_running = True
        self.recognizer = None
        self.microphone = None
        self.backend = "google"  # google, whisper, offline
        
        # Initialize available backends
        self._init_speech_recognition()
        
    def _init_speech_recognition(self):
        """Initialize speech recognition backends"""
        global SPEECH_AVAILABLE, WHISPER_AVAILABLE
        
        if SPEECH_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                self._adjust_for_ambient_noise()
                logging.info("Google Speech Recognition initialized")
            except Exception as e:
                logging.error(f"Failed to initialize Google Speech Recognition: {e}")
                SPEECH_AVAILABLE = False
                
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model("base")
                logging.info("Whisper model loaded")
            except Exception as e:
                logging.error(f"Failed to load Whisper model: {e}")
                WHISPER_AVAILABLE = False
    
    def _adjust_for_ambient_noise(self):
        """Adjust recognizer for ambient noise"""
        if not self.recognizer or not self.microphone:
            return
            
        try:
            logging.info("Adjusting for ambient noise... Please be quiet.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Ambient noise adjustment complete.")
        except Exception as e:
            logging.error(f"Ambient noise adjustment failed: {e}")
    
    def start_listening(self):
        """Start listening for voice commands"""
        if not self._has_working_backend():
            logging.error("No speech recognition backend available")
            return False
            
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        logging.info("Started listening for voice commands")
        return True
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        logging.info("Stopped listening for voice commands")
    
    def _has_working_backend(self) -> bool:
        """Check if any speech recognition backend is available"""
        return SPEECH_AVAILABLE or WHISPER_AVAILABLE
    
    def _listen_loop(self):
        """Main listening loop"""
        while self.is_listening and self.is_running:
            try:
                text = self._listen_for_speech()
                if text:
                    self._process_speech(text)
            except Exception as e:
                logging.error(f"Listening error: {e}")
                time.sleep(0.1)
    
    def _listen_for_speech(self) -> Optional[str]:
        """Listen for speech and return recognized text"""
        if SPEECH_AVAILABLE and self.recognizer and self.microphone:
            return self._listen_google()
        elif WHISPER_AVAILABLE:
            return self._listen_whisper()
        return None
    
    def _listen_google(self) -> Optional[str]:
        """Listen using Google Speech Recognition"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio).lower()
            logging.info(f"Google recognized: {text}")
            return text
        except sr.UnknownValueError:
            pass  # No speech detected
        except sr.RequestError as e:
            logging.error(f"Google Speech Recognition error: {e}")
        except Exception as e:
            logging.error(f"Google listening error: {e}")
        return None
    
    def _listen_whisper(self) -> Optional[str]:
        """Listen using Whisper (offline)"""
        try:
            # This would need audio recording implementation
            # For now, return None as placeholder
            logging.info("Whisper listening not yet implemented")
            return None
        except Exception as e:
            logging.error(f"Whisper listening error: {e}")
        return None
    
    def _process_speech(self, text: str):
        """Process recognized speech text"""
        # Check for wake words
        if any(wake_word in text.lower() for wake_word in self.wake_words):
            # Remove wake word from text
            for wake_word in self.wake_words:
                text = text.replace(wake_word, "").strip()
            
            if text and self.callback:
                self.callback(text)
    
    def add_wake_word(self, wake_word: str):
        """Add a new wake word"""
        if wake_word not in self.wake_words:
            self.wake_words.append(wake_word.lower())
            logging.info(f"Added wake word: {wake_word}")
    
    def remove_wake_word(self, wake_word: str):
        """Remove a wake word"""
        if wake_word in self.wake_words:
            self.wake_words.remove(wake_word.lower())
            logging.info(f"Removed wake word: {wake_word}")
    
    def get_available_backends(self) -> Dict[str, bool]:
        """Get status of available speech recognition backends"""
        return {
            "google": SPEECH_AVAILABLE,
            "whisper": WHISPER_AVAILABLE,
            "working": self._has_working_backend()
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.is_running = False
        self.is_listening = False 