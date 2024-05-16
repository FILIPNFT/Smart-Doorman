IoT Security and Monitoring System

Project Overview

This project is an IoT-based security and monitoring system designed to enhance the security of business premises by integrating face detection, RFID scanning, and real-time monitoring. It utilizes a Raspberry Pi 5 with a Raspberry Pi Camera V2 and RFID reader to detect the number of people in front of a building and manage access control through RFID cards and facial recognition.

Features

Face Detection: Uses OpenCV to count the number of people in the frame. If the count exceeds a predefined threshold, a notification is sent to security personnel.
RFID Access Control: Employs an RFID scanner to read entry cards. Access is granted when the card data matches the preregistered information, followed by facial verification.
Facial Recognition: Implements face recognition trained specifically to recognize authorized individuals to ensure secure access.
Real-Time Monitoring: A web interface displays the current number of people outside the building, logs recognized entries, and indicates unrecognized faces.
Technology Stack

Hardware: Raspberry Pi 5, Raspberry Pi Camera V2, RFID MFRC522
Software: Python, OpenCV, Flask, Firebase, JavaScript, HTML/CSS
Setup and Installation

Hardware Setup: Connect the Raspberry Pi Camera V2 and RFID MFRC522 to the Raspberry Pi 5.
Software Dependencies:
Install Python libraries: OpenCV, firebase_admin, flask, mfrc522.
Set up Firebase project and update firebaseConfig in the web application.
Running the System:
Start the camera and RFID reader scripts.
Launch the Flask server to serve the web interface.
Access the web application through a browser at localhost:8000.
Usage

Place the RFID card near the reader to attempt access.
The camera continuously monitors and updates the facial detection count.
Access logs and face detection updates are displayed in real time on the web interface.
Contributing

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.
