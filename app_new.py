
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import speech_recognition as sr
import pyttsx3 
import sys

# Your OpenAI/Google API keys for the conversation
# from openai import OpenAI
# client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

app = Flask(__name__)

# --- Core assistant logic from your assistant.py file ---
listener = sr.Recognizer()
engine = pyttsx3.init()

def speak_response(text):
    # This function is not used, as Twilio handles TTS with <Say>
    print(f"Assistant: {text}")

def process_command(command):
    if "hello" in command:
        return "Hello to you too!"
    elif "how are you" in command:
        return "I am doing well, thank you for asking."
    elif "what is your name" in command:
        return "My name is Assistant."
    else:
        return "I can only answer simple questions for now."

# --- Main webhook route ---
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    
    user_speech = request.form.get('SpeechResult')
    
    if user_speech:
        print(f"User said: {user_speech}")
        
        # Process the user's speech
        # For a simple project, we'll use a local function.
        # For a more advanced project, you'd call an LLM API (like OpenAI) here
        reply_text = process_command(user_speech.lower())
        response.say(reply_text)
    
    # Listen for more input and loop the conversation
    gather = Gather(input='speech', action='/voice')
    gather.say("How can I help you today?")
    response.append(gather)

    return str(response)

# --- This code starts your server ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
