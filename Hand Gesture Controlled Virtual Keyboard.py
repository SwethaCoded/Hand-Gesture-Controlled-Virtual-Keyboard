import cv2
import math
import cvzone
import imutils
import numpy as np
import time
from pynput.keyboard import Controller
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

# Key layouts
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["CLEAR", "SPACE", "BACKSPACE"]]  # Added SPACE button

finalText = ""
last_key_time = time.time()
key_press_delay = 1.5  # Delay in seconds

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 0), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 10, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)

    out = img.copy()
    alpha = 0.3  # Transparency level
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

# Create buttons dynamically based on the layout
buttonList = []
button_width = 100  # Increase button size for better visibility
button_height = 100

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        # Adjust the position for the CLEAR, SPACE, and BACKSPACE buttons
        if key == "CLEAR":
            buttonList.append(Button([50, button_height * (i + 1) + 50], key, size=[button_width * 2, button_height]))  # Wider button
        elif key == "SPACE":
            buttonList.append(Button([button_width * 2 + 60, button_height * (i + 1) + 50], key, size=[button_width * 4, button_height]))  # Wider button for SPACE
        elif key == "BACKSPACE":
            buttonList.append(Button([button_width * 6 + 60, button_height * (i + 1) + 50], key, size=[button_width * 4, button_height]))  # Wider button
        else:
            buttonList.append(Button([button_width * j + 50, button_height * i + 50], key, size=[button_width, button_height]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip the image
    img = imutils.resize(img, width=1280, height=720)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        img = drawAll(img, buttonList)

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 10, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    point1 = lmList[8]  # Index finger tip
                    point2 = lmList[4]  # Thumb tip

                    # Calculate the distance between the two points
                    distance = math.dist((point1[1], point1[2]), (point2[1], point2[2]))

                    # When Clicked
                    if 20 < distance < 70:
                        current_time = time.time()
                        if current_time - last_key_time > key_press_delay:
                            # Clear button action
                            if button.text == "CLEAR":
                                finalText = ""
                            # Space button action
                            elif button.text == "SPACE":
                                finalText += " "
                            # Backspace button action
                            elif button.text == "BACKSPACE":
                                finalText = finalText[:-1]
                            else:
                                finalText += button.text
                            last_key_time = current_time  # Update the last key press time
                            keyboard.press(button.text) if button.text not in ["CLEAR", "BACKSPACE", "SPACE"] else None

                # Display the final text area with improved styling
                cv2.rectangle(img, (50, 350), (1070, 450), (175, 10, 175), cv2.FILLED)
                cv2.putText(img, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
