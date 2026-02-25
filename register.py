"""
Face Recognition Attendance System
====================================
- First time: Registers face with a name
- Next time: Automatically marks attendance
"""

import cv2
import face_recognition
import numpy as np
import os
import json
import csv
from datetime import datetime

# ─── Config ────────────────────────────────────────────────────────────────────
DATA_DIR = "face_data"          # folder to store face encodings
ATTENDANCE_FILE = "attendance.csv"
TOLERANCE = 0.5                 # lower = stricter matching
# ────────────────────────────────────────────────────────────────────────────────

os.makedirs(DATA_DIR, exist_ok=True)

# ─── Helpers ───────────────────────────────────────────────────────────────────

def load_registered_faces():
    """Load all saved face encodings from disk."""
    encodings, names = [], []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".json"):
            path = os.path.join(DATA_DIR, file)
            with open(path) as f:
                data = json.load(f)
            encodings.append(np.array(data["encoding"]))
            names.append(data["name"])
    return encodings, names


def save_face(name: str, encoding: np.ndarray):
    """Save a new face encoding to disk."""
    safe_name = name.strip().replace(" ", "_")
    path = os.path.join(DATA_DIR, f"{safe_name}.json")
    with open(path, "w") as f:
        json.dump({"name": name, "encoding": encoding.tolist()}, f)
    print(f"[✓] Registered: {name}")


def mark_attendance(name: str):
    """Append an attendance record (once per day per person)."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Avoid duplicate entry for the same day
    existing = set()
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, newline="") as f:
            for row in csv.reader(f):
                if len(row) >= 2:
                    existing.add((row[0], row[1]))   # (name, date)

    if (name, date_str) not in existing:
        with open(ATTENDANCE_FILE, "a", newline="") as f:
            csv.writer(f).writerow([name, date_str, time_str])
        print(f"[✓] Attendance marked — {name}  {date_str}  {time_str}")
        return True
    else:
        print(f"[i] Already marked today — {name}")
        return False

# ─── Core Functions ────────────────────────────────────────────────────────────

def register_new_face(frame, face_encoding, known_encodings, known_names):
    """Ask the user for a name and save the new face."""
    print("\n[NEW FACE DETECTED] — Press 'R' in the terminal prompt to register.")
    name = input("Enter name to register (or press Enter to skip): ").strip()
    if name:
        save_face(name, face_encoding)
        known_encodings.append(face_encoding)
        known_names.append(name)
    return known_encodings, known_names


def run_attendance_system():
    print("=" * 50)
    print("  Face Recognition Attendance System")
    print("=" * 50)
    print("Controls:  Q = Quit   |   R = Force register mode")
    print()

    known_encodings, known_names = load_registered_faces()
    print(f"[i] Loaded {len(known_names)} registered face(s): {known_names}\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    attendance_log = {}   # name -> last marked date (in-memory cache)
    register_mode = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for faster processing
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for enc, loc in zip(face_encodings, face_locations):
            name = "Unknown"
            color = (0, 0, 255)   # red for unknown

            if known_encodings:
                distances = face_recognition.face_distance(known_encodings, enc)
                best_idx = np.argmin(distances)
                if distances[best_idx] < TOLERANCE:
                    name = known_names[best_idx]
                    color = (0, 200, 0)   # green for known

                    today = datetime.now().strftime("%Y-%m-%d")
                    if attendance_log.get(name) != today:
                        mark_attendance(name)
                        attendance_log[name] = today

            # Scale locations back to original frame size
            top, right, bottom, left = [v * 2 for v in loc]

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # If unknown and register_mode, capture & register
            if name == "Unknown" and register_mode:
                register_mode = False
                known_encodings, known_names = register_new_face(
                    frame, enc, known_encodings, known_names
                )

        # Overlay status
        mode_text = "MODE: REGISTER NEXT FACE" if register_mode else "MODE: ATTENDANCE"
        cv2.putText(frame, mode_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 140, 255) if register_mode else (200, 200, 200), 2)

        cv2.imshow("Attendance System — Q to quit, R to register", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            register_mode = True
            print("[i] Register mode ON — show a new face to the camera.")

    cap.release()
    cv2.destroyAllWindows()
    print("\n[✓] Session ended. Attendance saved to:", ATTENDANCE_FILE)


# ─── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_attendance_system()
