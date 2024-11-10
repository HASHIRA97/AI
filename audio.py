import whisper

# Load the Whisper model (you can choose different sizes: tiny, base, small, medium, large)
model = whisper.load_model("base")

# Transcribe the audio file (replace 'audio_file.mp3' with your actual audio file)
result = model.transcribe("My name.m4a")

# Get the transcribed text
print(result['text'])
