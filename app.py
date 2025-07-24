from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import mysql.connector
import face_recognition
import numpy as np
import pickle
from datetime import datetime

app = Flask(__name__)

# MySQL setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="facetrack"
)
cursor = db.cursor()

# Paths
DATA_DIR = "face_images"
ENCODING_DIR = "encodings"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ENCODING_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        user_id = request.form['user_id']
        department = request.form['department']

        cursor.execute("INSERT INTO users (name, user_id, department) VALUES (%s, %s, %s)",
                       (name, user_id, department))
        db.commit()

        user_folder = os.path.join(DATA_DIR, user_id)
        os.makedirs(user_folder, exist_ok=True)

        cam = cv2.VideoCapture(0)
        count = 0
        while count < 5:
            ret, frame = cam.read()
            if not ret:
                break
            cv2.imshow("Capture Face - Press 's' to Save", frame)
            if cv2.waitKey(1) & 0xFF == ord('s'):
                img_path = os.path.join(user_folder, f"{count}.jpg")
                cv2.imwrite(img_path, frame)
                count += 1
        cam.release()
        cv2.destroyAllWindows()

        encodings = []
        for img_name in os.listdir(user_folder):
            img_path = os.path.join(user_folder, img_name)
            img = face_recognition.load_image_file(img_path)
            faces = face_recognition.face_encodings(img)
            if faces:
                encodings.append(faces[0])

        with open(os.path.join(ENCODING_DIR, f"{user_id}.pkl"), "wb") as f:
            pickle.dump(encodings, f)

        return redirect('/')
    return render_template('register.html')

@app.route('/attendance')
def attendance():
    known_encodings = []
    known_ids = []

    for file in os.listdir(ENCODING_DIR):
        if file.endswith(".pkl"):
            user_id = file.replace(".pkl", "")
            with open(os.path.join(ENCODING_DIR, file), 'rb') as f:
                encs = pickle.load(f)
                known_encodings.extend(encs)
                known_ids.extend([user_id] * len(encs))

    cam = cv2.VideoCapture(0)
    detected = False
    message = "Unknown"
    name = ""
    user_id = ""

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                user_id = known_ids[best_match_index]
                cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                name = result[0] if result else "Unknown"

                today = datetime.today().date()
                cursor.execute("SELECT * FROM attendance WHERE user_id = %s AND DATE(timestamp) = %s", (user_id, today))
                already_marked = cursor.fetchone()

                if already_marked:
                    message = "Already marked today"
                else:
                    cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
                    db.commit()
                    message = "Attendance marked successfully"

                detected = True
                break

        if detected:
            break

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    return render_template("success.html", message=message, name=name, user_id=user_id)

@app.route('/records', methods=['GET', 'POST'])
def records():
    if request.method == 'POST':
        search_user_id = request.form['search_user_id']
        cursor.execute("""
            SELECT a.user_id, u.name, u.department, a.timestamp
            FROM attendance a
            JOIN users u ON a.user_id = u.user_id
            WHERE a.user_id = %s
            ORDER BY a.timestamp DESC
        """, (search_user_id,))
    else:
        cursor.execute("""
            SELECT a.user_id, u.name, u.department, a.timestamp
            FROM attendance a
            JOIN users u ON a.user_id = u.user_id
            ORDER BY a.timestamp DESC
        """)
    records = cursor.fetchall()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
