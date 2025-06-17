import cv2
import serial
import time

# Open USB Serial Port 
ser = serial.Serial("COM5", 115200, timeout=1)  
time.sleep(2)  # Waiting for STM32 to initialize

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)  # Open webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        ser.write(b'yes\n')  # Sending 'yes' if a face is detected
        print("Face Detected: Sending 'yes'")
    else:
        ser.write(b'no\n')   # Sending 'no' if no face is detected
        print("No Face: Sending 'no'")

    # the webcam output
    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
