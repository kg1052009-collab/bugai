#!/bin/bash

echo "🐛 Bug Voice Assistant - Installation Script"
echo "============================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Run setup to download Vosk model
echo "📥 Downloading Vosk model..."
python setup.py

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found: $(ollama --version)"
    
    # Ask user if they want to pull the model
    read -p "📥 Would you like to pull the llama3.1 model? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📥 Pulling llama3.1 model..."
        ollama pull llama3.1
    fi
else
    echo "⚠️ Ollama not found. Please install from https://ollama.ai/"
fi

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env configuration file..."
    cp .env.example .env
    echo "✅ Configuration file created at .env"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Test components: make test"
echo "3. Try the demo: make demo"
echo "4. Run the assistant: make run-enhanced"
echo ""
echo "For more information, see README.md"
