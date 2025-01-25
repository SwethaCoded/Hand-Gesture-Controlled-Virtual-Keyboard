# Hand-Gesture-Controlled-Virtual-Keyboard
# 🖱️ Hand Gesture Controlled Virtual Keyboard

This project uses hand gestures to control a virtual keyboard, built with Python and OpenCV. It allows users to type letters, numbers, and perform actions like backspace, clear, and space, all using hand gestures detected by the webcam.

## 🚀 Features:
- Virtual keyboard with functional keys (A-Z, numbers, special keys like BACKSPACE, CLEAR, SPACE).
- Hand gesture detection using OpenCV and HandTrackingModule.
- Real-time interaction with the keyboard using index finger and thumb gestures.
- The program simulates keypresses with the `pynput` library, sending commands to the operating system.
- User-friendly interface displaying the text as you type.

## 🛠️ Requirements:
- Python 3.x
- OpenCV
- cvzone
- pynput
- imutils

## 🚀 How to Run:
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/hand-gesture-keyboard.git
    ```

2. Install the required packages:
    ```bash
    pip install opencv-python cvzone pynput imutils
    ```

3. Run the script:
    ```bash
    python gesture_keyboard.py
    ```

Enjoy typing with your hands! ✋⌨️
