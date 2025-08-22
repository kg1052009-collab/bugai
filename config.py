"""
Configuration settings for Bug Voice Assistant
"""

import os

# Audio settings
SAMPLE_RATE = 16000
BLOCK_SIZE = 8000
AUDIO_DTYPE = "int16"
AUDIO_CHANNELS = 1

# Wake word and exit commands
WAKE_WORD = os.getenv("BUG_WAKE_WORD", "hey bug")
EXIT_WORDS = ["stop listening", "goodbye bug", "exit", "quit"]

# Model settings
VOSK_MODEL_PATH = os.getenv("BUG_VOSK_MODEL", "models/vosk-model-small-en-us-0.15")
OLLAMA_MODEL = os.getenv("BUG_OLLAMA_MODEL", "llama3.1")
OLLAMA_TIMEOUT = int(os.getenv("BUG_OLLAMA_TIMEOUT", "30"))

# Sentiment analysis thresholds
POSITIVE_THRESHOLD = float(os.getenv("BUG_POSITIVE_THRESHOLD", "0.3"))
NEGATIVE_THRESHOLD = float(os.getenv("BUG_NEGATIVE_THRESHOLD", "-0.3"))

# Conversation settings
MAX_MEMORY_TURNS = int(os.getenv("BUG_MAX_MEMORY", "10"))
RESPONSE_TIMEOUT = float(os.getenv("BUG_RESPONSE_TIMEOUT", "5.0"))

# TTS settings
TTS_RATE = int(os.getenv("BUG_TTS_RATE", "200"))
TTS_VOLUME = float(os.getenv("BUG_TTS_VOLUME", "0.9"))

# System prompts
SYSTEM_PROMPT = """You are Bug, a kind, helpful, and human-like AI assistant. 
Keep your responses conversational, friendly, and concise (1-3 sentences usually).
You're designed to be helpful while maintaining a warm, approachable personality."""

MOOD_PROMPTS = {
    "positive": "The user seems happy or excited! Keep the positive energy going.",
    "negative": "The user seems upset or frustrated. Respond with empathy and encouragement.",
    "neutral": "The user seems calm and neutral."
}
