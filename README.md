# Student Skill Development and Certification Management System 🎓

A full-stack DBMS Mini-Project web application built to track, manage, and verify students' technical skills and professional certifications.

## 📌 Features
- **Student Dashboard:**
  - Log technical skills and self-assessed proficiency levels (Beginner, Intermediate, Advanced).
  - Submit external professional certifications (AWS, Java, Oracle, etc.) with credential serial numbers (`credential_id`).
  - Track verification status (`Pending`, `Approved`, `Rejected`).
- **Faculty / Admin Portal:**
  - Real-time search engine to filter students by department, skill, or certification title.
  - Verification Queue with quick **Approve** or **Reject** action handlers.
- **FastAPI Python Backend & SQLite Database:**
  - Built using **SQLAlchemy ORM** and **Pydantic** validation schemas.
  - Auto-seeding database for departments, students, faculty, and skills.

---

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, Bootstrap 5, Vanilla JavaScript.
- **Backend:** Python 3.14, FastAPI, Uvicorn.
- **Database:** SQLite (SQLAlchemy ORM).

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd <repository-folder>
```

### 2. Install Dependencies & Start Backend
```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
The FastAPI backend server will run live on `http://127.0.0.1:8000`.
- Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

### 3. Open Frontend
Double click `index.html` or open it in any browser!
