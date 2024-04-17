import streamlit as st
from dotenv import load_dotenv
import numpy as np

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai
from gtts import gTTS
import os
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a personal gym trainer. You will be taking the transcript text and you have to explain the exercise in simple words and provide the exercise actions which the user can take action or the exercise can be done by them.
Please explain the workout routine in simple language and provide detailed steps on how to perform the exercise."""


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response

st.title("Workout Assistant🏋️‍♂️")
st.subheader('Instructions with voice commands 🗣️')
youtube_link = st.text_input("Enter YouTube Video Link:")
st.info('try this link for demo : https://www.youtube.com/watch?v=v5trqTX1VHg')

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary.candidates[0].content.parts[0].text)
        audio_data = summary.candidates[0].content.parts[0].text
        # st.write(type(audio_data))
        # audio_data = str(audio_data)
        # audio_data = audio_data.replace('*','')

        audio = gTTS(text=audio_data, lang="en", slow=True)

        audio.save("example.mp3")
        audio_file = open("example.mp3", "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/.mp3")

        sample_rate = 44100  # 44100 samples per second
        seconds = 2  # Note duration of 2 seconds
        frequency_la = 440  # Our played note will be 440 Hz
        # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
        t = np.linspace(0, seconds, seconds * sample_rate, False)
        # Generate a 440 Hz sine wave
        note_la = np.sin(frequency_la * t * 2 * np.pi)

        # st.audio(note_la, sample_rate=sample_rate)



