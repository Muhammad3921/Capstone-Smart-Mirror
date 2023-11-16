#Main python file to initiate video and microphone
import cv2
import face_recognition
import os
import time

fn = 'screenshot.jpg'
prev_time = os.path.getmtime(fn)
t = prev_time

t1 = face_recognition.load_image_file("training/nyle_train1.jpg")
t2 = face_recognition.load_image_file("training/nyle_train2.jpg")
t3 = face_recognition.load_image_file("training/nyle_train3.png")
t4 = face_recognition.load_image_file("training/nyle_train4.jpg")
t5 = face_recognition.load_image_file("training/nyle_train5.jpg")

nyle1 = face_recognition.face_encodings(t1)[0]
nyle2 = face_recognition.face_encodings(t2)[0]
nyle3 = face_recognition.face_encodings(t3)[0]
nyle4 = face_recognition.face_encodings(t4)[0]
nyle5 = face_recognition.face_encodings(t5)[0]

nyle = [
    nyle1, nyle2, nyle3, nyle4, nyle5
]
# Load the pre-trained Haarcascades face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the camera (0 represents the default camera)
cap = cv2.VideoCapture(0)

counter = 0
while counter !=40:
    print(counter)
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Save a screenshot when a face is detected
        counter= counter+1
        cv2.imwrite('screenshot.jpg', frame)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

time.sleep(5)
t6 = face_recognition.load_image_file("screenshot.jpg")
CurrentFace = face_recognition.face_encodings(t6)[0]
r1 = face_recognition.compare_faces(nyle, CurrentFace)
print(r1)


# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()