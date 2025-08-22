import queue, sys, json, os, time
import sounddevice as sd
import vosk
import pyttsx3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import subprocess

WAKE_WORD = "hey bug"
EXIT_WORDS = ["stop listening", "goodbye bug"]

# ---- TTS ----
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---- Sentiment ----
sentiment = SentimentIntensityAnalyzer()
def analyze_mood(text):
    score = sentiment.polarity_scores(text)
    if score["compound"] > 0.3:
        return "positive"
    elif score["compound"] < -0.3:
        return "negative"
    return "neutral"

# ---- LLM (Ollama local) ----
def ask_llm(prompt, model="llama3.1"):
    """Calls local Ollama model. Requires Ollama installed & model pulled."""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True
        )
        return result.stdout.decode("utf-8").strip()
    except Exception as e:
        return f"(LLM error: {e})"

# ---- Vosk STT ----
q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen(model_path="models/vosk-model-small-en-us-0.15"):
    if not os.path.exists(model_path):
        raise RuntimeError("Download a Vosk model and unpack into ./models/")
    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, 16000)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        print("🎤 Listening… say 'hey bug' to wake me up.")
        buffer = ""
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if text:
                    yield text

# ---- Main Agent Loop ----
def run_bug():
    memory = []
    for text in listen():
        print("🗣️ You said:", text)

        if WAKE_WORD in text:
            speak("Hello, I'm Bug. How can I help you today?")
            while True:
                speak("I'm listening...")
                user_text = next(listen())
                print("USER:", user_text)

                if any(exit in user_text for exit in EXIT_WORDS):
                    speak("Goodbye!")
                    return

                mood = analyze_mood(user_text)
                context = "You are Bug, a kind, human-like teacher. "
                if mood == "negative":
                    context += "User seems upset; respond gently and encouragingly.\n"
                elif mood == "positive":
                    context += "User seems happy; keep the energy up!\n"

                context += "Conversation so far:\n"
                for turn in memory[-5:]:
                    context += f"{turn}\n"
                context += f"User: {user_text}\nBug:"

                reply = ask_llm(context)
                memory.append(f"User: {user_text}")
                memory.append(f"Bug: {reply}")

                print("BUG:", reply)
                speak(reply)

if __name__ == "__main__":
    run_bug()
