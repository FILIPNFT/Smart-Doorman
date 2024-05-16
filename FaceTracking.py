#!/usr/bin/python3

import cv2
import firebase_admin
from firebase_admin import credentials, db
from picamera2 import Picamera2
import time
import datetime

# Firebase konfiguracija
CREDENTIALS_PATH = '/home/filip/iot-raf-firebase-adminsdk-8tqgl-582662fcea.json'
DATABASE_URL = 'https://iot-raf-default-rtdb.europe-west1.firebasedatabase.app'

# Inicijalizuj Firebase Admin SDK
firebase_admin.initialize_app(credentials.Certificate(CREDENTIALS_PATH), {
    'databaseURL': DATABASE_URL
})

# Konfiguracija detektora lica
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

# Konfiguracija PiCamera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

def send_face_detection_event(faces_count):
    """Funkcija za slanje broja detektovanih lica na Firebase Realtime Database."""
    ref = db.reference('face_detections')
    # Formatiranje vremena u ?itljiviji format: npr. '2023-12-31 23:59:59'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ref.push({
        'timestamp': timestamp,
        'detected_faces': faces_count
    })

last_detected_count = -1  # Po?etna vrednost koja garantuje da je razli?ita od mogu?eg broja lica
reset_timer = 5  # Vreme za resetovanje detekcije lica na 0 (5 sekundi)
last_time_faces_detected = time.time()

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)
    current_faces_count = len(faces)

    # Ako je detektovano lica ili ako je vreme za reset i nije ve? poslato 0
    if current_faces_count != last_detected_count:
        if current_faces_count > 0 or (time.time() - last_time_faces_detected >= reset_timer and current_faces_count == 0):
            send_face_detection_event(current_faces_count)
            last_time_faces_detected = time.time()
            last_detected_count = current_faces_count

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Camera", im)
    if cv2.waitKey(1) == 27:  # Escape key
        break

cv2.destroyAllWindows()
picam2.stop()
