import face_recognition
import cv2
import numpy as np

# U?itaj sliku tvog lica i nau?i je
my_image = face_recognition.load_image_file("tvoja_slika.jpg")
my_face_encoding = face_recognition.face_encodings(my_image)[0]

# Pokre?e kameru
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([my_face_encoding], face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = "Filip"

        print("Prepoznato lice: ", name)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
