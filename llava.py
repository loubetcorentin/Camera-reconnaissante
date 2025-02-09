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


def ollama_requests():
    printer = Printer("/dev/tty.usbmodemflip_Rodiki1")
    printer.set_print_density(7, 255, 2)
    # printer.set_margins(0, 5)
    # printer.set_size(Printer.DOUBLE_WIDTH)
    printer.set_code_page(0)
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
        # content = content.replace("\\n", "\n")
        print(f"Received Ollama result : {content}")
        printer.write("---SUSPECT---")
        printer.write("--DETECTED--")
        printer.print_datetime()
        printer.write("\n")
        printer.write(content)
        printer.write("---CALLING---")
        printer.write("---BACKUP---")
        printer.write("\n" * 5)

        with open(OUTPUT_MSG_FILE, "w") as out_file:
            out_file.write(content)
        print(f"Saved Ollama result, see in {OUTPUT_MSG_FILE}")
        time.sleep(50)


if __name__ == "__main__":
    try:
        ollama_requests()
    except KeyboardInterrupt:
        sys.exit()
