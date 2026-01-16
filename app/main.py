import cv2
import numpy as np
import face_recognition
import os
from dotenv import load_dotenv
from functions import findEncodings, markAttendanceDaily
from pathlib import Path

root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'

load_dotenv(dotenv_path=env_path)

camera_ip = os.getenv('CAMERA_IP')
camera_port = os.getenv('CAMERA_PORT')
students_path = os.getenv('KNOWN_FACES_DIR')

os.makedirs(students_path, exist_ok=True)

images = []
classNames = []

students_sub_folders = os.listdir(students_path)
print(students_sub_folders)

student_encodings = {}

for student in students_sub_folders:
    studentImages = os.listdir(f'{students_path}/{student}')
    print(f"Processing student: {student}")
    
    student_images_list = []
    
    for cl in studentImages:
        if 'Identifier' in cl:
            continue
        
        curImg = cv2.imread(f'{students_path}/{student}/{cl}')
        if curImg is not None:
            student_images_list.append(curImg)
    
    encodings = findEncodings(student_images_list)
    
    if encodings:
        student_encodings[student] = encodings
        print(f"  Stored {len(encodings)} encodings for {student}")

encodeListKnown = []
classNames = []

for student, encodings in student_encodings.items():
    for encoding in encodings:
        encodeListKnown.append(encoding)
        classNames.append(student)

print(f'Encoding Complete: {len(encodeListKnown)} total encodings for {len(student_encodings)} students')

camera_url = f'http://{camera_ip}:{camera_port}/video'

cap = cv2.VideoCapture(camera_url)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex] and faceDis[matchIndex] <= 0.55:
            name = classNames[matchIndex].upper()
            confidence = 1 - faceDis[matchIndex]
            
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f"{name} ({confidence:.2f})", (x1+6, y2-6), 
                       cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendanceDaily(name)
        else:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "UNKNOWN", (x1+6, y2-6), 
                       cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Camera', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()