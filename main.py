import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
import pygame
from gtts import gTTS
import subprocess

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "50b498eb4e234e2d85b215b7d483d9f9"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def adjust_volume(command):
    if "increase volume" in command.lower():
        subprocess.call(["nircmd.exe", "changesysvolume", "5000"])  # Increase volume
        speak("Volume increased")
    elif "decrease volume" in command.lower():
        subprocess.call(["nircmd.exe", "changesysvolume", "-5000"])  # Decrease volume
        speak("Volume decreased")
    elif "mute volume" in command.lower():
        subprocess.call(["nircmd.exe", "mutesysvolume", "1"])  # Mute volume
        speak("Volume muted")
    elif "unmute volume" in command.lower():
        subprocess.call(["nircmd.exe", "mutesysvolume", "0"])  # Unmute volume
        speak("Volume unmuted")

def toggle_bluetooth(command):
    if "turn on bluetooth" in command.lower():
        subprocess.call(["bluetoothctl", "power", "on"])  # Turn on Bluetooth
        speak("Bluetooth turned on")
    elif "turn off bluetooth" in command.lower():
        subprocess.call(["bluetoothctl", "power", "off"])  # Turn off Bluetooth
        speak("Bluetooth turned off")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    elif "volume" in c.lower():
        adjust_volume(c)

    elif "bluetooth" in c.lower():
        toggle_bluetooth(c)

    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Listen"
        # Obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)  # Increased timeout

            # Recognize speech and convert it to text
            word = r.recognize_google(audio).lower()

            print(f"Recognized: {word}")  # Debug print

            if "listen" in word:  # Changed from == "Listen" to "in"
                speak("Command please")
                # Listen for command after recognizing "Listen"
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()

                    processCommand(command)

        except Exception as e:
            print("Error: {0}".format(e))
