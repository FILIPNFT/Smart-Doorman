import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import logging
import signal
import time

def end_read(signal, frame):
    """Capture SIGINT for cleanup when the script is interrupted"""
    print("Ctrl+C captured, ending write.")
    GPIO.cleanup()
    raise SystemExit

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    signal.signal(signal.SIGINT, end_read)

    # Explicitly set the GPIO mode before initializing the reader
    GPIO.setmode(GPIO.BCM)

    try:
        writer = SimpleMFRC522()
        while True:
            text = input("Enter new data to write to the card: ")
            print("Now place your tag to write.")
            writer.write(text)
            print("Data written.")
            print("You can write new data or press Ctrl+C to exit.")
            time.sleep(1)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        GPIO.cleanup()
        print("Cleanup done. GPIO cleaned.")

if __name__ == "__main__":
    main()
