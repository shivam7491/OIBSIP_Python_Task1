import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from bs4 import BeautifulSoup

# Initialize the text-to-speech engine
engine = pyttsx3.init() 

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-US') 
        print(f"You said: {query}\n") 
    except Exception as e: 
        print(e)   
        print("Say that again please...\n") 
        return "" 
    return query.lower() 

def respond(query):
    if "hello" in query:
        speak("Hello there! How can I help you?")
    elif "what time is it" in query:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%H:%M')}")
    elif "what is today's date" in query:
        today = datetime.date.today()
        speak(f"Today's date is {today}")
    elif "search for" in query:
        search_term = query.split("for")[-1]
        url = f"https://www.google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f"Here's what I found for {search_term}")
    else:
        search_and_answer(query)

def search_and_answer(query):
    google_url = f"https://www.google.com/search?q={query}"
    try:
        response = requests.get(google_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        result_divs = soup.find_all('div', class_='IsZvec')

        if result_divs:
            answer = result_divs[0].text
            speak(answer)
        else:
            search_wikipedia(query)

    except requests.exceptions.RequestException as e:
        print(f"Google search error: {e}")
        search_wikipedia(query)

def search_wikipedia(query):
    wiki_url = f"https://en.wikipedia.org/wiki/{query}"
    try:
        response = requests.get(wiki_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        top_paragraph = soup.find('p')

        if top_paragraph:
            answer = top_paragraph.text
            speak(answer)
        else:
            speak("Sorry, I couldn't find a good answer for that.")
    except requests.exceptions.RequestException as e:
        print(f"Wikipedia search error: {e}")
        speak("Sorry, I couldn't find a good answer for that.")

def main():
    speak("Hello, I'm your basic voice assistant. How can I help?")
    while True:
        query = get_audio()
        if query == "quit":
            break
        respond(query)

if __name__ == "__main__":
    main()
