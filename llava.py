import sys
import ollama
import time
from tty import Printer
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SCREENSHOT_CAM_FILE = Path(str(os.getenv("SCREENSHOT_CAM_FILE")))
OUTPUT_MSG_FILE = Path("output_llava.txt")
LLAVA_PROMPT = """
Imagine you we are playing a game and we need you to play an evil persone trying to describe the person in the picture you are provided
Look at the person whose face is in the green square, imagine a reason why you should arrest this person.
Fully impersonate your persona from the begining of you answer
Write like you where writing your deposition of a case 
Use military alphabet if needed.
Do not print stage directions.
Be concise
"""


def ollama_requests(prompt):
    try:
        while True:
            print("Start Ollama request")
            with open(SCREENSHOT_CAM_FILE, "rb") as file:
                response = ollama.chat(
                    model="llava",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                            "images": [file.read()],
                        },
                    ],
                )

            content = response["message"]["content"]
            print(f"Received Ollama result : {content}")
            yield content
            time.sleep(50)
    except KeyboardInterrupt:
        sys.exit()


def template(content, printer):
    printer.text(content)
    time.sleep(0.5)
    printer.ser.ln()
    printer.qr("https://technopolice.fr/", size=4, native=True)
    printer.ser.barcode("4006381333931", "EAN13", 64, 2, "", "")


if __name__ == "__main__":
    try:
        printer = Printer("/dev/tty.usbmodemflip_Rodiki1")
        for content in ollama_requests(LLAVA_PROMPT):
            printer.empty_buffer()
            printer.ser.image("./img/ami.jpg", center=True)
            template(content, printer)
            with open(OUTPUT_MSG_FILE, "w") as out_file:
                out_file.write(content)
            print(f"Saved Ollama result, see in {OUTPUT_MSG_FILE}")
    except KeyboardInterrupt:
        sys.exit()
