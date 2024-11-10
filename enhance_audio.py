import noisereduce as nr
import scipy.io.wavfile as wav
from pydub import AudioSegment
import numpy as np

# Load audio file
def load_audio(file_path):
    # pydub can handle many formats (e.g., mp3, wav)
    audio = AudioSegment.from_file(file_path)
    # Convert to mono channel and 16-bit PCM format for noise reduction
    audio = audio.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    return audio

# Convert pydub audio segment to numpy array for processing
def audio_to_numpy(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    return samples

# Save numpy array back to audio file
def save_audio(output_path, audio_data, sample_rate):
    wav.write(output_path, sample_rate, audio_data)

# Noise reduction and speech enhancement
def enhance_speech(audio_file, output_file, volume_increase_db=10):
    # Step 1: Load the audio
    audio = load_audio(audio_file)
    sample_rate = audio.frame_rate
    audio_data = audio_to_numpy(audio)

    # Step 2: Perform noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)

    # Step 3: Convert reduced noise back to AudioSegment
    enhanced_audio = AudioSegment(
        reduced_noise.astype(np.int16).tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )

    # Step 4: Increase the volume
    enhanced_audio = enhanced_audio + volume_increase_db  # Increase volume by specified dB

    # Step 5: Save the enhanced audio
    save_audio(output_file, np.array(enhanced_audio.get_array_of_samples()), sample_rate)
    print(f"Noise-reduced and volume-increased audio saved to: {output_file}")

# Example usage
input_audio = '/home/bibrahim/PycharmProjects/Machine Learning/My name.m4a'
output_audio = '/home/bibrahim/PycharmProjects/Machine Learning/My name enhanced.m4a'

enhance_speech(input_audio, output_audio)
