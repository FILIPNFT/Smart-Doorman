import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import firebase_admin
from firebase_admin import credentials, db
import logging
import signal
import time
import datetime

def end_read(signal, frame):
    print("Ctrl+C captured, ending read.")
    GPIO.cleanup()
    raise SystemExit

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def toggle_entry_exit(id, text):
    ref = db.reference(f'rfid_entries/{id}')
    entry = ref.get()
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.datetime.now().strftime(timestamp_format)

    if entry is None:
        ref.set({
            'status': 'Entered',
            'timestamp': now,
            'text': text.strip()  # Include text in entry
        })
        return 'Entered', None
    else:
        if entry['status'] == 'Entered':
            entry_time = datetime.datetime.strptime(entry['timestamp'], timestamp_format)
            exit_time = datetime.datetime.now()
            duration = exit_time - entry_time
            ref.set({
                'status': 'Exited',
                'timestamp': exit_time.strftime(timestamp_format),
                'duration': str(duration),
                'text': text.strip()  # Update text in exit record
            })
            return 'Exited', duration
        else:
            ref.set({
                'status': 'Entered',
                'timestamp': now,
                'text': text.strip()  # Include text in re-entry
            })
            return 'Entered', None

def main():
    # Firebase configuration
    CREDENTIALS_PATH = ''
    DATABASE_URL = ''

    # Initialize Firebase Admin SDK
    firebase_admin.initialize_app(credentials.Certificate(CREDENTIALS_PATH), {
        'databaseURL': DATABASE_URL
    })

    signal.signal(signal.SIGINT, end_read)
    GPIO.setmode(GPIO.BCM)
    reader = SimpleMFRC522()

    try:
        while True:
            print("Place your card near the reader...")
            id, text = reader.read()
            status, duration = toggle_entry_exit(id, text)
            print(f"ID: {id}, Text: {text.strip()}, Status: {status}, Duration: {duration}")
            time.sleep(1)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        GPIO.cleanup()
        print("Cleanup done. GPIO cleaned.")

if __name__ == "__main__":
    main()
