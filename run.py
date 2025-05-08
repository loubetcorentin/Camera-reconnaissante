from yolo2 import webcam_stream
from llava import ollama_stream
import threading
import sys
import cv2
import base64
from pathlib import Path
from tty_printer import EscPosPrettyPrinter, SimplePrinter

import os
import time
from dotenv import load_dotenv

load_dotenv()

LLAVA_PROMPT = Path("prompts", "prompt_detailed.txt").read_text()
SERIAL_PATH = "COM25"
#str(os.getenv("SERIAL_PATH"))
printer = SimplePrinter(SERIAL_PATH, debug=False)


def encode_image(frame):
    # Convert OpenCV frame to base64 string
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")


def consume(prompt, frame):
    printer.write_start()
    for part in ollama_stream(prompt=prompt, file=frame):
        printer.write_text(part)
        time.sleep(0.05)
    printer.wite_end()


if __name__ == "__main__":
    try:
        for frame in webcam_stream():
            if cv2.waitKey(1) == ord(" "):
                thread = threading.Thread(
                    target=consume, args=(LLAVA_PROMPT, encode_image(frame))
                )
                thread.start()
                print("ok")

    except KeyboardInterrupt:
        sys.exit()
