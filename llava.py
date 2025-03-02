import os
import sys
import time
from pathlib import Path
from tty_printer import Printer

import ollama
from dotenv import load_dotenv

load_dotenv()

SCREENSHOT_CAM_FILE = Path(str(os.getenv("SCREENSHOT_CAM_FILE")))
OUTPUT_MSG_FILE = Path(str(os.getenv("OUTPUT_MSG_FILE")))
SERIAL_PATH = str(os.getenv("SERIAL_PATH"))
LLAVA_PROMPT = Path("prompts", "prompt.txt").read_text()


def ollama_stream(prompt, file):
    try:
        with open(OUTPUT_MSG_FILE, "w") as out_file:
            print("Start Ollama request")
            for part in ollama.chat(
                model="llava",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [file],
                    },
                ],
                stream=True,
            ):
                yield part["message"]["content"]
                print(part["message"]["content"], end="", flush=True)
                out_file.write(part["message"]["content"])
        print("Ollama stoped generating request")
    except KeyboardInterrupt:
        sys.exit()


def template(content, printer):
    printer.text(content)

if __name__ == "__main__":
    try:
        printer = Printer(SERIAL_PATH, debug=True)
        ami_img = Path('./img/ami.jpg')
        if ami_img.exists():
            printer.ser.image(ami_img, center=True)
        printer.write_datetime()
        with open(SCREENSHOT_CAM_FILE, "rb") as file:
            for content in ollama_stream(LLAVA_PROMPT, file.read()):
                printer.text(content)
                time.sleep(0.1)
        printer.ser.ln()
        printer.qr("https://technopolice.fr/", size=4)
        printer.ser.barcode("4006381333931", "EAN13", 64, 2, "", "")
    except KeyboardInterrupt:
        sys.exit()
