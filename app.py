from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import numpy as np
import cv2
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KNOWN_DIR = "dataset"

known_encodings = []
known_names = []

# 🔥 Load dataset at startup
for person_name in os.listdir(KNOWN_DIR):
    person_path = os.path.join(KNOWN_DIR, person_name)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        try:
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)

        except:
            print(f"Error loading {img_path}")

print(f"Loaded {len(known_encodings)} face encodings")


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
    min_dist = min(distances)
    index = np.argmin(distances)

    if min_dist < 0.5:
        return {
            "result": "KNOWN",
            "name": known_names[index]
        }
    else:
        return {"result": "UNKNOWN"}
