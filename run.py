from yolo2 import webcam_stream
from llava import ollama_stream
import threading
import sys
import cv2
import base64
from pathlib import Path

LLAVA_PROMPT = Path("prompts", "prompt.txt").read_text()


def encode_image(frame):
    # Convert OpenCV frame to base64 string
    _, buffer = cv2.imencode(".jpg", frame)
    return base64.b64encode(buffer).decode("utf-8")


def consume(prompt, frame):
    for part in ollama_stream(prompt=prompt, file=frame):
        print(part, end="", flush=True)


if __name__ == "__main__":
    try:
        for frame in webcam_stream():
            if cv2.waitKey(1) == ord("a"):
                thread = threading.Thread(
                    target=consume, args=(LLAVA_PROMPT, encode_image(frame))
                )
                thread.start()
                print("ok")

    except KeyboardInterrupt:
        sys.exit()
