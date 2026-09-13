from pydantic import BaseModel
from typing import Optional, List
import datetime

# Department Schemas
class DepartmentBase(BaseModel):
    dept_name: str
    hod_name: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentResponse(DepartmentBase):
    dept_id: int
    class Config:
        from_attributes = True

# Student Schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    batch_year: Optional[int] = None
    dept_id: Optional[int] = None

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: int
    class Config:
        from_attributes = True

# Skill Schemas
class SkillBase(BaseModel):
    skill_name: str
    domain: Optional[str] = None
    description: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    skill_id: int
    class Config:
        from_attributes = True

# StudentSkill Schemas
class StudentSkillCreate(BaseModel):
    student_id: int
    skill_id: int
    proficiency_level: str

class StudentSkillResponse(BaseModel):
    student_id: int
    skill_id: int
    proficiency_level: str
    date_added: datetime.date
    skill: Optional[SkillResponse] = None
    class Config:
        from_attributes = True

# StudentCertificate Schemas
class StudentCertificateCreate(BaseModel):
    student_id: int
    cert_id: Optional[int] = None
    credential_id: str
    certificate_url: str
    date_obtained: Optional[datetime.date] = None
    expiry_date: Optional[datetime.date] = None

class VerificationUpdate(BaseModel):
    verification_status: str # Approved or Rejected
    verified_by: Optional[int] = None
    remarks: Optional[str] = None

class StudentCertificateResponse(BaseModel):
    student_cert_id: int
    student_id: int
    cert_id: Optional[int] = None
    credential_id: str
    certificate_url: str
    date_obtained: Optional[datetime.date] = None
    expiry_date: Optional[datetime.date] = None
    verification_status: str
    verified_by: Optional[int] = None
    verification_date: Optional[datetime.date] = None
    remarks: Optional[str] = None
    student: Optional[StudentResponse] = None

    class Config:
        from_attributes = True
