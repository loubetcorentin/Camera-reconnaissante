import sys
from ultralytics import YOLO
import cv2
from random import randrange
import numpy as np
import ollama
from threading import Thread
import time
from pathlib import Path
from tty import Printer

IMG_PATH = Path("img")
SCREENSHOT_CAM_FILE = IMG_PATH / "screen_cam.jpg"
YOLO_WEIGHTS_PATH = Path("yolo-Weights")
YOLO11N_FACE_FILE = YOLO_WEIGHTS_PATH / "yolov11n-face.pt"

OUTPUT_MSG_FILE = Path("output_llava.txt")


LLAVA_PROMPT = "Look at the person whose face is in the green square, imagine a reason why it could be a dangerous person."


def webcam_stream():
    # start webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 480)
    cap.set(4, 480)

    # model
    model = YOLO(YOLO11N_FACE_FILE)
    model.verbose = False

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.7
    color = (0, 255, 0)
    thickness = 2

    border = 13
    bckg = 255 * np.ones((240 + border + 100, 240 + 2 * border, 3))
    ref_time = time.time()

    while True:
        success, img = cap.read()
        img = img[:, 80:560]

        results = model(img, stream=True)

        # coordinates
        for r in results:
            boxes = r.boxes
            classNames = r.names

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                if (x2 - x1) * (y2 - y1) > 10000 and box.cls[0] == 0:
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
                    # cv2.putText(img, f"competence:{randrange(20,30)*box.conf[0]:.2f}%", [x1+5, y1-25], font, fontScale, color, thickness)
                    # cv2.putText(img, f"attractiveness:{randrange(20,30)*box.conf[0]:.2f}%", [x1+5, y1-0], font, fontScale, color, thickness)

        cv2.imshow("Webcam", img)

        if time.time() - ref_time > 1:
            ref_time = time.time()
            cv2.imwrite(str(SCREENSHOT_CAM_FILE), img)

        if cv2.waitKey(1) == ord("q"):
            bckg[border : 240 + border, border : 240 + border] = img
            cv2.imwrite(str(SCREENSHOT_CAM_FILE), img)
            break

    cap.release()
    cv2.destroyAllWindows()


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
        # webcam_stream()
        # webcam_thread = Thread(target=webcam_stream)
        ollama_thread = Thread(target=ollama_requests)
        # webcam_thread.start()
        ollama_thread.start()
    except KeyboardInterrupt:
        sys.exit()
