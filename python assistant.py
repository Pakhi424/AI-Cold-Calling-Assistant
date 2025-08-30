import speech_recognition as sr
import pyttsx3
import requests
from twilio.rest import Client

# Your Twilio Account SID, Auth Token, and phone number
account_sid = "AC892aa691b31e4358269bc06b62cdf6c2"  # <-- PASTE YOUR ACCOUNT SID HERE
auth_token = "1d5fce2e52d0e758a2a3d8f663b44443"# <-- PASTE YOUR AUTH TOKEN HERE
client = Client(account_sid, auth_token)
from_number = "+16419252841" # <-- PASTE YOUR TWILIO NUMBER HERE

# Your ngrok URL from running app.py
ngrok_url ="https://17edc9014d2d.ngrok-free.app" # <-- PASTE YOUR NGROK URL HERE

# Initialize the speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()

# Create a function for the assistant to speak
def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Create a function to listen for a command
def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice) # Uses Google's free API
            command = command.lower()
            return command
    except sr.UnknownValueError:
        return "error"
    except sr.RequestError:
        return "error"

# Function to get the weather (from our previous step)
def get_weather(city):
    api_key = "YOUR_API_KEY_HERE"  # <-- PASTE YOUR OPENWEATHERMAP API KEY HERE
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    
    response = requests.get(complete_url)
    weather_data = response.json()
    
    if weather_data["cod"] != "404":
        main_data = weather_data["main"]
        temperature = main_data["temp"]
        description = weather_data["weather"][0]["description"]
        return f"The temperature is {temperature}°C with {description}."
    else:
        return "Sorry, I could not find the weather for that city."

# Function to make a cold call
def make_call_and_talk(to_number):
    try:
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=f"{ngrok_url}/voice" # Tell Twilio to use your server for the conversation
        )
        print(f"Call initiated to {to_number}. SID: {call.sid}")
    except Exception as e:
        print(f"Error making call: {e}")

# This will be the list of numbers you want to call
contact_list = ["+12345678901"] # <-- REPLACE WITH A REAL NUMBER TO CALL FOR TESTING

# Create the main function to run the assistant
def run_assistant():
    speak("Hello. How can I help you today?")
    while True:
        command = listen()
        if "error" in command:
            speak("Sorry, I didn't catch that. Can you say it again?")
            continue
        print(f"User: {command}")

        if "start calling" in command:
            speak("Okay, I will begin the cold calling process.")
            for contact in contact_list:
                make_call_and_talk(contact)
            speak("I have finished the calling process.")
        
        elif "weather in" in command:
            city = command.split("weather in ")[1]
            weather_response = get_weather(city)
            speak(weather_response)
        
        elif "hello" in command:
            speak("Hello to you too!")
        elif "how are you" in command:
            speak("I'm doing well, thank you for asking.")
        elif "what is your name" in command:
            speak("My name is Assistant.")
        elif "stop" in command or "exit" in command or "bye" in command:
            speak("Goodbye!")
            break
        else:
            speak("I can only answer simple questions for now.")

# Run the assistant
if __name__ == "__main__":
    run_assistant()
