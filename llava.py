import os
import sys
import time
from pathlib import Path
from tty_printer import EscPosPrettyPrinter, SimplePrinter

import ollama
from dotenv import load_dotenv

load_dotenv()

SCREENSHOT_CAM_FILE = Path(str(os.getenv("SCREENSHOT_CAM_FILE")))
OUTPUT_MSG_FILE = Path(str(os.getenv("OUTPUT_MSG_FILE")))
SERIAL_PATH = "COM25"
#str(os.getenv("SERIAL_PATH"))
LLAVA_PROMPT = Path("prompts", "prompt_detailed.txt").read_text()

# Choose type of printer
# printer = EscPosPrettyPrinter(SERIAL_PATH, debug=True)
printer = SimplePrinter(SERIAL_PATH, debug=False)


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
                keep_alive=-1
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
        printer.write_start()
        with open(SCREENSHOT_CAM_FILE, "rb") as file:
            for content in ollama_stream(LLAVA_PROMPT, file.read()):
                printer.write_text(content)
                time.sleep(0.3)
        
        printer.wite_end()
    except KeyboardInterrupt:
        sys.exit()
