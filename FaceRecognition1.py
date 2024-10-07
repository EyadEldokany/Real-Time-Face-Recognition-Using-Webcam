import face_recognition
import cv2
import numpy as np

# Load known images
known_image_1 = face_recognition.load_image_file("C:\\Users\\ASUS\\Downloads\\person_1.jpg")
known_image_2 = face_recognition.load_image_file("C:\\Users\\ASUS\\Downloads\\person_2.jpg")
known_image_3 = face_recognition.load_image_file(r"C:\Users\ASUS\Downloads\person_3.jpeg")
# Encode known images
known_encoding_1 = face_recognition.face_encodings(known_image_1)[0]
known_encoding_2 = face_recognition.face_encodings(known_image_2)[0]
known_encoding_3 = face_recognition.face_encodings(known_image_3)[0]
# List of known face encodings and their labels
known_face_encodings = [known_encoding_1, known_encoding_2 , known_encoding_3]
known_face_names = ["Person 1", "Person 2","Person 3"]

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all face locations and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Initialize an array for the names of detected faces
    face_names = []

    # Compare the detected faces with known encodings
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results by drawing rectangles around faces and showing names
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up since the frame we used was scaled down to 1/4
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with the name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
