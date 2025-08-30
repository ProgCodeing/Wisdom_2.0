import pygame
from pipes import quote
import struct
import subprocess
import time
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.config import ASSISTANT_NAME
from engine.command import speak, takecommand
import pywhatkit as kit
import webbrowser
import sqlite3
import pvporcupine
import g4f # This allows us to write text using gpt-4
from pptx import Presentation # Creates Presentation for us
import random # For generating random numbers
import re # For regular expressions 
import os # Allow us to interact with system
import time


from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("wisdom.db")
cursor = con.cursor()

# wisdom startup sound

def playAssistantsound():
    music_dir = 'www\\assets\\sound\\welcome_home_jarvis.mp3'
    playsound(music_dir)
@eel.expose
def postassistantsound():
    music_dir = 'www\\assets\\sound\\start_sound.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# To open a application or website we are using openCommand function

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+ query)
                    webbrowser.open(results[0][0])

                else:
                    query = takecommand().lower()
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                        webbrowser.open(f"https://www.{query}.com")
                        if ".com" in query or "dotcom" in query or "dot com" in query or ".co.in" in query or ".org" in query:
                            webbrowser.open(f"https://www.{query}")
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

# def google(query):
#     import wikipedia as googleScrap
#     query = query.replace("Wisdom","")
#     query = query.replace("Jarvis","")
#     query = query.replace("Wisdom search","")
#     query = query.replace("Jarvis search","")
#     query = query.replace("search google","")
#     speak("I found this on google")

#     try:
#         kit.search(query)
#         result = googleScrap.summary(query,1)
#         speak(result)

#     except:
#         speak("Sorry, nothing is available for this topic try a different topic")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    # speak("यूट्यूब पर "+search_term+" चलाता हूँ, सर")
    speak("Playing "+search_term+" on Youtube")
    kit.playonyt(search_term)

def hotword(query=None):  # Added default value to avoid missing argument error
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Porcupine setup
        porcupine = pvporcupine.create(keyword_paths=["engine\\Wisdom_en_windows_v3_0_0.ppn"],
                                       keywords=["jarvis", "alexa"],
                                       access_key='pfrfncwnW04UWcmr0lv6Ot+NwvCChGtwUoPxa/y63rDrfzQTGkyN3A==')
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("Hotword detected")
                # Simulate pressing Win+J using pyautogui
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
                
    except Exception as e:
        print(f"Error in hotword detection: {e}")


# Using find contacts function to find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "starting video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)



# chat bot 

def chatBot(query):
    try:
        # Initialize ChatBot with cookies
        chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")

        # Start a new conversation
        conversation_id = chatbot.new_conversation()
        chatbot.change_conversation(conversation_id)

        # Get chatbot response
        response = chatbot.chat(query)
        print(response)

        # Text-to-speech (ensure speak is defined)
        if callable(globals().get('speak')):
            speak(response)

        return response

    except FileNotFoundError:
        print("Error: Cookies file not found. Please ensure 'engine\\cookies.json' exists.")
        return "Error: Unable to load cookies."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: ChatBot encountered an issue."

    
@eel.expose()
def htmlexit():
    exit()
