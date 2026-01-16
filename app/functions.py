import face_recognition
import os
from datetime import datetime
import cv2

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        
        if len(encodings) > 0:
            encodeList.append(encodings[0])
        else:
            print("Warning: No face found in image, skipping...")
    
    return encodeList

def markAttendanceDaily(name):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime('%H:%M:%S')

    os.makedirs('SheetsAttendance', exist_ok=True)
    filepath = f'SheetsAttendance/{current_date}.csv'

    nameList = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                entry = line.strip().split(',')
                if entry and entry[0]:
                    nameList.append(entry[0])
    
    if name not in nameList:
        with open(filepath, 'a', newline='') as f:
            if not nameList:
                f.write('Name,Time\n')
            f.write(f'{name},{current_time}\n')