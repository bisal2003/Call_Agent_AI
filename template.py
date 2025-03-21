import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "frontend/",
    "backend/models.py",
    "backend/chains.py",
    "backend/prompts.py",
    "backend/speech_to_text.py",
    "backend/text_to_speech.py",
    "backend/ai_agent.py",
    "backend/vector_store.py",
    "backend/tools.py",
    "backend/stages.py",
    "backend/variables.py",
    "backend/phone_background.py",
    "backend/stt_module.py",
    "backend/requirements.txt",
    ".env"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir:
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file {filename}")

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
