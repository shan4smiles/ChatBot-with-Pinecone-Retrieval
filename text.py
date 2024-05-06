import streamlit as st
import speech_recognition as sr
import pyaudio

def main():

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Create a microphone instance
    microphone = sr.Microphone()

    # Start the microphone audio stream
    with microphone as source:
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)  # Listen for up to 5 seconds
                text = recognizer.recognize_google(audio)

                # Display the recognized text
                return text
            except sr.WaitTimeoutError:
                return "No speech detected. Listening... (Press Ctrl+C to stop)"
            except sr.UnknownValueError:
                return "Could not understand audio. Listening... (Press Ctrl+C to stop)"
            except KeyboardInterrupt:
                return "Stopping..."
text = main()

