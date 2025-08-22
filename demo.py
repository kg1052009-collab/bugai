#!/usr/bin/env python3
"""
Bug Voice Assistant Demo (Text-only version)
For testing without audio components
"""

import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import subprocess

import load_env  # Load .env file
from config import *

class BugDemo:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.conversation_memory = []
        print("🐛 Bug Voice Assistant - Demo Mode")
        print("=" * 40)
        print("Type 'quit' or 'exit' to stop")
        print()
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= POSITIVE_THRESHOLD:
            return "positive"
        elif compound <= NEGATIVE_THRESHOLD:
            return "negative"
        else:
            return "neutral"
    
    def ask_llm(self, prompt, model=OLLAMA_MODEL):
        """Get response from Ollama LLM"""
        try:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode("utf-8"),
                capture_output=True,
                timeout=OLLAMA_TIMEOUT
            )
            
            if result.returncode == 0:
                return result.stdout.decode("utf-8").strip()
            else:
                return f"(LLM Error: {result.stderr.decode('utf-8').strip()})"
                
        except subprocess.TimeoutExpired:
            return "(LLM timed out)"
        except FileNotFoundError:
            return "(Ollama not found - please install Ollama)"
        except Exception as e:
            return f"(LLM error: {e})"
    
    def build_context(self, user_input):
        """Build context for LLM"""
        mood = self.analyze_sentiment(user_input)
        
        context_parts = [SYSTEM_PROMPT]
        
        if mood in MOOD_PROMPTS:
            context_parts.append(MOOD_PROMPTS[mood])
        
        if self.conversation_memory:
            context_parts.append("Recent conversation:")
            for turn in self.conversation_memory[-MAX_MEMORY_TURNS:]:
                context_parts.append(turn)
        
        context_parts.append(f"User: {user_input}")
        context_parts.append("Bug:")
        
        return "\n".join(context_parts)
    
    def run(self):
        """Run the demo"""
        print("🐛 Bug: Hello! I'm Bug, your voice assistant. How can I help you today?")
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'goodbye']:
                    print("🐛 Bug: Goodbye! It was nice talking with you.")
                    break
                
                # Analyze sentiment
                mood = self.analyze_sentiment(user_input)
                mood_emoji = {"positive": "😊", "negative": "😔", "neutral": "😐"}
                print(f"   (Detected mood: {mood} {mood_emoji.get(mood, '')})")
                
                # Generate response
                print("   🤔 Thinking...")
                context = self.build_context(user_input)
                response = self.ask_llm(context)
                
                # Add to memory
                self.conversation_memory.append(f"User: {user_input}")
                self.conversation_memory.append(f"Bug: {response}")
                
                print(f"🐛 Bug: {response}")
                
            except KeyboardInterrupt:
                print("\n🐛 Bug: Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    demo = BugDemo()
    demo.run()
