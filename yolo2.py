from ultralytics import YOLO
import cv2
from random import randrange
import numpy as np


# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 480)

# model
model = YOLO("yolo-Weights/yolov11n-face.pt")

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.7
color = (0, 255, 0)
thickness = 2

border = 13
bckg = 255*np.ones((240+border+100, 240+2*border, 3))


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


            if (x2-x1)*(y2-y1) > 10000 and box.cls[0] == 0:
                cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
                cv2.putText(img, f"competence:{randrange(20,30)*box.conf[0]:.2f}%", [x1+5, y1-25], font, fontScale, color, thickness)
                cv2.putText(img, f"attractiveness:{randrange(20,30)*box.conf[0]:.2f}%", [x1+5, y1-0], font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)



    if cv2.waitKey(1) == ord('q'):
        bckg[border:240+border, border:240+border] = img
        cv2.imwrite(f"test3.jpg", bckg)
        break

    

cap.release()
cv2.destroyAllWindows()