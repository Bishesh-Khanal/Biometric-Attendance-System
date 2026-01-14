import cv2
import os
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'

load_dotenv(dotenv_path=env_path)

camera_ip = os.getenv('CAMERA_IP')
camera_port = os.getenv('CAMERA_PORT')

camera_url = f'http://{camera_ip}:{camera_port}/video'

cap = cv2.VideoCapture(camera_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
else:
    print("Success! Camera opened")
    
    ret, frame = cap.read()
    if ret:
        print("Frame captured! Shape:", frame.shape)

        os.makedirs('tests/images', exist_ok=True)
        filepath = f'tests/images/test_frame.jpg'

        cv2.imwrite(filepath, frame)
        print(f'Saved {filepath}')
    else:
        print("Failed to read frame")
        
cap.release()