from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import datetime

import models
import schemas
from database import engine, get_db

# Create DB tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Skill Development & Certification Management API",
    description="FastAPI Backend for Student Skill Tracker & Certification Verification DBMS System",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initial DB Seed Endpoint
@app.on_event("startup")
def seed_database():
    db = next(get_db())
    # Seed Department
    if not db.query(models.Department).first():
        cse = models.Department(dept_name="Computer Science & Engineering", hod_name="Dr. A. Sharma")
        ece = models.Department(dept_name="Electronics & Communication", hod_name="Dr. B. Verma")
        db.add_all([cse, ece])
        db.commit()

        # Seed Faculty
        prof = models.Faculty(first_name="Ramesh", last_name="Kumar", email="faculty@college.edu", designation="Associate Professor", dept_id=1)
        db.add(prof)
        db.commit()

        # Seed Student
        student = models.Student(first_name="Alex", last_name="Johnson", email="student@college.edu", batch_year=2026, dept_id=1)
        db.add(student)
        db.commit()

        # Seed Skills
        skills = [
            models.Skill(skill_name="Java", domain="Programming", description="Core & Advanced Java"),
            models.Skill(skill_name="Python", domain="Data Science", description="Python programming"),
            models.Skill(skill_name="SQL", domain="Database", description="Relational DB Queries"),
            models.Skill(skill_name="React.js", domain="Frontend", description="UI Library"),
            models.Skill(skill_name="AWS Cloud", domain="Cloud", description="Cloud Computing Platform")
        ]
        db.add_all(skills)
        db.commit()

        # Seed Certifications
        certs = [
            models.Certification(cert_name="AWS Cloud Practitioner", issuing_org="Amazon Web Services", skill_id=5),
            models.Certification(cert_name="Java SE 11 Developer", issuing_org="Oracle", skill_id=1)
        ]
        db.add_all(certs)
        db.commit()

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Skill & Certification Management API"}

# --- DEPARTMENT ENDPOINTS ---
@app.get("/api/departments", response_model=List[schemas.DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

# --- SKILL ENDPOINTS ---
@app.get("/api/skills", response_model=List[schemas.SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return db.query(models.Skill).all()

@app.post("/api/skills", response_model=schemas.SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Skill).filter(models.Skill.skill_name == skill.skill_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already exists")
    db_skill = models.Skill(**skill.model_dump())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# --- STUDENT SKILL ENDPOINTS ---
@app.post("/api/student-skills", response_model=schemas.StudentSkillResponse, status_code=status.HTTP_201_CREATED)
def log_student_skill(item: schemas.StudentSkillCreate, db: Session = Depends(get_db)):
    db_item = models.StudentSkill(**item.model_dump())
    db.merge(db_item) # Insert or update
    db.commit()
    return db_item

@app.get("/api/student-skills/{student_id}", response_model=List[schemas.StudentSkillResponse])
def get_student_skills(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.StudentSkill).filter(models.StudentSkill.student_id == student_id).all()

# --- STUDENT CERTIFICATE ENDPOINTS ---
@app.post("/api/student-certificates", response_model=schemas.StudentCertificateResponse, status_code=status.HTTP_201_CREATED)
def submit_certificate(cert: schemas.StudentCertificateCreate, db: Session = Depends(get_db)):
    db_cert = models.StudentCertificate(**cert.model_dump())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

@app.get("/api/student-certificates/student/{student_id}", response_model=List[schemas.StudentCertificateResponse])
def get_student_certificates(student_id: int, db: Session = Depends(get_db)):
    return db.query(models.StudentCertificate).filter(models.StudentCertificate.student_id == student_id).all()

# --- FACULTY VERIFICATION ENDPOINTS ---
@app.get("/api/faculty/pending-certificates", response_model=List[schemas.StudentCertificateResponse])
def get_pending_certificates(db: Session = Depends(get_db)):
    return db.query(models.StudentCertificate).filter(models.StudentCertificate.verification_status == "Pending").all()

@app.put("/api/faculty/verify-certificate/{student_cert_id}", response_model=schemas.StudentCertificateResponse)
def verify_certificate(student_cert_id: int, payload: schemas.VerificationUpdate, db: Session = Depends(get_db)):
    cert = db.query(models.StudentCertificate).filter(models.StudentCertificate.student_cert_id == student_cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate submission not found")
    
    cert.verification_status = payload.verification_status
    cert.verified_by = payload.verified_by
    cert.verification_date = datetime.date.today()
    if payload.remarks:
        cert.remarks = payload.remarks
        
    db.commit()
    db.refresh(cert)
    return cert
