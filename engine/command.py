import os
from bs4 import BeautifulSoup
import pyttsx3
import requests
import speech_recognition as sr
import eel
import time
from googletrans import Translator
import webbrowser

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')       # getting details of current voice
    engine.setProperty('voice', voices[2].id)   # setting voices 0 for David, 1 for Hemant, 2 for Ravi, 3 for Mira
    engine.setProperty('rate', 175)     # setting up new voice rate
    eel.DisplayMessage(text)
    # print(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()



def takecommand():

    r = sr.Recognizer()
    t = Translator()

    with sr.Microphone() as source:
        # print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        # print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-IN')
        # query.lower() = t.translate(query.lower() ,dest='en').text
        # print(f"user said: {query}")
        eel.DisplayMessage(query.lower())
        time.sleep(2)
       
    except:
        return ""

    return query.lower()


@eel.expose
def allCommand(message=1):
    # if message == 1:
    #     query = takecommand()
    #     # print(query.lower())
    #     eel.senderText(query.lower())
    # else:
    #     query = message
    #     eel.senderText(query.lower())

    
    try:
        if message == 1:  # Use voice command
            query = takecommand()
            if not query:  # Handle None or empty result
                print("No command received from voice input.")
                eel.senderText("No command received.")
                return
        else:  # Use provided message
            if not isinstance(message, str):  # Ensure message is a string
                print("Invalid message type. Expected a string.")
                eel.senderText("Invalid message type.")
                return
            query = message

        eel.senderText(query.lower())  # Send processed command
    except Exception as e:
        print(f"Error in allCommand: {e}")
        eel.senderText("An error occurred while processing the command.")



    try:


        if "open" in query.lower():
            from engine.features import openCommand
            openCommand(query.lower())
        elif "on youtube" in query.lower():
            from engine.features import PlayYoutube
            PlayYoutube(query.lower())
        
        elif "send a message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            try:
                flag = ""
                contact_no, name = findContact(query)
                if(contact_no != 0):

                    if "send a message" in query:
                        flag = 'message'
                        speak("what message to send")
                        query = takecommand()
                        
                    elif "phone call" in query:
                        flag = 'call'

                    elif "video call" in query:
                        flag = 'video call'

                    else:
                        speak("Sir, What do you want to do")
                        
                    whatsApp(contact_no, query, flag, name)
            except:
                 speak("Something went wrong")

        elif "remember that" in query:
                    from engine.config import ASSISTANT_NAME
                    rememberMessage = query.replace("remember that", "")
                    rememberMessage = query.replace(ASSISTANT_NAME, "")
                    
                    speak(f"Sir, You told " + rememberMessage)
                    remember = open("engine\\Remember.txt", "a")
                    remember.write(rememberMessage)
                    remember.close()
        elif "what do you remember" in query:
                    remember = open("engine\\Remember.txt", "r")
                    speak("Sir, You told me " + remember.read())

        elif "shutdown the system" in query:
                    speak("Are you sure you want to studown the system")
                    shutUPdown = query
                    if shutUPdown == "yes":
                        os.system("shutdown /s /t 1")
                    elif shutUPdown == "no":
                         pass
                    else:
                         speak("Sir, I want confirmation")

        elif "internet speed" in query:
                    import speedtest

                    try:
                        wifi = speedtest.Speedtest()
                        upload_net = wifi.upload() / 1048576  # Convert to megabytes
                        download_net = wifi.download() / 1048576  # Convert to megabytes
                        speak(f"Your Wifi Upload speed is {int(upload_net)} megabytes")
                        speak(f"Your Wifi Download speed is {int(download_net)} megabytes")
                    except ModuleNotFoundError:
                        speak("The speedtest module is not installed. Install it using 'pip install speedtest-cli'")
                    except Exception as e:
                        speak(f"An error occurred: {e}")

        elif "temperature" in query:
                    search = "temperature in Hal township ojhar"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search}is{temp}")
        elif "weather" in query:
                    search = "Weather in Hal township ojhar"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    weat = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search}is{weat}")

        elif "system shutdown" in query:
                    from engine.features import postassistantsound
                    speak("Ok sir, I am going to sleep")
                    time.sleep(0.5) 
                    postassistantsound()
                    time.sleep(1)
                    exit()

        elif "what is your name" in query:
             speak("Sir, My name is Wisdom or Wise Intelligence System In Domians Of Machine")

        elif "how are you" in query or "how is your performance" in query:
                speak("Sir I am absolutely at my prime, I have the power to solve j double e and neat exam papers in less than 1 minute and 15 seconds")
                    

        elif "create a presentation" in query or "make a presentation" in query:
            # Catching errors in try catch block
            try:
                speak("Sure Sir. I will create it, please select a design from 1 to 6") # To alert the user for presentation generation
                
                time.sleep(0.2) # To make this program fast and smooth

                from app import get_presentation # Importing get_presentation function
                get_presentation(query) # Generating presentation

            except Exception as e:
                  speak("Something Went Wrong")
                  print(e)
            
        else:
            from engine.features import chatBot
            chatBot(query)


    except Exception as e:
        print(e)
    eel.ShowHood()