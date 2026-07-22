# Object Tracking with Servo Control

A real-time object tracking project that uses OpenCV to detect a colored object via webcam and controls a servo motor through Arduino to mimic the object's horizontal movement.

## How It Works
1. A webcam captures live video and detects the object using color-based tracking (HSV color space).
2. Python calculates the object's horizontal position and converts it into a servo angle (0–180°).
3. The angle is sent to an Arduino board over Serial communication.
4. The Arduino moves a servo motor to match the tracked object's position.

## Tech Stack
- **Python** (OpenCV, PySerial, NumPy)
- **Arduino** (C++ / Servo library)
- **Hardware:** Webcam, Arduino Uno, SG90 Servo Motor

## Files
- `tracker.py` — Python script for object detection and serial communication
- `calibrate_hsv.py` — Helper script to calibrate HSV color range for tracking
- `servo_control.ino` — Arduino sketch to receive angle commands and move the servo

## Setup
1. Install dependencies: `pip install opencv-python numpy pyserial`
2. Upload `servo_control.ino` to your Arduino via Arduino IDE
3. Update `COM_PORT` in `tracker.py` to match your Arduino's port
4. Run `python tracker.py`

## Category
Object Tracking (OpenCV)
