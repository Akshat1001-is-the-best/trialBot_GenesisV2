import streamlit as st
from model import live_speech_to_text
from websearcher import google_Search
from model_chatbot import respond
from tts import tts
from youtube import vid_download


if __name__ == "__main__":
    while True:
        text = live_speech_to_text()
        
        if respond(text) == "goodbye":
            tts("Thank you bye!")
            break
        elif "video" in text:
            tts("could you please specify what video in the terminal below?")
            vid_download(input("enter search here: "))
        elif respond(text) == "question":
            tts("let me bring it up, please wait a moment")
            google_Search(text)
        elif ("lights" and "turn on") in text:
            tts("please wait a moment as I sync to the lights")
            tts("there seems to be a problem, light source cannot be found")
            tts("please check terminal for more infomation")
        else:
            tts(respond(text))
