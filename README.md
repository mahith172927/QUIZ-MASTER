# 🎓 Quiz Master

A **multi-user, full-stack exam preparation platform** built using **Flask** and **HTML** ,**CSS**. It features role-based access (Admin & Users), real-time quiz management, scoring, scheduling0— all integrated with **FLASK** and **SQLite**.



## 📌 Features

### 👤 User Functionality
- Token-based User Registration & Login
- Choose subjects/chapters and attempt quizzes
- View scores and quiz history


### 🛠 Admin (Quiz Master)
- Predefined admin login (no registration needed)
- CRUD for Subjects → Chapters → Quizzes → Questions
- Set quiz duration and scheduling
- Monitor all user activities
- View dashboard summary (quiz count, avg. score, top scorers)

---

## 🧱 Tech Stack

### 📦 Backend
- Flask 
- Flask-Security for Authentication and Role-based access
- SQLite for lightweight database


### 🎨 Frontend
-HTML For designing
-CSS For Styling
- Bootstrap for responsive UI

---

## 🚀 Getting Started

### Backend Setup (Flask)

python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python app.py
