# 🎯 Face Recognition Attendance System

An AI-based real-time attendance system built using **Python**, **OpenCV**, and **face_recognition**.
The system detects faces through a webcam, registers new users, and automatically marks attendance with date and time.

---

## 🚀 Features

* ✅ Real-time face detection using webcam
* 👤 Register new faces dynamically
* 📊 Automatic attendance marking (once per day)
* 💾 Stores face encodings locally
* 🟢 Known faces highlighted in green
* 🔴 Unknown faces highlighted in red
* ⚡ Optimized frame resizing for faster performance

---

## 🧠 Technologies Used

* Python 3.x
* OpenCV (`cv2`)
* face_recognition (dlib-based)
* NumPy
* JSON / CSV for storage

---

## 📂 Project Structure

```
face_attendance/
│
├── venv/                  # Virtual environment
├── face_data/             # Stored face encodings (auto-created)
├── attendance.csv         # Attendance records (auto-created)
└── attendance_system.py   # Main application
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone or Download Project

Place `attendance_system.py` inside a project folder.

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```
pip install cmake
pip install dlib
pip install face_recognition
pip install opencv-python
pip install numpy
```

> ⚠️ Installing **dlib** may take several minutes on Windows.

---

## ▶️ How to Run

```
python attendance_system.py
```

Your webcam window will open.

---

## 🎮 Controls

| Key   | Action                      |
| ----- | --------------------------- |
| **R** | Register next detected face |
| **Q** | Quit application            |

---

## 👤 First-Time Usage

1. Run the program.
2. Show your face to the webcam.
3. Press **R** to register.
4. Enter your name in the terminal.
5. Next time you appear, attendance will be marked automatically.

---

## 📝 Attendance Format

Attendance is saved in:

```
attendance.csv
```

Example:

```
Name, Date, Time
Srinivas, 2026-02-25, 17:45:21
```

---

## ⚠️ Troubleshooting

### ❌ `ModuleNotFoundError`

Make sure virtual environment is activated:

```
venv\Scripts\activate
```

### ❌ Webcam Not Opening

Check:

* Camera permissions
* No other app using webcam

### ❌ Slow Performance

Try:

* Better lighting
* Closing background apps

---

## 🔮 Future Improvements

* GUI dashboard (Tkinter / Streamlit)
* Database integration (MySQL / Firebase)
* Face mask detection
* Cloud-based attendance logs
* Multiple camera support

---

## 👨‍💻 Author

**Srinivas**
B.Tech CSE (AI & ML)
Face Recognition Attendance System Project

---

⭐ If you like this project, consider improving it with more AI features!
