# 🚀 Quick Start Guide - Bug Voice Assistant

## Instant Demo (30 seconds)

```bash
# 1. Set up environment (one-time)
python3 -m venv venv
source venv/bin/activate
pip install vaderSentiment

# 2. Try the text demo immediately
python demo.py
```

Type messages to chat with Bug! 🐛

## Example Conversation

```
🐛 Bug: Hello! I'm Bug, your voice assistant. How can I help you today?

👤 You: I'm feeling really excited today!
   (Detected mood: positive 😊)
   🤔 Thinking...
🐛 Bug: That's wonderful! Your positive energy is contagious...

👤 You: I'm having a bad day
   (Detected mood: negative 😔)  
   🤔 Thinking...
🐛 Bug: I'm sorry you're having a tough time...

👤 You: quit
🐛 Bug: Goodbye! It was nice talking with you.
```

## Full Setup (for voice features)

```bash
# Run the automated installer
./install.sh

# Install Ollama for AI responses
# Visit: https://ollama.ai/

# Install system audio dependencies
sudo apt-get install portaudio19-dev espeak espeak-data  # Ubuntu
# or
brew install portaudio espeak  # macOS

# Pull AI model
ollama pull llama3.1

# Test everything
make test

# Run full voice assistant
make run-enhanced
```

## Available Versions

- **`demo.py`** - Text chat (works immediately)
- **`bug_assistant.py`** - Basic voice assistant  
- **`bug_assistant_enhanced.py`** - Full-featured version

## Commands

- `make demo` - Start text demo
- `make test` - Check all components
- `make help` - Show all commands

Say "hey bug" to activate voice mode!
Say "goodbye bug" or "exit" to quit.

---
**Pro Tip**: Start with `python demo.py` to see Bug's personality, then upgrade to voice features when ready! 🎤
