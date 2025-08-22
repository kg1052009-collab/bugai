#!/usr/bin/env python3
"""
Setup script for Bug Voice Assistant
Downloads required Vosk model if not present
"""

import os
import urllib.request
import zipfile
import sys

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR = "models"
MODEL_PATH = "models/vosk-model-small-en-us-0.15"

def download_model():
    """Download and extract the Vosk model"""
    if os.path.exists(MODEL_PATH):
        print(f"✅ Model already exists at {MODEL_PATH}")
        return
    
    print("📥 Downloading Vosk model...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    zip_path = os.path.join(MODEL_DIR, "model.zip")
    
    try:
        urllib.request.urlretrieve(MODEL_URL, zip_path)
        print("📦 Extracting model...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(MODEL_DIR)
        
        os.remove(zip_path)
        print(f"✅ Model installed at {MODEL_PATH}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        sys.exit(1)

def check_ollama():
    """Check if Ollama is installed"""
    try:
        import subprocess
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
        else:
            print("⚠️ Ollama not found. Please install from https://ollama.ai/")
    except FileNotFoundError:
        print("⚠️ Ollama not found. Please install from https://ollama.ai/")

if __name__ == "__main__":
    print("🐛 Bug Voice Assistant Setup")
    print("=" * 30)
    
    download_model()
    check_ollama()
    
    print("\n🎯 Setup complete!")
    print("Run: python bug_assistant.py")
