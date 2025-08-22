.PHONY: help install setup test run demo clean

help:
	@echo "🐛 Bug Voice Assistant - Available Commands"
	@echo "=========================================="
	@echo "install      - Install Python dependencies"
	@echo "setup        - Download Vosk model and check Ollama"
	@echo "test         - Test all components"
	@echo "run          - Start the basic voice assistant"
	@echo "run-enhanced - Start the enhanced voice assistant"
	@echo "demo         - Run text-only demo (no audio required)"
	@echo "clean        - Remove downloaded models and cache"
	@echo "ollama       - Pull default Ollama model"

install:
	pip install -r requirements.txt

setup: install
	python setup.py

test:
	python test_components.py

run:
	python bug_assistant.py

run-enhanced:
	python bug_assistant_enhanced.py

demo:
	python demo.py

ollama:
	ollama pull llama3.1

clean:
	rm -rf models/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
