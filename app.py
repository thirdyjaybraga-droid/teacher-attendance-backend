from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load teachers
with open("teachers.json", "r", encoding="utf-8-sig") as f:
    teachers = json.load(f)

# In-memory attendance storage
attendance = {}

@app.route("/")
def home():
    return "Teacher attendance backend is running!"

@app.route("/scan_qr/<teacher_id>")
def scan_qr(teacher_id):
    if teacher_id in teachers:
        attendance[teacher_id] = "Present"
        return f"Attendance confirmed for {teachers[teacher_id]}"
    else:
        return "Teacher not found in database"

@app.route("/attendance")
def get_attendance():
    result = {teachers[k]: v for k, v in attendance.items()}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
