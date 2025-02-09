import sys
import ollama
import time
from tty import Printer
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SCREENSHOT_CAM_FILE = os.getenv("SCREENSHOT_CAM_FILE")
OUTPUT_MSG_FILE = Path("output_llava.txt")
LLAVA_PROMPT = """
Look at the person whose face is in the green square, imagine a reason
why it could be a dangerous person.
"""


def ollama_requests():
    printer = Printer("/dev/tty.usbmodemflip_Rodiki1")
    printer.set_print_density(7, 255, 2)
    printer.set_margins(5, 5)
    printer.set_size(Printer.DOUBLE_WIDTH)
    while True:
        print("Start Ollama request")
        with open(SCREENSHOT_CAM_FILE, "rb") as file:
            response = ollama.chat(
                model="llava",
                messages=[
                    {
                        "role": "user",
                        "content": LLAVA_PROMPT,
                        "images": [file.read()],
                    },
                ],
            )

        content = response["message"]["content"]
        print(f"Received Ollama result : {content}")
        printer.write(str.encode(content))

        with open(OUTPUT_MSG_FILE, "w") as out_file:
            out_file.write(content)
        print(f"Saved Ollama result, see in {OUTPUT_MSG_FILE}")
        time.sleep(50)


if __name__ == "__main__":
    try:
        ollama_requests()
    except KeyboardInterrupt:
        sys.exit()
