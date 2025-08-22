#!/usr/bin/env python3
"""
Bug Voice Assistant - Enhanced Version
Interactive voice assistant with improved error handling and features
"""

import queue
import sys
import json
import os
import time
import logging
import signal
import threading
from typing import Generator, Optional, List, Tuple

import sounddevice as sd
import vosk
import pyttsx3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import subprocess

import load_env  # Load .env file
from config import *

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bug_assistant.log')
    ]
)
logger = logging.getLogger(__name__)

class VoiceAssistant:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.is_running = True
        self.conversation_memory: List[str] = []
        self.current_mood = "neutral"
        
        # Initialize components
        self._init_tts()
        self._init_sentiment()
        self._init_vosk()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("Shutdown signal received, stopping assistant...")
        self.is_running = False
        self.is_listening = False
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', TTS_RATE)
            self.tts_engine.setProperty('volume', TTS_VOLUME)
            
            # Try to use a more natural voice if available
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voices or specific voices for a friendlier sound
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                        
            logger.info("TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            sys.exit(1)
    
    def _init_sentiment(self):
        """Initialize sentiment analyzer"""
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            logger.info("Sentiment analyzer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analyzer: {e}")
            sys.exit(1)
    
    def _init_vosk(self):
        """Initialize Vosk speech recognition"""
        try:
            if not os.path.exists(VOSK_MODEL_PATH):
                logger.error(f"Vosk model not found at {VOSK_MODEL_PATH}")
                logger.error("Please run: python setup.py")
                sys.exit(1)
            
            self.vosk_model = vosk.Model(VOSK_MODEL_PATH)
            self.vosk_recognizer = vosk.KaldiRecognizer(self.vosk_model, SAMPLE_RATE)
            logger.info(f"Vosk model loaded from {VOSK_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to initialize Vosk: {e}")
            sys.exit(1)
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Audio input callback"""
        if status:
            logger.warning(f"Audio status: {status}")
        if self.is_listening:
            self.audio_queue.put(bytes(indata))
    
    def speak(self, text: str, interrupt: bool = False):
        """Speak text using TTS"""
        if not text.strip():
            return
            
        try:
            logger.info(f"Speaking: {text}")
            if interrupt:
                self.tts_engine.stop()
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"🗣️ Bug: {text}")  # Fallback to text output
    
    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        try:
            scores = self.sentiment_analyzer.polarity_scores(text)
            compound = scores['compound']
            
            if compound >= POSITIVE_THRESHOLD:
                return "positive"
            elif compound <= NEGATIVE_THRESHOLD:
                return "negative"
            else:
                return "neutral"
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return "neutral"
    
    def ask_llm(self, prompt: str, model: str = OLLAMA_MODEL) -> str:
        """Get response from Ollama LLM"""
        try:
            logger.debug(f"Asking LLM: {prompt[:100]}...")
            
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode("utf-8"),
                capture_output=True,
                timeout=OLLAMA_TIMEOUT
            )
            
            if result.returncode == 0:
                response = result.stdout.decode("utf-8").strip()
                logger.debug(f"LLM response: {response[:100]}...")
                return response
            else:
                error = result.stderr.decode("utf-8").strip()
                logger.error(f"Ollama error: {error}")
                return "I'm having trouble thinking right now. Could you try again?"
                
        except subprocess.TimeoutExpired:
            logger.error("Ollama request timed out")
            return "Sorry, I'm taking too long to think. Let me try to be quicker next time."
        except FileNotFoundError:
            logger.error("Ollama not found")
            return "I need Ollama to be installed to answer that question."
        except Exception as e:
            logger.error(f"LLM error: {e}")
            return "I encountered an error while thinking about that."
    
    def listen_for_speech(self) -> Generator[str, None, None]:
        """Listen for speech and yield recognized text"""
        try:
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype=AUDIO_DTYPE,
                channels=AUDIO_CHANNELS,
                callback=self._audio_callback
            ):
                logger.info("Audio stream started")
                
                while self.is_running:
                    try:
                        data = self.audio_queue.get(timeout=1.0)
                        
                        if self.vosk_recognizer.AcceptWaveform(data):
                            result = json.loads(self.vosk_recognizer.Result())
                            text = result.get("text", "").strip().lower()
                            
                            if text:
                                logger.info(f"Recognized: '{text}'")
                                yield text
                                
                    except queue.Empty:
                        continue
                    except Exception as e:
                        logger.error(f"Speech recognition error: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Audio stream error: {e}")
            return
    
    def build_context(self, user_input: str) -> str:
        """Build context for LLM including conversation history and mood"""
        # Analyze current mood
        self.current_mood = self.analyze_sentiment(user_input)
        
        # Build context
        context_parts = [SYSTEM_PROMPT]
        
        # Add mood context
        if self.current_mood in MOOD_PROMPTS:
            context_parts.append(MOOD_PROMPTS[self.current_mood])
        
        # Add conversation history
        if self.conversation_memory:
            context_parts.append("Recent conversation:")
            for turn in self.conversation_memory[-MAX_MEMORY_TURNS:]:
                context_parts.append(turn)
        
        # Add current user input
        context_parts.append(f"User: {user_input}")
        context_parts.append("Bug:")
        
        return "\n".join(context_parts)
    
    def add_to_memory(self, user_input: str, assistant_response: str):
        """Add conversation turn to memory"""
        self.conversation_memory.append(f"User: {user_input}")
        self.conversation_memory.append(f"Bug: {assistant_response}")
        
        # Keep memory size manageable
        if len(self.conversation_memory) > MAX_MEMORY_TURNS * 2:
            self.conversation_memory = self.conversation_memory[-MAX_MEMORY_TURNS * 2:]
    
    def wait_for_wake_word(self):
        """Wait for wake word in background listening mode"""
        logger.info(f"🎤 Listening for wake word: '{WAKE_WORD}'")
        print(f"🎤 Listening for wake word: '{WAKE_WORD}' (Ctrl+C to exit)")
        
        self.is_listening = True
        
        for text in self.listen_for_speech():
            if not self.is_running:
                break
                
            if WAKE_WORD in text:
                logger.info("Wake word detected!")
                print("🐛 Wake word detected!")
                return True
        
        return False
    
    def conversation_loop(self):
        """Main conversation loop after wake word"""
        self.speak("Hello! I'm Bug, your voice assistant. How can I help you today?")
        
        logger.info("Entering conversation mode")
        conversation_start = time.time()
        
        while self.is_running:
            try:
                print("🎤 Listening... (speak now)")
                self.speak("I'm listening...", interrupt=False)
                
                # Get next speech input
                speech_detected = False
                speech_timeout = time.time() + RESPONSE_TIMEOUT
                
                for text in self.listen_for_speech():
                    if not self.is_running:
                        return
                    
                    speech_detected = True
                    print(f"👤 You: {text}")
                    
                    # Check for exit commands
                    if any(exit_cmd in text for exit_cmd in EXIT_WORDS):
                        self.speak("Goodbye! It was nice talking with you.")
                        logger.info("Exit command received")
                        return
                    
                    # Generate response
                    print("🤔 Thinking...")
                    context = self.build_context(text)
                    response = self.ask_llm(context)
                    
                    # Add to memory and respond
                    self.add_to_memory(text, response)
                    print(f"🐛 Bug: {response}")
                    self.speak(response)
                    
                    break
                
                if not speech_detected and time.time() > speech_timeout:
                    logger.info("No speech detected, continuing to listen")
                    
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Conversation error: {e}")
                self.speak("I encountered an error. Let me try again.")
    
    def run(self):
        """Main run loop"""
        logger.info("Bug Voice Assistant starting...")
        print("🐛 Bug Voice Assistant")
        print("=" * 30)
        
        try:
            while self.is_running:
                # Wait for wake word
                if self.wait_for_wake_word():
                    # Enter conversation mode
                    self.conversation_loop()
                    
                    # Reset for next wake word
                    logger.info("Returning to wake word listening mode")
                    print("\n" + "="*30)
                    
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt - shutting down")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Clean shutdown"""
        logger.info("Shutting down Bug Voice Assistant")
        self.is_running = False
        self.is_listening = False
        
        try:
            self.tts_engine.stop()
        except:
            pass
            
        print("👋 Bug Voice Assistant stopped")

def main():
    """Main entry point"""
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()
