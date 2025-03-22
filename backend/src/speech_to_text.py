import os
import sounddevice as sd
import wave
import numpy as np
from collections import deque
from groq import Groq
import time

# Audio configuration
CHUNK = 1024
FORMAT = np.int16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 2000
SILENCE_DURATION = 1.0
SILENCE_DELAY = 5
DETECTION_START_SECONDS = 1.5

def detect_silence(audio_chunk):
    """Detect silence based on RMS energy."""
    rms = np.sqrt(np.mean(np.square(audio_chunk)))
    return rms < SILENCE_THRESHOLD

def save_audio(filename, frames, rate):
    """Save audio frames to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def record_audio():
    print("Recording... Press Ctrl+C to stop.")
    audio_frames = []
    silence_queue = deque(maxlen=SILENCE_DELAY)
    silence_start_time = None
    recording_start_time = time.time()

    def callback(indata, frames, time_info, status):
        nonlocal silence_start_time
        audio_frames.append(indata.tobytes())
        audio_array = np.frombuffer(indata, dtype=np.int16)
        
        elapsed_time = time.time() - recording_start_time
        if elapsed_time < DETECTION_START_SECONDS:
            return

        is_silent = detect_silence(audio_array)
        silence_queue.append(is_silent)

        if all(silence_queue):
            if silence_start_time is None:
                silence_start_time = time.time()
            elif time.time() - silence_start_time >= SILENCE_DURATION:
                filename = "audio_segment.wav"
                save_audio(filename, audio_frames, RATE)
                print(f"Saved: {filename}")
                raise sd.CallbackStop
        else:
            silence_start_time = None

    try:
        with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=RATE, dtype='int16'):
            sd.sleep(1000000)  # Keep running indefinitely
    except KeyboardInterrupt:
        print("Recording stopped.")
        if audio_frames:
            filename = "audio_segment.wav"
            save_audio(filename, audio_frames, RATE)
            print(f"Saved: {filename}")
            return filename

def speech_to_text(filename):
    client = Groq()

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), 
            model="whisper-large-v3-turbo", 
            prompt="Specify context or spelling",  
            response_format="json",  
            language="en",  
            temperature=0.0  
        )
        return transcription.text

if __name__ == "__main__":
    filename = record_audio()
    print("Transcription:", speech_to_text(filename))
