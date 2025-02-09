import os
import sys
import time
from pathlib import Path
from tty import Printer

import ollama
from dotenv import load_dotenv

load_dotenv()

SCREENSHOT_CAM_FILE = Path(str(os.getenv("SCREENSHOT_CAM_FILE")))
OUTPUT_MSG_FILE = Path(str(os.getenv("OUTPUT_MSG_FILE")))
SERIAL_PATH = str(os.getenv("SERIAL_PATH"))
LLAVA_PROMPT = """
Imagine you we are playing a game and we need you to play an evil persone trying to describe the person in the picture you are provided
Look at the person whose face is in the green square, imagine a reason why you should arrest this person.
Fully impersonate your persona from the begining of you answer
Write like you where writing your deposition of a case 
Use military alphabet if needed.
Do not print stage directions.
Be concise
"""


def ollama_stream(prompt):
    try:
        print("Start Ollama request")
        with open(SCREENSHOT_CAM_FILE, "rb") as file:
            for part in ollama.chat(
                model="llava",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [file.read()],
                    },
                ],
                stream=True,
            ):
                yield part["message"]["content"]
                print(part["message"]["content"], end="", flush=True)
        print("Ollama stoped generating request")
    except KeyboardInterrupt:
        sys.exit()


def template(content, printer):
    printer.text(content)


if __name__ == "__main__":
    try:
        printer = Printer(SERIAL_PATH, debug=False)
        printer.ser.image("./img/ami.jpg", center=True)
        with open(OUTPUT_MSG_FILE, "w") as out_file:
            for content in ollama_stream(LLAVA_PROMPT):
                printer.text(content)
                out_file.write(content)
                time.sleep(0.1)
        printer.ser.ln()
        printer.qr("https://technopolice.fr/", size=4)
        printer.ser.barcode("4006381333931", "EAN13", 64, 2, "", "")
    except KeyboardInterrupt:
        sys.exit()
