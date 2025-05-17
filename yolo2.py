import os
import sys
import time
import subprocess
from pathlib import Path
from time import sleep

import cv2
import numpy as np
import serial
from dotenv import load_dotenv
from ultralytics import YOLO

from random import randrange


load_dotenv()

SCREENSHOT_CAM_FILE = os.getenv("SCREENSHOT_CAM_FILE")
YOLO_WEIGHTS_PATH = Path("yolo-Weights")
YOLO11N_FACE_FILE = YOLO_WEIGHTS_PATH / "yolov11n-face.pt"
SERIAL_PATH = "COM25"
DEBUG = True

def trigger_llava():
    """
    Triggers the LLaVA script for further processing.

    This function attempts to execute the LLaVA script, which is located at a predefined path.
    It first constructs the full path to the Python executable and the LLaVA script,
    then it uses `subprocess.Popen()` to initiate the script in a separate process.

    If an error occurs during the execution (e.g., missing script or incorrect Python environment),
    the function catches the exception and prints an error message.

    Usage:
        Call this function when you want to trigger the LLaVA script for processing
        after detecting a face in the webcam stream.

    Exceptions:
        - If the script fails to execute, an error message is printed.
    """
    try:
        print("🔥 Triggering LLaVA (Serge Llama) 🔥")

        basepath = Path("C:/Users/coren/Documents/these/Camera-reconnaissante")
        python = basepath / ".venv" / "Scripts" / "python.exe"
        llava = basepath / "llava.py"

        subprocess.Popen([str(python), str(llava)], shell=False)
        sleep(5)

    except Exception as e:
        print(f"Error when calling LLaVA: {e}")

def available_port(port):
    """
    Checks if the given serial port is available.
    
    Args:
        port (str): The name of the serial port (e.g., 'COM3' or '/dev/ttyUSB0').

    Returns:
        bool: True if the port is available, False otherwise.
    """
    try:
        with serial.Serial(port):
            pass
        return True
    except serial.SerialException:
        return False

def webcam_stream(save_img = True):
    """
    Captures video from the webcam and processes frames using YOLO.

    Args:
        save_img (bool): If True, save frames to the defined path.
        port (str): Serial port to check availability before processing.
    """
    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        return

    # model initialisation
    model = YOLO(YOLO11N_FACE_FILE)
    model.verbose = False

    # Define text settings for bounding boxes
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    fontScale = 0.7
    color = (0, 255, 0)
    thickness = 2
    border = 13
    bckg = 255 * np.ones((240 + border + 100, 240 + 2 * border, 3))
   
    ref_time = time.time()

    while True:
        if not available_port(SERIAL_PATH):
            print(f"Serial port {SERIAL_PATH} is not available. Waiting...")
            sleep(2)
            continue

        success, img = cap.read()
        if not success:
            print("Error: Unable to read an image from the camera.")
            break

        found = False
        results = model(img, stream=True)

        # Process YOLO results and draw bounding boxes
        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Check if face is detected
                if (x2 - x1) * (y2 - y1) > 10000 and box.cls[0] == 0:
                    found = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
                    cv2.putText(
                        img,
                        f"competence:{randrange(20,30)*box.conf[0]:.2f}%",
                        [x1 + 5, y1 - 25],
                        font,
                        fontScale,
                        color,
                        thickness,
                    )
                    print(f"Face detected with confidence {box.conf[0]:.2f}")

        yield img

        time.sleep(0.1)

        if found:
            # Save image if face is detected
            if time.time() - ref_time > 1:
                ref_time = time.time()
                if save_img :
                    cv2.imwrite(str(SCREENSHOT_CAM_FILE), img)
                    print(f"📸 Screenshot saved: {SCREENSHOT_CAM_FILE}")
                    
                    if DEBUG:
                        cv2.imshow("Webcam", img)
            
            trigger_llava()

            # Clean exit if q is pressed
            if cv2.waitKey(1) == ord("q"):
                cv2.imwrite(str(SCREENSHOT_CAM_FILE), img)
                print("Exit requested by the user.")
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        for _ in webcam_stream():
            pass
    except KeyboardInterrupt:
        print("Interrupted by Ctrl+C, stopping the program.")
        sys.exit()
