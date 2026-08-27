# Text to Speech (TTS) is a technology that converts written text into spoken words. It is commonly used in applications such as virtual assistants, audiobooks, and accessibility tools for individuals with visual impairments. TTS systems typically use a combination of natural language processing and speech synthesis techniques to generate human-like speech from text input.

from gtts import gTTS

text = "Hello everyone, myself Prasham Jain. I am a software engineer and I love to code. I have experience in Python, Java, and web development. I enjoy learning new technologies and working on challenging projects."

tts = gTTS(text=text, lang='en')

tts.save("output.mp3")

print("Audio Saved !!")