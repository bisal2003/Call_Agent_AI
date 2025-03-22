import os
import uuid
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Asus\Desktop\Call_Agent_AI\Call_Agent_AI\neurosphere-453417-a13fa049f648.json"

def text_to_speech(text):
    print("Text to Speech")
    pass
#     try:
#         # Initialize Google Cloud TTS Client
#         client = texttospeech.TextToSpeechClient()
#         synthesis_input = texttospeech.SynthesisInput(text=text)
#         uuid_ = uuid.uuid4()

#         # Path to save audio
#         output_dir = os.path.abspath("./frontend/public/assets/")
#         if not os.path.exists(output_dir):
#             print(f"Creating directory: {output_dir}")
#             os.makedirs(output_dir)

#         output_file = os.path.join(output_dir, f"female_{uuid_}.mp3")

#         # Voice configuration
#         voice = texttospeech.VoiceSelectionParams(
#             language_code="en-IN",
#             name="en-IN-Chirp3-HD-Zephyr",
#             ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
#         )

#         audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

#         # Generate speech
#         response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

#         # Save the audio file
#         with open(output_file, "wb") as out:
#             out.write(response.audio_content)
#             print(f"Audio successfully saved to {output_file}")

#         # Play using pydub
#         audio = AudioSegment.from_mp3(output_file)
#         play(audio)

#         # Return the accessible path for React
#         return f"/assets/female_{uuid_}.mp3"

#     except Exception as e:
#         import traceback
#         print("Error:", e)
#         print(traceback.format_exc())
#         return None

# # Example Usage
# # print(text_to_speech_female(
# #     "Hello probin, I hope you're doing well. It's always great to catch up. "
# #     "Today, I wanted to share some exciting news about a new AI-powered tool that can generate realistic voice outputs. "
# #     "It supports multiple languages and voice types, making it ideal for podcasts, audiobooks, or even interactive chat applications. "
# #     "Let me know if you'd like to hear more about how it works!"
# # ))
