import os
import uuid
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"neurosphere-453417-a13fa049f648.json"

def save_audio_from_response(response, sample_rate=16000):
    """
    Save WAV audio directly from the API response to a file using Google Cloud TTS.
    Ensures output is at 16 kHz.
    """
    os.makedirs("frontend/src/audio", exist_ok=True)
    id = uuid.uuid4()
    file_name = os.path.join("frontend/src/audio", f"{id}.wav")
    
    if response.audio_content:
        with open(file_name, "wb") as output_file:
            output_file.write(response.audio_content)
        
        # Ensure the sample rate is 16 kHz
        audio = AudioSegment.from_file(file_name)
        audio = audio.set_frame_rate(sample_rate)
        audio.export(file_name, format="wav")
        
        print(f"Audio saved successfully as {file_name}.")
        return f"{id}.wav"
    else:
        print(f"Failed to generate TTS audio.")
        return None

def text_to_speech(input_response="What is the weather report in India"):
    """
    Generate TTS audio using Google Cloud and save it locally at 16 kHz.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=input_response)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-IN",
        name="en-IN-Chirp3-HD-Zephyr",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    # Set the audio config to be compatible with 16 kHz processing
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000  # Explicitly set to 16 kHz
    )
    
    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        return save_audio_from_response(response, 16000)
    except Exception as e:
        print(f"Error during TTS generation: {e}")
        return None

if __name__ == "__main__":
    text_to_speech()
