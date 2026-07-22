import cv2
import numpy as np
import serial
import time

COM_PORT = "COM6"      
BAUD_RATE = 9600

LOWER_COLOR = np.array([100, 100, 50])
UPPER_COLOR = np.array([130, 255, 255])

SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180

def map_value(value, in_min, in_max, out_min, out_max):
    value = max(in_min, min(in_max, value))
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
     
    try:
        arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  
        print(f"تم الاتصال بالأردوينو على {COM_PORT}")
    except Exception as e:
        print(f"فشل الاتصال بالأردوينو: {e}")
        print("تأكد من رقم البورت الصحيح وإن الأردوينو IDE مو فاتح مسكه")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ما قدرت أفتح الكاميرا")
        return

    last_angle_sent = -1
    current_angle = 90  
    smoothing = 0.3  

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  
        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        target_angle = None

        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 300:  
                (x, y), radius = cv2.minEnclosingCircle(largest)
                cx = int(x)

                cv2.circle(frame, (cx, int(y)), int(radius), (0, 255, 0), 2)
                cv2.circle(frame, (cx, int(y)), 4, (0, 0, 255), -1)

                target_angle = map_value(cx, 0, frame_width, SERVO_MAX_ANGLE, SERVO_MIN_ANGLE)

        if target_angle is not None:
            current_angle += (target_angle - current_angle) * smoothing

        angle_to_send = int(current_angle)

        if angle_to_send != last_angle_sent:
            arduino.write(f"{angle_to_send}\n".encode())
            last_angle_sent = angle_to_send

        cv2.line(frame, (frame_center_x, 0), (frame_center_x, frame_height), (255, 0, 0), 1)

        cv2.imshow("Pen Tracker", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()