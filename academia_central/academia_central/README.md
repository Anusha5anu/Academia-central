# 🎓 Academia Central — Setup Guide

A full-stack Student Enrollment & Management System built with **Python (Flask)**, **MongoDB**, and **Bootstrap 5**.

---

## 📁 Project Structure

```
academia_central/
│
├── app.py                   ← Main Flask app (run this!)
├── requirements.txt         ← Python packages to install
├── .env.example             ← Copy to .env and fill in secrets
│
├── backend/
│   ├── db.py                ← MongoDB connection
│   └── routes/
│       ├── auth_routes.py   ← Register & Login (JWT)
│       ├── student_routes.py← Student profile CRUD + search
│       ├── course_routes.py ← Course listing, enrollment
│       ├── admin_routes.py  ← Dashboard stats, approvals
│       └── page_routes.py   ← HTML page rendering
│
└── frontend/
    ├── templates/           ← Jinja2 HTML pages
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── register.html
    │   ├── student_dashboard.html
    │   ├── student_profile.html
    │   ├── courses.html
    │   └── admin_dashboard.html
    └── static/
        ├── css/style.css    ← Custom styles
        └── js/auth.js       ← Login state & logout
```

---

## 🚀 How to Run (Step by Step)

### Step 1 — Install MongoDB
Download and install MongoDB Community Edition:
https://www.mongodb.com/try/download/community

Start MongoDB:
```bash
# On Windows (in a new terminal):
mongod

# On Mac/Linux:
brew services start mongodb-community
```

### Step 2 — Set Up Python Environment
```bash
# Go into the project folder
cd academia_central

# Create a virtual environment (keeps packages isolated)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all required packages
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Open .env and set your values:
# MONGO_URI=mongodb://localhost:27017/academia_central
# JWT_SECRET_KEY=any_random_string_here
```

### Step 4 — Run the App
```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## 🧪 Quick Test Flow

1. Go to `/register` → Create an **Admin** account
2. Go to `/register` → Create a **Student** account
3. Login as **Admin** → Go to Admin Dashboard → Add a Course
4. Login as **Student** → Browse Courses → Enroll
5. Login as **Admin** → See pending enrollments → Approve/Reject

---

## 📡 API Endpoints Summary

| Method | Endpoint                          | Who        | Description                   |
|--------|-----------------------------------|------------|-------------------------------|
| POST   | /api/auth/register                | Anyone     | Create account                |
| POST   | /api/auth/login                   | Anyone     | Get JWT token                 |
| POST   | /api/students/profile             | Student    | Create profile                |
| GET    | /api/students/profile             | Student    | View own profile              |
| PUT    | /api/students/profile             | Student    | Update profile                |
| GET    | /api/students/search?name=&dept=  | Admin      | Search students               |
| GET    | /api/courses/                     | All        | List courses                  |
| POST   | /api/courses/                     | Admin      | Add course                    |
| POST   | /api/courses/<id>/enroll          | Student    | Enroll in course              |
| GET    | /api/courses/my-enrollments       | Student    | View own enrollments          |
| PUT    | /api/courses/enrollment/<id>      | Admin      | Approve/Reject enrollment     |
| GET    | /api/admin/dashboard              | Admin      | Dashboard stats               |
| GET    | /api/admin/pending-enrollments    | Admin      | List pending approvals        |

---

## 🛠️ Technologies Used

| Layer         | Technology                         |
|---------------|------------------------------------|
| Backend       | Python 3.10+ / Flask               |
| Database      | MongoDB (NoSQL)                    |
| DB Driver     | PyMongo                            |
| Auth          | JWT (flask-jwt-extended) + bcrypt  |
| Frontend      | HTML5, CSS3, JavaScript            |
| UI Framework  | Bootstrap 5 + Bootstrap Icons      |
