"""
Voice Feedback Module
Handles text-to-speech and audio feedback
"""

import threading
import time
import logging
from typing import Optional, Callable
import queue

# Initialize TTS flags
TTS_AVAILABLE = False
GTTS_AVAILABLE = False

# Try to import text-to-speech libraries
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    pass

try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
except ImportError:
    pass

class VoiceFeedback:
    """Text-to-speech feedback system"""
    
    def __init__(self, voice_enabled: bool = True, voice_rate: int = 150):
        self.voice_enabled = voice_enabled
        self.voice_rate = voice_rate
        self.tts_engine = None
        self.feedback_queue = queue.Queue()
        self.is_speaking = False
        
        # Initialize TTS engines
        self._init_tts_engines()
        
        # Start feedback thread
        if self.voice_enabled:
            self.feedback_thread = threading.Thread(target=self._feedback_loop, daemon=True)
            self.feedback_thread.start()
    
    def _init_tts_engines(self):
        """Initialize available text-to-speech engines"""
        global TTS_AVAILABLE, GTTS_AVAILABLE
        
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.voice_rate)
                
                # Get available voices
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Try to set a female voice if available
                    for voice in voices:
                        if 'female' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                    else:
                        # Use first available voice
                        self.tts_engine.setProperty('voice', voices[0].id)
                
                logging.info("PyTTSx3 TTS engine initialized")
            except Exception as e:
                logging.error(f"Failed to initialize PyTTSx3: {e}")
                TTS_AVAILABLE = False
        
        if GTTS_AVAILABLE:
            try:
                pygame.mixer.init()
                logging.info("gTTS TTS engine initialized")
            except Exception as e:
                logging.error(f"Failed to initialize gTTS: {e}")
                GTTS_AVAILABLE = False
    
    def speak(self, text: str, priority: int = 1):
        """Speak text with priority (lower = higher priority)"""
        if not self.voice_enabled:
            return
            
        self.feedback_queue.put((priority, text))
    
    def speak_immediate(self, text: str):
        """Speak text immediately (interrupts current speech)"""
        if not self.voice_enabled:
            return
            
        # Clear queue and speak immediately
        while not self.feedback_queue.empty():
            try:
                self.feedback_queue.get_nowait()
            except queue.Empty:
                break
        
        self.feedback_queue.put((0, text))  # Highest priority
    
    def _feedback_loop(self):
        """Main feedback loop for processing speech queue"""
        while self.voice_enabled:
            try:
                # Get next feedback item
                priority, text = self.feedback_queue.get(timeout=1)
                
                if text:
                    self._speak_text(text)
                    
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Feedback loop error: {e}")
    
    def _speak_text(self, text: str):
        """Actually speak the text using available TTS engine"""
        self.is_speaking = True
        
        try:
            if TTS_AVAILABLE and self.tts_engine:
                self._speak_pyttsx3(text)
            elif GTTS_AVAILABLE:
                self._speak_gtts(text)
            else:
                logging.warning("No TTS engine available")
                
        except Exception as e:
            logging.error(f"Speech error: {e}")
        finally:
            self.is_speaking = False
    
    def _speak_pyttsx3(self, text: str):
        """Speak using PyTTSx3"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logging.error(f"PyTTSx3 speech error: {e}")
    
    def _speak_gtts(self, text: str):
        """Speak using gTTS"""
        try:
            # Create temporary audio file
            tts = gTTS(text=text, lang='en', slow=False)
            temp_file = f"temp_speech_{int(time.time())}.mp3"
            tts.save(temp_file)
            
            # Play audio
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Clean up
            pygame.mixer.music.unload()
            import os
            os.remove(temp_file)
            
        except Exception as e:
            logging.error(f"gTTS speech error: {e}")
    
    def set_voice_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.voice_rate = rate
        if TTS_AVAILABLE and self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
    
    def set_voice_volume(self, volume: float):
        """Set voice volume (0.0 to 1.0)"""
        if TTS_AVAILABLE and self.tts_engine:
            self.tts_engine.setProperty('volume', max(0.0, min(1.0, volume)))
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        if TTS_AVAILABLE and self.tts_engine:
            return self.tts_engine.getProperty('voices')
        return []
    
    def set_voice(self, voice_id: str):
        """Set specific voice by ID"""
        if TTS_AVAILABLE and self.tts_engine:
            self.tts_engine.setProperty('voice', voice_id)
    
    def enable_voice(self):
        """Enable voice feedback"""
        self.voice_enabled = True
        if not hasattr(self, 'feedback_thread') or not self.feedback_thread.is_alive():
            self.feedback_thread = threading.Thread(target=self._feedback_loop, daemon=True)
            self.feedback_thread.start()
    
    def disable_voice(self):
        """Disable voice feedback"""
        self.voice_enabled = False
    
    def is_available(self) -> bool:
        """Check if any TTS engine is available"""
        return TTS_AVAILABLE or GTTS_AVAILABLE
    
    def get_status(self) -> dict:
        """Get TTS engine status"""
        return {
            "voice_enabled": self.voice_enabled,
            "is_speaking": self.is_speaking,
            "pyttsx3_available": TTS_AVAILABLE,
            "gtts_available": GTTS_AVAILABLE,
            "any_available": self.is_available(),
            "voice_rate": self.voice_rate
        }
    
    def cleanup(self):
        """Cleanup resources"""
        self.voice_enabled = False
        if TTS_AVAILABLE and self.tts_engine:
            self.tts_engine.stop()
        if GTTS_AVAILABLE:
            pygame.mixer.quit() 