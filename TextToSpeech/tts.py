from gtts import gTTS
import os

# Create output folder
output_folder = "Converted Speech"
os.makedirs(output_folder, exist_ok=True)

print("================================")
print("       TEXT TO SPEECH")
print("================================")

# Language selection
print("\nSelect Language:")
print("1. English")
print("2. Hindi")

choice = input("\nChoose language (1/2): ")

if choice == "1":
    lang = "en"
elif choice == "2":
    lang = "hi"
else:
    print("\nInvalid choice!")
    exit()

# Get text
text = input("\nEnter your text:\n")

# Get filename
filename = input("\nEnter the name to save the audio: ")

# Remove .mp3 if user already typed it
if filename.lower().endswith(".mp3"):
    filename = filename[:-4]

# Create complete file path
output_path = os.path.join(output_folder, filename + ".mp3")

# Convert text to speech
print("\nConverting text to speech...")

tts = gTTS(text=text, lang=lang)
tts.save(output_path)

print("\n================================")
print("Audio Saved Successfully !!")
print(f"Location: {output_path}")
print("================================")
