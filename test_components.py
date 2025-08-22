#!/usr/bin/env python3
"""
Component tests for Bug Voice Assistant
Tests individual components without requiring full audio setup
"""

import sys
import subprocess
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def test_sentiment():
    """Test sentiment analysis component"""
    print("🧪 Testing sentiment analysis...")
    
    sentiment = SentimentIntensityAnalyzer()
    
    test_cases = [
        ("I'm so happy today!", "positive"),
        ("This is terrible and I hate it", "negative"),
        ("The weather is okay", "neutral"),
        ("I'm really excited about this project!", "positive"),
        ("I feel sad and lonely", "negative")
    ]
    
    for text, expected in test_cases:
        score = sentiment.polarity_scores(text)
        
        if score["compound"] > 0.3:
            result = "positive"
        elif score["compound"] < -0.3:
            result = "negative"
        else:
            result = "neutral"
            
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{text}' → {result} (compound: {score['compound']:.2f})")

def test_tts():
    """Test TTS component"""
    print("\n🧪 Testing TTS...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("  ✅ pyttsx3 initialized successfully")
        
        # Test properties
        voices = engine.getProperty('voices')
        if voices:
            print(f"  ✅ Found {len(voices)} voice(s)")
        else:
            print("  ⚠️ No voices found")
            
        rate = engine.getProperty('rate')
        print(f"  ✅ Current speech rate: {rate}")
        
    except Exception as e:
        print(f"  ❌ TTS Error: {e}")

def test_ollama():
    """Test Ollama availability"""
    print("\n🧪 Testing Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  ✅ Ollama version: {result.stdout.strip()}")
        else:
            print(f"  ❌ Ollama error: {result.stderr}")
    except FileNotFoundError:
        print("  ❌ Ollama not found - install from https://ollama.ai/")
    except subprocess.TimeoutExpired:
        print("  ❌ Ollama command timed out")
    except Exception as e:
        print(f"  ❌ Ollama test failed: {e}")

def test_ollama_models():
    """Test available Ollama models"""
    print("\n🧪 Testing Ollama models...")
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Header + at least one model
                models = [line.split()[0] for line in lines[1:] if line.strip()]
                print(f"  ✅ Available models: {', '.join(models)}")
                if 'llama3.1' in models:
                    print("  ✅ Default model (llama3.1) is available")
                else:
                    print("  ⚠️ Default model (llama3.1) not found")
                    print("    Run: ollama pull llama3.1")
            else:
                print("  ⚠️ No models installed")
                print("    Run: ollama pull llama3.1")
        else:
            print(f"  ❌ Failed to list models: {result.stderr}")
    except Exception as e:
        print(f"  ❌ Model test failed: {e}")

def test_audio():
    """Test audio dependencies"""
    print("\n🧪 Testing audio dependencies...")
    try:
        import sounddevice as sd
        print("  ✅ sounddevice imported successfully")
        
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        print(f"  ✅ Found {len(input_devices)} input device(s)")
        print(f"  ✅ Found {len(output_devices)} output device(s)")
        
        if not input_devices:
            print("  ⚠️ No input devices found - microphone may not work")
        if not output_devices:
            print("  ⚠️ No output devices found - audio output may not work")
            
    except Exception as e:
        print(f"  ❌ Audio test failed: {e}")

def test_vosk_model():
    """Test Vosk model availability"""
    print("\n🧪 Testing Vosk model...")
    import os
    
    model_path = "models/vosk-model-small-en-us-0.15"
    if os.path.exists(model_path):
        print(f"  ✅ Vosk model found at {model_path}")
        try:
            import vosk
            model = vosk.Model(model_path)
            print("  ✅ Vosk model loaded successfully")
        except Exception as e:
            print(f"  ❌ Failed to load Vosk model: {e}")
    else:
        print(f"  ❌ Vosk model not found at {model_path}")
        print("    Run: python setup.py")

if __name__ == "__main__":
    print("🐛 Bug Voice Assistant - Component Tests")
    print("=" * 50)
    
    test_sentiment()
    test_tts()
    test_audio()
    test_vosk_model()
    test_ollama()
    test_ollama_models()
    
    print("\n" + "=" * 50)
    print("🏁 Tests complete!")
    print("\nIf all components show ✅, you're ready to run Bug!")
    print("Otherwise, check the troubleshooting section in README.md")
