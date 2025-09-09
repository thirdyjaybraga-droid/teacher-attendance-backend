from flask import Flask, request, jsonify, redirect, send_file
from flask_cors import CORS
import csv, os, datetime, json

app = Flask(__name__)
CORS(app)  # allow frontend (GitHub Pages) to fetch

TEACHERS_FILE = "teachers.json"
ATTENDANCE_FILE = "attendance.csv"

# create sample teachers if not present
if not os.path.exists(TEACHERS_FILE):
    sample = [
        {"id": "T001", "name": "Alice Johnson"},
        {"id": "T002", "name": "Bob Smith"},
        {"id": "T003", "name": "Charlie Brown"}
    ]
    with open(TEACHERS_FILE, "w") as f:
        json.dump(sample, f, indent=2)

with open(TEACHERS_FILE, encoding="utf-8-sig") as f:
    teachers = json.load(f)


# ensure attendance CSV has header
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "timestamp", "id", "name", "status"])

def find_teacher(tid):
    return next((t for t in teachers if t["id"] == tid), None)

@app.route("/checkin")
def checkin():
    tid = request.args.get("id")
    redirect_url = request.args.get("redirect")  # optional redirect target
    if not tid:
        return "Missing id", 400

    teacher = find_teacher(tid)
    if not teacher:
        return "Teacher not found", 404

    now = datetime.datetime.utcnow().isoformat()
    today = datetime.date.today().isoformat()

    # check if already checked in today
    already = False
    with open(ATTENDANCE_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] == today and row["id"] == tid:
                already = True
                break

    status = "Present" if not already else "Already"
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([today, now, tid, teacher["name"], status])

    # redirect to confirmation page passed in redirect param (preserve id)
    if redirect_url:
        sep = "&" if "?" in redirect_url else "?"
        return redirect(f"{redirect_url}{sep}id={tid}", code=302)
    else:
        return jsonify({"message": "Recorded", "id": tid, "status": status})

@app.route("/api/attendance")
def api_attendance():
    date = request.args.get("date", datetime.date.today().isoformat())
    rows = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["date"] == date:
                    rows.append(r)
    return jsonify(rows)

@app.route("/api/teachers")
def api_teachers():
    return jsonify(teachers)

@app.route("/download")
def download():
    if not os.path.exists(ATTENDANCE_FILE):
        return jsonify({"error":"No attendance file"}), 404
    return send_file(ATTENDANCE_FILE, as_attachment=True)

@app.route("/")
def home():
    return "Teacher attendance API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
