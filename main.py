import requests
import random
import time
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit as pwt
import pyautogui
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *
from PIL import Image, ImageTk

# Initialize pyttsx3 engine
def init_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)
    engine.setProperty('voice', voices[1].id)
    return engine

# Initialize pyttsx3 engine
engine = init_engine()

# Pardon messages
pardonme = ["Sorry, can you please repeat", 
            "Ohooo, I forgot to catch up, I am listening, can you repeat it", 
            "Sorry, please repeat"]

# Greetings
wish = ["Hi, how are you?", 
        "Hello, are you free now?", 
        "Hey, how can I assist you?"]

# Function to get IP address
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response.get("ip")

# Function to get location based on IP
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

# Function to speak
def tell(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet based on time
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        tell(f"Good Morning User, it's {time_now}")
    elif 12 <= hour < 18:
        tell(f"Good Afternoon User, it's {time_now}")
    else:
        tell(f"Good Evening User, it's {time_now}")

# Function to listen to voice command
def take_listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-in')
            print(f"You said: {command}\n")
        except Exception as e:
            tell(random.choice(pardonme))
            return "None"
        return process(command)

# Function to process voice command
def process(command):
    if "hi" in command:
        tell(random.choice(wish))
    elif 'time now' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        print(time_now)
        tell(f'It\'s {time_now}')
    elif 'name' in command:
        tell("My name is Aurora, I am your virtual assistant")
    elif 'date' in command:
        day = datetime.date.today()
        print(day)
        tell(str(day))
    elif 'hey' in command:
        tell("Hi there. How can I help you?")
    elif 'who are you' in command:
        tell("I am Aurora. I am your personal assistant")
    elif 'who is' in command:
        person = command.replace('who is', '').strip()
        info_person = wikipedia.summary(person, 2)
        print(info_person)
        tell(info_person)
    elif 'google search' in command:
        search_query = command.replace('google search', '').strip()
        webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
        tell('Searching on Google')
    elif 'define' in command:
        search_query = command.replace('define', '').strip()
        search_wiki = wikipedia.summary(search_query, 3)
        print(search_wiki)
        tell(search_wiki)
    elif 'play' in command:
        song_name = command.replace('play', '').strip()
        tell(f"Playing {song_name} on YouTube")
        pwt.playonyt(song_name)
    elif 'weather' in command:
        webbrowser.open_new_tab("https://www.google.com/search?q=weather")
        tell("Here is the weather information from Google")
    elif 'news' in command:
        tell('Here are some hot news from BBC')
        webbrowser.open_new_tab('https://www.bbc.com/news')
        response = requests.get('https://www.bbc.com/news')
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')
        for headline in headlines:
            print(headline.text.strip())
            tell(headline.text.strip())
        tell("Closing tab")
        pyautogui.click(1871, 22)
    elif 'remind me' in command:
        reminder_text = command.replace('remind me', '').strip()
        with open("memory.txt", "a") as file:
            file.write(reminder_text + "\n")
        tell("Okay Sir, I will remember this")
    elif 'recall' in command:
        with open("memory.txt", "r") as file:
            memory_content = file.read()
        if not memory_content:
            tell("No task to remember")
        else:
            tell(f"You asked me to remember that {memory_content}")
            with open("memory.txt", "w") as file:
                file.write("")  # Clear the memory after recalling

# Main loop to listen continuously
def loop():
    while True:
        take_listen()

# GUI part
root = Tk()
root.geometry("2000x1100")
root.title("AURORA")

canvas = Canvas(root, width=1000, height=1000)
canvas.pack(fill="both", expand=True)
canvas.create_text(550, 300, text="Hello, I am Aurora\nYour beloved Personal Assistant...", font='Times 12 italic bold')
canvas.create_text(1000, 800, text="Press to listen", font='Times 12 italic bold')

canvas.create_text(1400, 300, text="You can ask me..\n1.Time\n2.Date\n3.News\n4.Weather\n5.Playsongs\n6.Remind me\n7.Recall", font='Times 12 italic bold')

img = ImageTk.PhotoImage(file="finalmic (1).jpg")
MIC_button = Button(root, command=take_listen, image=img)
MIC_button_window = canvas.create_window(925, 600, anchor="nw", window=MIC_button)

root.mainloop()
