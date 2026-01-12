import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# --- CONFIGURATION ---
# Create a folder named 'known_faces' and put your photo 'me.jpg' inside it first!
KNOWN_FACES_DIR = "known_faces"
TOLERANCE = 0.6  # Lower = Stricter

print("--- SENTRY MODE INITIALIZING ---")

# 1. Load Known Faces (The "Whitelist")
known_face_encodings = []
known_face_names = []

if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)
    print(f"WARNING: Created '{KNOWN_FACES_DIR}' folder. Please add your photo there!")

print("Loading authorized personnel...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0].upper())
        print(f"Loaded: {filename}")

# 2. Camera Setup
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret: break

    # Optimize: Process every other frame or resize to 1/4th for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1] # Convert BGR to RGB

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    status = "SCANNING..."
    color = (255, 255, 255) # White
    intrusion = False

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
        name = "UNKNOWN"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        face_names.append(name)

        if name == "UNKNOWN":
            intrusion = True
    
    # Logic for Intrusion
    if intrusion:
        status = "BREACH DETECTED"
        color = (0, 0, 255) # Red
        # Blur the whole screen to hide content
        frame = cv2.blur(frame, (50, 50))
    elif len(face_names) > 0:
        status = f"ACCESS GRANTED: {face_names[0]}"
        color = (0, 255, 0) # Green

    # Draw UI
    # We draw on the original 'frame'
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up (since we detected on 1/4th size)
        top *= 4; right *= 4; bottom *= 4; left *= 4
        
        # Draw Box
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    # Status Bar
    cv2.putText(frame, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow('Sentry Mode', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()