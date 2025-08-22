# 🐛 Bug Voice Assistant

An interactive voice assistant powered by Vosk (STT), Ollama (LLM), pyttsx3 (TTS), and VADER sentiment analysis.

## Features

- 🎤 **Wake word activation**: Say "hey bug" to activate
- 🗣️ **Speech-to-text**: Uses Vosk for offline speech recognition
- 🤖 **AI responses**: Powered by local Ollama LLM (llama3.1 by default)
- 🎵 **Text-to-speech**: Natural voice responses using pyttsx3
- 😊 **Sentiment analysis**: Adapts responses based on user mood using VADER
- 💭 **Conversation memory**: Maintains context for natural conversations
- 🔚 **Exit commands**: Say "stop listening" or "goodbye bug" to exit

## Prerequisites

1. **Python 3.7+**
2. **Ollama**: Install from [ollama.ai](https://ollama.ai/)
3. **System audio dependencies**: For speech recognition and TTS

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install portaudio19-dev espeak espeak-data
```

**macOS:**
```bash
brew install portaudio espeak
```

## Quick Start

### Option 1: Automated Installation (Recommended)
```bash
git clone <repository-url>
cd bugai
./install.sh
```

### Option 2: Manual Installation
```bash
git clone <repository-url>
cd bugai
pip install -r requirements.txt
python setup.py  # Downloads Vosk model
```

**Install Ollama model:**
```bash
ollama pull llama3.1
```

**Run the assistant:**

**Basic version:**
```bash
python bug_assistant.py
# or
make run
```

**Enhanced version (recommended):**
```bash
python bug_assistant_enhanced.py
# or
make run-enhanced
```

**Text-only demo (no audio required):**
```bash
python demo.py
# or
make demo
```

**Interact:**
   - **Voice mode**: Say "hey bug" to wake up the assistant
   - **Demo mode**: Type your messages directly
   - Have a conversation
   - Say "goodbye bug", "stop listening", or "exit" to quit

## Versions

### Basic Version (`bug_assistant.py`)
- Simple implementation following the original code structure
- Direct Vosk integration for speech recognition
- Basic conversation flow
- Suitable for understanding the core concepts

### Enhanced Version (`bug_assistant_enhanced.py`) ⭐ Recommended
- Improved error handling and logging
- Configurable settings via environment variables
- Better audio management and graceful shutdown
- Enhanced conversation memory management
- More robust LLM integration with timeouts
- Detailed logging to file and console
- Professional code structure with classes

### Demo Version (`demo.py`)
- Text-only interface (no audio required)
- Perfect for testing LLM integration
- Great for development and debugging
- Same conversation logic as full versions

## Configuration

### Enhanced Version Configuration (Recommended)

Copy the example environment file and customize:
```bash
cp .env.example .env
# Edit .env with your preferences
```

Available environment variables:
- `BUG_WAKE_WORD`: Custom wake word (default: "hey bug")
- `BUG_OLLAMA_MODEL`: Ollama model to use (default: "llama3.1")
- `BUG_OLLAMA_TIMEOUT`: LLM response timeout in seconds (default: 30)
- `BUG_POSITIVE_THRESHOLD`: Positive sentiment threshold (default: 0.3)
- `BUG_NEGATIVE_THRESHOLD`: Negative sentiment threshold (default: -0.3)
- `BUG_MAX_MEMORY`: Conversation turns to remember (default: 10)
- `BUG_TTS_RATE`: Speech rate for TTS (default: 200)
- `BUG_TTS_VOLUME`: TTS volume (default: 0.9)

### Basic Version Configuration

Edit the constants in `bug_assistant.py`:

**Changing the LLM Model:**
```python
reply = ask_llm(context, model="llama2")  # Use different model
```

**Adjusting Wake Word:**
```python
WAKE_WORD = "hey assistant"  # Custom wake word
```

**Sentiment Thresholds:**
```python
if score["compound"] > 0.5:  # More strict positive threshold
    return "positive"
```

## Architecture

```
User Speech → Vosk STT → Sentiment Analysis → Context Building → Ollama LLM → pyttsx3 TTS → Audio Output
                    ↓
               Wake Word Detection
                    ↓
               Conversation Memory
```

## Dependencies

- `sounddevice`: Audio I/O
- `vosk`: Speech-to-text recognition
- `pyttsx3`: Text-to-speech synthesis
- `vaderSentiment`: Sentiment analysis
- `subprocess`: Ollama integration

## Troubleshooting

**Audio Issues:**
- Check microphone permissions
- Verify audio device selection with `python -m sounddevice`

**Ollama Issues:**
- Ensure Ollama service is running: `ollama serve`
- Verify model is installed: `ollama list`

**Model Issues:**
- Re-run setup: `python setup.py`
- Check models directory exists and contains Vosk model

## License

MIT License
