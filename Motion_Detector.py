#!/usr/bin/python3
import time
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

# Konstante za konfiguraciju
CREDENTIALS_PATH = '/home/filip/iot-raf-firebase-adminsdk-8tqgl-582662fcea.json'
DATABASE_URL = 'https://iot-raf-default-rtdb.europe-west1.firebasedatabase.app'
LOW_RES_SIZE = (320, 240)
VIDEO_CONFIG = {"main": {"size": (1280, 720), "format": "RGB888"}, "lores": {"size": LOW_RES_SIZE, "format": "YUV420"}}
MOTION_THRESHOLD = 7
VIDEO_BITRATE = 1000000
NO_MOTION_DELAY = 5.0  # Seconds

# Inicijalizacija Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate(CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})

# Funkcija za slanje podatka o detekciji pokreta na Firebase Realtime Database
def send_motion_event(mse):
    ref = db.reference('motion_events')
    ref.push({
        'mse': mse,
        'timestamp': {'.sv': 'timestamp'}
    })

def main():
    initialize_firebase()

    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(**VIDEO_CONFIG))
    picam2.start_preview()

    encoder = H264Encoder(VIDEO_BITRATE, repeat=True)
    encoder.output = CircularOutput()
    picam2.start()
    picam2.start_encoder(encoder)

    w, h = LOW_RES_SIZE
    prev = None
    encoding = False
    last_motion_time = 0

    try:
        while True:
            current_frame = picam2.capture_buffer("lores")
            current_frame = current_frame[:w * h].reshape(h, w)

            if prev is not None:
                mse = np.square(np.subtract(current_frame, prev)).mean()
                if mse > MOTION_THRESHOLD:
                    if not encoding:
                        start_motion_recording(encoder, mse)
                        encoding = True
                    last_motion_time = time.time()
                elif encoding and time.time() - last_motion_time > NO_MOTION_DELAY:
                    stop_motion_recording(encoder)
                    encoding = False
            prev = current_frame
    finally:
        picam2.stop_encoder()

def start_motion_recording(encoder, mse):
    epoch = int(time.time())
    encoder.output.fileoutput = f"{epoch}.h264"
    encoder.output.start()
    print("New Motion", mse)
    send_motion_event(mse)

def stop_motion_recording(encoder):
    encoder.output.stop()
    print("Motion stopped.")

if __name__ == "__main__":
    main()

