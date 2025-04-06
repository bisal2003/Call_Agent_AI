import src.speech_to_text as speech_to_text
# import test.aiagent as aiagent
import src.text_to_speech as text_to_speech
from src.models import gemini_llm
import aiagent
import time
while True:
    try:
        question = speech_to_text.speech_to_text()
        print(question)
        
        response = gemini_llm().invoke(question)

        text_to_speech.text_to_speech(response)
        end1 = time.time()
        # print(end1 - end)

    except KeyboardInterrupt:
        print("Stopping...")
        break