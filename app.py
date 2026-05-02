from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import numpy as np
import base64
import cv2
import pickle
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ENCODINGS_FILE = "encodings.pkl"

# Load known encodings
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        known_encodings = pickle.load(f)
else:
    known_encodings = []

@app.post("/register")
async def register(data: dict):
    images = data["images"]

    new_encodings = []

    for img in images:
        image_data = img.split(",")[1]
        img_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        encs = face_recognition.face_encodings(frame)
        if encs:
            new_encodings.append(encs[0])

    known_encodings.extend(new_encodings)

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(known_encodings, f)

    return {"status": "Registered", "count": len(new_encodings)}


@app.post("/detect")
async def detect(data: dict):
    image_data = data["image"].split(",")[1]
    img_bytes = base64.b64decode(image_data)

    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    faces = face_recognition.face_encodings(frame)

    if not faces:
        return {"result": "No Face"}

    unknown = faces[0]

    if len(known_encodings) == 0:
        return {"result": "UNKNOWN"}

    distances = face_recognition.face_distance(known_encodings, unknown)

    if min(distances) > 0.5:
        return {"result": "UNKNOWN"}
    else:
        return {"result": "KNOWN"}
