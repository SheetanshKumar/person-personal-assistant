__author__ = "sheetansh"
# Year : 2018

import speech_recognition as sr  # importing speech recognition package from google api
# from pygame import mixer
import playsound    # to play saved mp3 file
from gtts import gTTS #import pyttsx3  # google text to speech
import os   # to save/open files
import wolframalpha # to calculate strings into formula, its a website which provides api, 100 times per day
from selenium import webdriver  # to control browser operations
from selenium.webdriver.common.keys import Keys
from io import BytesIO
from io import StringIO

num = 1
'''
def speak (usertext):
    engine = pyttsx3.init()
    engine.say(usertext)
    engine.runAndWait()
'''

def assistant_speaks(output):
    global num
    num +=1
    print("PerSon : ", output)
    toSpeak = gTTS(text=output, lang='en-US', slow=False)
    file = str(num)+".mp3"
    toSpeak.save(file)
    # mp3_fp = BytesIO()
    # toSpeak = gTTS(output, 'en', slow=False)
    # toSpeak.write_to_fp(mp3_fp)
    # os.system("D:\PeRSon\\audio\spoken.mp3")
    '''mixer.init()
    mixer.music.load('D:\PeRSon\\audio\spoken.mp3')
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()'''
    # song = AudioSegment.from_file(mp3_fp, format="mp3")
    # playsound.playsound(mp3_fp)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    r = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source, phrase_time_limit=5)
    print("Stop.")
    try:
        text = r.recognize_google(audio,language='en-US')
        print("You : ", text)
        return text
    except:
        assistant_speaks("Could not understand your audio, PLease try again!")
        return 0


def search_web(input):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
    if 'youtube' in input.lower():
        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx+1:]
        driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
        return

    elif 'wikipedia' in input.lower():
        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return
    else:
        if 'google' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        elif 'search' in input:
            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q=" + '+'.join(query))
        else:
            driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))
        return


def open_application(input):
    if "chrome" in input:
        assistant_speaks("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return
    elif "firefox" in input or "mozilla" in input:
        assistant_speaks("Opening Mozilla Firefox")
        os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
        return
    elif "word" in input:
        assistant_speaks("Opening Microsoft Word")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')
        return
    elif "excel" in input:
        assistant_speaks("Opening Microsoft Excel")
        os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
        return
    else:
        assistant_speaks("Application not available")
        return


def process_text(input):
    try:
        if "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am Person. Your personal Assistant.
            I am here to make your life easier. 
            You can command me to perform various tasks such as calculating sums or opening applications etcetra'''
            assistant_speaks(speak)
            return
        elif "who made you" in input or "created you" in input:
            speak = "I have been created by Sheetansh Kumar."
            assistant_speaks(speak)
            return
        elif "crazy" in input:
            speak = """Well, there are 2 mental asylums in India."""
            assistant_speaks(speak)
            return
        elif "calculate" in input.lower():
            app_id= "E46YXW-T5LG6RT7K7"
            client = wolframalpha.Client(app_id)

            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assistant_speaks("The answer is " + answer)
            return
        elif 'open' in input:
            open_application(input.lower())
            return
        elif 'search' in input or 'play' in input:
            search_web(input.lower())
            return
        else:
            assistant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else:
                return
    except Exception as e:
        print(e)
        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)


if __name__ == "__main__":
    #assistant_speaks("What's your name, Human?")
    name ='Human'
    #name = get_audio()
    assistant_speaks("Hello, " + name + '.')
    while(1):
        assistant_speaks("What can i do for you?")
        text = get_audio().lower()
        if text == 0:
            continue
        #assistant_speaks(text)
        if "exit" in str(text) or "bye" in str(text) or "go " in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, "+ name+'.')
            break
        process_text(text)
