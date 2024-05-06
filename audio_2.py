import pyttsx3

pa = pyttsx3.init('sapi5')
voices = pa.getProperty('voices')
pa.setProperty('voices', voices[0].id)

def Say(word):
    pa.say(word)
    pa.runAndWait()
