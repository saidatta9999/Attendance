
# 🧠 Face Recognition Attendance System

A smart **Flask-based web application** that uses **real-time face recognition** to mark attendance securely. Built using **Python, OpenCV, face_recognition**, and **MySQL**, this system ensures one-time attendance per user per day and stores detailed logs in a database.

---

## 📌 Features

- 🔒 **Secure Login via Face Detection**
- 📷 Real-time webcam face recognition
- 🧍 User registration with face data
- 📆 Marks attendance only once per day
- 📁 Attendance stored in MySQL
- 📊 Admin can view all attendance records
- 🔁 Detects repeated attendance attempts and shows “Already marked today”
- 🔉 Optional success sound notification after marking

---

## 🛠️ Tech Stack

| Component        | Technology            |
|------------------|------------------------|
| Backend          | Flask (Python)         |
| Face Recognition | face_recognition, OpenCV |
| Database         | MySQL                  |
| Frontend         | HTML, CSS, JS          |
| ORM / Driver     | `mysql-connector-python` |

---

## ⚙️ Project Structure

```
facetrack/
│
├── static/               # CSS/JS/image assets
├── templates/            # HTML files
│   ├── home.html
│   ├── register.html
│   ├── success.html
│   └── records.html
|   └── attendance.html
│
├── face_images/              # Stores user face images
├── encodings/        # Storres .pkl files
├── app.py                # Flask main app
├── requirements.txt      # Dependencies
└── schema.sql            # MySQL schema
└── README.md             # Decriptions of project
```

---

## 🧑‍💻 How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/saidatta9999/Attendance.git
cd Attendance
```

### 2. Set Up Python Environment
```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL
- Open MySQL Workbench or CLI
- Create a database:
  ```sql
  CREATE DATABASE facetrack;
  ```
- Run the schema:
  ```bash
  mysql -u your_user_name -p facetrack < schema.sql
  ```

### 4. Run the Flask App
```bash
python app.py
```
Then open: [http://localhost:5000](http://localhost:5000)

---

## 🧾 Database Schema

### users Table
| Column     | Type         | Description          |
|------------|--------------|----------------------|
| id         | INT (PK)     | Auto increment       |
| name       | VARCHAR(100) | User full name       |
| user_id    | VARCHAR(50)  | Unique ID (roll/emp) |
| department | VARCHAR(100) | Department info      |

### attendance Table
| Column     | Type         | Description                  |
|------------|--------------|------------------------------|
| id         | INT (PK)     | Auto increment               |
| user_id    | VARCHAR(50)  | Linked to users table        |
| timestamp  | DATETIME     | Auto set to current time     |

---

## 🔒 Attendance Rules

- Each user is allowed **only one attendance entry per day**.
- Repeated scans will show: **"Already marked today"**.

---

## 📸 Face Images

Face encodings are generated using `face_recognition` and stored in `.pkl` format. Images are organized in:
```
/face_images/username/
```
> ⚠️ Don’t push these images to GitHub. Use `.gitignore` to exclude the face_images folder.

---

## 📦 Requirements

```
Flask
face_recognition
opencv-python
mysql-connector-python
numpy
```

---

## 📢 Future Enhancements

- Admin dashboard for record filtering and export
- Email/SMS attendance notification
- AWS deployment
- Mobile camera support

---

## 🤝 Contributing

Pull requests are welcome. Please open issues for bugs or suggestions.

---

## 📝 License

This project is licensed under the MIT License.
