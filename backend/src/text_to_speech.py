import time
import os
import requests
import wave
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
import uuid

from io import BytesIO
import wave

def save_audio_from_response(response):
    """
    Save WAV audio directly from the API response to a file.
    """

    os.makedirs("frontend/src/audio", exist_ok=True)
    id = uuid.uuid4()
    file_name = os.path.join("frontend/src/audio" , f"{id}.wav")
    print(file_name)
    if response.status_code == 200:
        # Load audio content into a BytesIO stream
        audio_stream = BytesIO(response.content)
        # Open the WAV file from the stream for reading
        with wave.open(audio_stream, 'rb') as wf:
            # Open the output file for writing
            with wave.open(file_name, 'wb') as output_file:
                # Copy audio parameters
                output_file.setnchannels(wf.getnchannels())
                output_file.setsampwidth(wf.getsampwidth()) 
                output_file.setframerate(wf.getframerate())
                # Write audio frames
                output_file.writeframes(wf.readframes(wf.getnframes()))
        print(f"Audio saved successfully as {file_name}.")
        return f"{id}.wav"
    else:
        print(f"Failed to generate TTS audio. Status code: {response.status_code}, Response: {response.text}")


def play_audio_from_response(response):
    pass



def text_to_speech(input_response="What is the weather report in india"):
    """
    Generate TTS audio and play it directly.
    """

    token = os.getenv("WAVES_API_KEY_1")
    start_in = time.time()
    url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"
    payload = {
        "voice_id": "deepika",
        "text": input_response,
        "sample_rate": 8000,
        "add_wav_header": True,
        "speed" : 1.3
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    end_in = time.time()
    print(end_in - start_in)

    return save_audio_from_response(response)

if __name__ == "__main__":
    start = time.time()
    text_to_speech()
    end = time.time()






# from smallest import Smallest
# import os
# from dotenv import load_dotenv
# import time
# import uuid
# load_dotenv()

# client = Smallest(api_key=os.getenv("WAVES_API_KEY_1"))

# def text_to_speech(llm_response):
#     id = uuid.uuid4()
#     os.makedirs("frontend/src/audio", exist_ok=True)
#     full_path = os.path.join("frontend/src/audio" , f"{id}.wav")

#     client.synthesize(
#     llm_response,
#     voice = "deepika",
#     save_as=full_path,
#     speed=1.3)

#     return f"src/audio/{id}.wav"

# if __name__ == "__main__":
#     start = time.time()
#     print(text_to_speech("What is the weather report in india"))
#     end = time.time()
#     print(end - start)



# import asyncio
# import os
# import uuid
# from dotenv import load_dotenv
# from smallest import AsyncSmallest
# import aiofiles
# import time
# load_dotenv()

# client = AsyncSmallest(api_key=os.getenv("WAVES_API_KEY_1"))


# async def text_to_speech(llm_response):
#     id = uuid.uuid4()
#     os.makedirs("frontend/src/audio", exist_ok=True)
#     full_path = os.path.join("frontend/src/audio", f"{id}.wav")

#     async with client as tts:
#         audio_bytes = await tts.synthesize(llm_response,
#             voice="deepika",
#             save_as=full_path,
#             speed=1.3,
#         )
        
#         async with aiofiles.open(full_path, "wb") as f:
#             await f.write(audio_bytes)

#     return f"src/audio/{id}.wav"


# if __name__ == "__main__":
#     start = time.time()
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     audio_path = loop.run_until_complete(text_to_speech("what is the weather report in india"))
#     loop.close()
   
#     end = time.time()
#     print(end - start)











# import time
# import wave
# import asyncio
# from groq import Groq
# from smallest import Smallest
# from smallest import TextToAudioStream
# import os

# llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
# tts = Smallest(api_key=os.getenv("WAVES_API_KEY"))

# async def generate_text(prompt):
#     """Async generator for streaming text from Groq. You can use any LLM"""
#     completion = llm.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#             }
#         ],
#         model="llama3-8b-8192",
#         stream=True,
#     )

#     for chunk in completion:
#         text = chunk.choices[0].delta.content
#         print(text)
#         if text is not None:
#             yield text

# async def save_audio_to_wav(file_path, processor, llm_output):
#     with wave.open(file_path, "wb") as wav_file:
#         wav_file.setnchannels(1)
#         wav_file.setsampwidth(2) 
#         wav_file.setframerate(24000)
        
#         async for audio_chunk in processor.process(llm_output):
#             print("generation")
#             wav_file.writeframes(audio_chunk)

# async def text_to_speech(llm_output):
#     # Initialize the TTS processor with the TTS instance
#     processor = TextToAudioStream(tts_instance=tts)
#     start = time.time()

#     # As an example, save the generated audio to a WAV file.
#     await save_audio_to_wav("llm_to_speech.wav", processor, llm_output)
#     print("Done")
#     end = time.time()
#     print(end - start)
# if __name__ == "__main__":
#     asyncio.run(text_to_speech("hello"))


























# import os
# import time
# import uuid
# import aiohttp
# import asyncio
# import aiofiles

# async def text_to_speech(input_response):
#     try:
#         # Fetch the API key from environment variables
#         token = os.getenv("WAVES_API_KEY")
#         if not token:
#             raise ValueError("WAVES_API_KEY not found in environment variables")

#         # Define the API endpoint and payload
#         url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"
#         payload = {
#             "voice_id": "deepika",
#             "speed": 1.3,
#             "text": input_response,
#             "sample_rate": 8000,
#             "add_wav_header": True
#         }
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }

#         # Record start time for performance measurement
#         start_time = time.time()

#         # Make an asynchronous POST request
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, json=payload, headers=headers) as response:
#                 if response.status != 200:
#                     print(f"Waves API error: {response.status}, {await response.text()}")
#                     return None

#                 # Read binary audio content from the response
#                 audio_content = await response.read()
#                 if not audio_content:
#                     print("No audio content in response.")
#                     return None

#         # Create the directory for audio files if it doesn't exist
#         audio_dir = "static/audio"
#         os.makedirs(audio_dir, exist_ok=True)

#         # Generate a unique filename and file path
#         filename = f"audio_{uuid.uuid4()}.wav"
#         file_path = os.path.join(audio_dir, filename)

#         # Save the audio file asynchronously
#         async with aiofiles.open(file_path, 'wb') as f:
#             await f.write(audio_content)

#         # Log processing time and return the file path
#         print(f"Audio processing time: {time.time() - start_time:.2f} seconds")
#         print(f"Audio saved to: {file_path}")

#         return f"/static/audio/{filename}"

#     except Exception as e:
#         print(f"Error in text_to_speech: {str(e)}")
#         return None

# # Run the function in an async environment
# if __name__ == "__main__":
#     async def main():
#         start = time.time()
#         input_text = "what is the weather report in india?"
#         path = await text_to_speech(input_text)
#         print(f"Total execution time: {time.time() - start:.2f} seconds")
#         print(f"Audio path: {path}")

#     asyncio.run(main())

# import time
# import os
# import requests
# from dotenv import load_dotenv
# import uuid
# import asyncio
# import aiohttp

# load_dotenv()

# def text_to_speech(input_response="What is the weather report in india"):
#     """
#     Generate TTS audio, save it locally, and return the file path.
#     Returns:
#         str: Path to the saved audio file or None if there's an error
#     """
#     try:
#         token = os.getenv("WAVES_API_KEY")
#         if not token:
#             raise ValueError("WAVES_API_KEY not found in environment variables")

#         url = "https://waves-api.smallest.ai/api/v1/lightning/get_speech"

#         payload = {
#             "voice_id": "deepika",
#             "speed" : 1.3,
#             "text": input_response,
#             "sample_rate": 8000,
#             "add_wav_header": True
#         }
        
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }

#         # Make request to Waves API
#         start_time = time.time()
#         response = requests.request("POST", url, json=payload, headers=headers)
        
#         if response.status_code != 200:
#             print(f"Waves API error: {response.status_code}, {response.text}")
#             return None

#         # Create audio directory if it doesn't exist
#         audio_dir = "static/audio"
#         os.makedirs(audio_dir, exist_ok=True)

#         # Generate unique filename
#         filename = f"audio_{uuid.uuid4()}.wav"
#         file_path = os.path.join(audio_dir, filename)

#         # Save the audio file
#         with open(file_path, 'wb') as f:
#             f.write(response.content)

#         print(f"Audio processing time: {time.time() - start_time:.2f} seconds")
#         print(f"Audio saved to: {file_path}")
        
#         # Return the URL-friendly path
#         return f"/static/audio/{filename}"

#     except Exception as e:
#         print(f"Error in text_to_speech: {str(e)}")
#         return None

# if __name__ == "__main__":
#     start = time.time()
#     path = text_to_speech()
#     print(f"Total execution time: {time.time() - start:.2f} seconds")
#     print(f"Audio path: {path}")