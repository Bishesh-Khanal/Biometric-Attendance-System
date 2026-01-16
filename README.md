# Biometric Attendance System

## Setup

### Option 1: Using Mamba/Conda (Recommended)
```bash
mamba env create -f environment.yml
mamba activate cv-env
```

### Option 2: Using pip
```bash
python -m venv cv-env
source cv-env/bin/activate  # On Windows: cv-env\Scripts\activate
pip install -r requirements.txt
```

## Configuration
1. Copy `.env.example` to `.env`
2. Update `CAMERA_IP` with your phone's IP address
3. Run IP Webcam app on your phone
4. Create a sub directory for each student inside the `Students` directory
5. Put your students' images inside their respective sub directory

## Run
```bash
python app/main.py
```
