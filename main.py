from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)

import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os
from utils import *
import os
os.environ['CURL_CA_BUNDLE'] = ''

st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

import os
os.environ["OPENAI_API_KEY"] = "#your_key"


llm = ChatOpenAI(model_name="gpt-3.5-turbo")

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

#Getting audio data
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
                audio = recognizer.listen(source, timeout=2)  # Listen for up to 2 seconds
                text = recognizer.recognize_google(audio)

                # Display the recognized text
                return text
            except sr.WaitTimeoutError:
                return "No speech detected. Listening... (Press Ctrl+C to stop)"
            except sr.UnknownValueError:
                return "Could not understand audio. Listening... (Press Ctrl+C to stop)"
            except KeyboardInterrupt:
                return "Stopping..."
st.write("Say Something")
#text = main()
import gtts
import playsound
import pyttsx3
with textcontainer:
    query = st.text_input("Query: ", key="input")
    #query = text
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner(conversation_string, query)
            st.subheader("Refined Query:")
            st.write(refined_query)
            
            #Audio
            pa = pyttsx3.init('sapi5')
            voices = pa.getProperty('voices')
            pa.setProperty('voices', voices[0].id)
            def Say(word):
                pa.say(word)
                pa.runAndWait()


            context = find_match(refined_query)
            # print(context)  
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 
        Say(response)
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

import os
os.environ["OPENAI_API_KEY"] = "YOUR-OPENAI_API_KEY"

urls = [
    "https://www.healthline.com/nutrition/diets",
    "https://en.wikipedia.org/wiki/Health",
    "https://www.webmd.com/",
    "https://www.precisionnutrition.com/blog"
]

from langchain.document_loaders import UnstructuredURLLoader    
loaders = UnstructuredURLLoader(urls=urls)
data = loaders.load()
# We got data here      

# Text Splitter
from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(separator='\n', 
                                      chunk_size=1000, 
                                      chunk_overlap=200)
docs = text_splitter.split_documents(data)


