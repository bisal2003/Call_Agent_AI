import os
import pyaudio
import wave
from collections import deque
from groq import Groq
import time
# Audio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 2000
SILENCE_DURATION = 1.0
SILENCE_DELAY = 5
DETECTION_START_SECONDS = 1.5

def detect_silence(audio_chunk):
    """Detect silence based on RMS energy."""
    rms = (sum(int(sample)**2 for sample in audio_chunk) / len(audio_chunk)) ** 0.5
    return rms < SILENCE_THRESHOLD

def save_audio(filename, frames, rate):
    """Save audio frames to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Recording... Press Ctrl+C to stop.")
    audio_frames = []
    silence_queue = deque(maxlen=SILENCE_DELAY)
    silence_start_time = None
    recording_start_time = time.time()

    try:
        while True:
            audio_data = stream.read(CHUNK, exception_on_overflow=False)
            audio_frames.append(audio_data)
            
            elapsed_time = time.time() - recording_start_time
            if elapsed_time < DETECTION_START_SECONDS:
                continue
            
            audio_array = list(wave.struct.unpack('%dh' % CHUNK, audio_data))
            is_silent = detect_silence(audio_array)
            silence_queue.append(is_silent)

            if all(silence_queue):
                if silence_start_time is None:
                    silence_start_time = time.time()
                elif time.time() - silence_start_time >= SILENCE_DURATION:
                    filename = "audio_segment.wav"
                    save_audio(filename, audio_frames, RATE)
                    print(f"Saved: {filename}")
                    return filename
            else:
                silence_start_time = None
    except KeyboardInterrupt:
        print("Recording stopped.")
        if audio_frames:
            filename = "audio_segment.wav"
            save_audio(filename, audio_frames, RATE)
            print(f"Saved: {filename}")
            return filename
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

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
