# Unknown Detector (Real-Time Face Recognition)

## Features
- Real-time webcam detection
- Predefined known faces (5 images per person)
- Detect UNKNOWN faces with animation
- Shows name for known faces

## Setup

### 1. Add dataset

backend/dataset/person_name/
→ add 5 images per person

---

### 2. Run backend

cd backend
pip install -r requirements.txt
uvicorn app:app --reload

---

### 3. Run frontend

Open frontend/index.html in browser

---

## Notes

- Works best with clear face images
- Threshold = 0.5 (can adjust in app.py)
- Use HTTPS for deployment (camera access)
