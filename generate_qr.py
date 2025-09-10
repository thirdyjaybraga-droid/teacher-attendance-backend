import qrcode
import urllib.parse
import os
import json

# load teachers.json (same format as the backend)
with open("teachers.json") as f:
    teachers = json.load(f)

# Set these:
BACKEND = "https://teacher-attendance-backend-vbzs.onrender.com"   # e.g. https://teacher-attendance-backend.onrender.com
# Must be the exact confirm.html path on GitHub Pages:
REDIRECT = "https://thirdyjaybraga-droid.github.io/teacher-attendance/confirm.html"

os.makedirs("teacher_qr", exist_ok=True)
for t in teachers:
    params = {"id": t["id"], "redirect": REDIRECT}
    url = BACKEND.rstrip("/") + "/checkin?" + urllib.parse.urlencode(params)
    img = qrcode.make(url)
    filename = f"teacher_qr/{t['id']}_{t['name'].replace(' ','_')}.png"
    img.save(filename)
    print("Saved:", filename, "->", url)
