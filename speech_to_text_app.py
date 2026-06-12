import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os

def speech_to_text(uploaded_file):
    temp_audio_path = None
    wav_path = None

    try:
        # Get file extension
        suffix = os.path.splitext(uploaded_file.name)[1].lower()

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
            temp_audio.write(uploaded_file.getbuffer())
            temp_audio_path = temp_audio.name

        # Convert MP3 to WAV if needed
        if suffix == ".mp3":
            sound = AudioSegment.from_mp3(temp_audio_path)

            wav_path = temp_audio_path.replace(".mp3", ".wav")
            sound.export(wav_path, format="wav")

            audio_path = wav_path
        else:
            audio_path = temp_audio_path

        # Speech Recognition
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return "Could not understand the audio."

    except sr.RequestError as e:
        return f"Speech Recognition service error: {e}"

    except Exception as e:
        return f"Error: {e}"

    finally:
        # Clean temporary files
        try:
            if temp_audio_path and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

            if wav_path and os.path.exists(wav_path):
                os.remove(wav_path)
        except:
            pass


def main():
    st.set_page_config(page_title="Speech to Text Converter")

    st.title("🎤 Speech to Text Converter")
    st.write("Upload a WAV or MP3 audio file and convert it into text.")

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3"]
    )

    if uploaded_file is not None:

        st.write("### File Details")
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Type:** {uploaded_file.type}")

        if st.button("Convert to Text"):

            with st.spinner("Converting audio..."):
                text = speech_to_text(uploaded_file)

            st.success("Conversion Complete!")

            st.write("### Converted Text")
            st.text_area(
                label="Output",
                value=text,
                height=200
            )


if __name__ == "__main__":
    main()

