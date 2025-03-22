import os
import pyaudio
import wave
from google.cloud import speech

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/probindhakal/Desktop/NITS_NEURATHON_CALL_AGENT/ai-phone-agent/neurosphere-453417-a13fa049f648.json"

def audio_file(file_path, duration=5):
    """Record audio at 16 kHz sample rate"""
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=16000,  # Consistently using 16 kHz
                      input=True,
                      frames_per_buffer=1024)
    
    print("Recording... Speak now!")
    frames = []
    
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  # Consistently using 16 kHz
        wf.writeframes(b''.join(frames))

def speech_to_text(file_path):
    """
    Convert speech to text using Google Cloud Speech-to-Text API
    Expects 16 kHz audio input
    """
    client = speech.SpeechClient()
    
    try:
        with open(file_path, "rb") as audio_file:
            audio_data = audio_file.read()
        
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,  # Consistently using 16 kHz
            language_code="en-US",
            # Optional: Enable automatic punctuation
            enable_automatic_punctuation=True,
        )
        
        print("Transcribing...")
        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            print("No speech detected.")
            return None
        else:
            transcript = response.results[0].alternatives[0].transcript
            print(f"Transcript: {transcript}")
            return transcript
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        raise

if __name__ == "__main__":
    file_path = "audio_input.wav"
    audio_file(file_path)
    speech_to_text(file_path)