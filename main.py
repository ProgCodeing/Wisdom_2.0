import os
import eel
from time import sleep

from engine.features import *
from engine.command import *

def start():
    
    eel.init("www")

    playAssistantsound()

    os.system('start chrome.exe --app="http://localhost:8000/index.html"')

    time.sleep(0.1)

    eel.start('index.html', mode=None, host='localhost', block=True)