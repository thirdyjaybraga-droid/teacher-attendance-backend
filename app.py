from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load teachers
with open("teachers.json", "r", encoding="utf-8-sig") as f:
    teachers = json.load(f)

ATTENDANCE_FILE = "attendance.json"

# Ensure attendance.json exists
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump({}, f)

def load_attendance():
    with open(ATTENDANCE_FILE, "r") as f:
        return json.load(f)

def save_attendance(data):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(data, f)

@app.route("/")
def home():
    return "Teacher attendance backend is running!"

@app.route("/scan_qr/<teacher_id>")
def scan_qr(teacher_id):
    attendance = load_attendance()
    if teacher_id in teachers:
        attendance[teacher_id] = "Present"
        save_attendance(attendance)
        return f"Attendance confirmed for {teachers[teacher_id]}"
    else:
        return "Teacher not found in database"

@app.route("/attendance")
def get_attendance():
    attendance = load_attendance()
    result = {teachers[k]: v for k, v in attendance.items()}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
