from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Department(Base):
    __tablename__ = "departments"

    dept_id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String, nullable=False)
    hod_name = Column(String, nullable=True)

    students = relationship("Student", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    batch_year = Column(Integer, nullable=True)
    dept_id = Column(Integer, ForeignKey("departments.dept_id"))

    department = relationship("Department", back_populates="students")
    skills = relationship("StudentSkill", back_populates="student")
    certificates = relationship("StudentCertificate", back_populates="student")

class Faculty(Base):
    __tablename__ = "faculty"

    faculty_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    designation = Column(String, nullable=True)
    dept_id = Column(Integer, ForeignKey("departments.dept_id"))

    department = relationship("Department", back_populates="faculty")

class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, unique=True, nullable=False)
    domain = Column(String, nullable=True)
    description = Column(String, nullable=True)

    certifications = relationship("Certification", back_populates="skill")
    student_skills = relationship("StudentSkill", back_populates="skill")

class Certification(Base):
    __tablename__ = "certifications"

    cert_id = Column(Integer, primary_key=True, index=True)
    cert_name = Column(String, nullable=False)
    issuing_org = Column(String, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"))

    skill = relationship("Skill", back_populates="certifications")
    student_certs = relationship("StudentCertificate", back_populates="certification")

class StudentSkill(Base):
    __tablename__ = "student_skills"

    student_id = Column(Integer, ForeignKey("students.student_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)
    proficiency_level = Column(String, nullable=False) # Beginner, Intermediate, Advanced
    date_added = Column(Date, default=datetime.date.today)

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill", back_populates="student_skills")

class StudentCertificate(Base):
    __tablename__ = "student_certificates"

    student_cert_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    cert_id = Column(Integer, ForeignKey("certifications.cert_id"), nullable=True)
    credential_id = Column(String, nullable=False) # Partial Key
    certificate_url = Column(String, nullable=False)
    date_obtained = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    verification_status = Column(String, default="Pending") # Pending, Approved, Rejected
    verified_by = Column(Integer, ForeignKey("faculty.faculty_id"), nullable=True)
    verification_date = Column(Date, nullable=True)
    remarks = Column(String, nullable=True)

    student = relationship("Student", back_populates="certificates")
    certification = relationship("Certification", back_populates="student_certs")
