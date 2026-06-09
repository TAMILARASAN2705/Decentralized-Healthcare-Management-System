"""
Data Models for Healthcare Management System
"""

import hashlib
import uuid
from datetime import datetime
import json


class Patient:
    """Patient model for healthcare system"""
    
    def __init__(self, name, email, phone, date_of_birth, address):
        self.patient_id = self._generate_unique_id()
        self.name = name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.address = address
        self.registration_date = datetime.now().isoformat()
    
    def _generate_unique_id(self):
        """Generate unique patient ID"""
        return f"PAT_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'registration_date': self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Patient from dictionary"""
        patient = cls.__new__(cls)
        patient.patient_id = data['patient_id']
        patient.name = data['name']
        patient.email = data['email']
        patient.phone = data['phone']
        patient.date_of_birth = data['date_of_birth']
        patient.address = data['address']
        patient.registration_date = data['registration_date']
        return patient
    
    def __str__(self):
        return f"Patient(id={self.patient_id}, name={self.name}, email={self.email})"


class Doctor:
    """Doctor model for healthcare system"""
    
    def __init__(self, name, email, specialization, license_number, password):
        self.doctor_id = self._generate_unique_id()
        self.name = name
        self.email = email
        self.specialization = specialization
        self.license_number = license_number
        self.password_hash = self._hash_password(password)
        self.registration_date = datetime.now().isoformat()
    
    def _generate_unique_id(self):
        """Generate unique doctor ID"""
        return f"DOC_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """Verify password against stored hash"""
        return self._hash_password(password) == self.password_hash
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'email': self.email,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'password_hash': self.password_hash,
            'registration_date': self.registration_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Doctor from dictionary"""
        doctor = cls.__new__(cls)
        doctor.doctor_id = data['doctor_id']
        doctor.name = data['name']
        doctor.email = data['email']
        doctor.specialization = data['specialization']
        doctor.license_number = data['license_number']
        doctor.password_hash = data['password_hash']
        doctor.registration_date = data['registration_date']
        return doctor
    
    def __str__(self):
        return f"Doctor(id={self.doctor_id}, name={self.name}, email={self.email})"


class MedicalRecord:
    """Medical Record model for healthcare system"""
    
    def __init__(self, patient_id, doctor_id, diagnosis, treatment, prescription, notes):
        self.record_id = self._generate_unique_id()
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.prescription = prescription
        self.notes = notes
        self.creation_date = datetime.now().isoformat()
        self.record_hash = self._calculate_hash()
    
    def _generate_unique_id(self):
        """Generate unique record ID"""
        return f"REC_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}"
    
    def _calculate_hash(self):
        """Calculate SHA-256 hash of record data"""
        data = f"{self.record_id}|{self.patient_id}|{self.doctor_id}|{self.diagnosis}|{self.treatment}|{self.prescription}|{self.notes}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'treatment': self.treatment,
            'prescription': self.prescription,
            'notes': self.notes,
            'creation_date': self.creation_date,
            'record_hash': self.record_hash
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create MedicalRecord from dictionary"""
        record = cls.__new__(cls)
        record.record_id = data['record_id']
        record.patient_id = data['patient_id']
        record.doctor_id = data['doctor_id']
        record.diagnosis = data['diagnosis']
        record.treatment = data['treatment']
        record.prescription = data['prescription']
        record.notes = data['notes']
        record.creation_date = data['creation_date']
        record.record_hash = data['record_hash']
        return record
    
    def __str__(self):
        return f"MedicalRecord(id={self.record_id}, patient_id={self.patient_id}, doctor_id={self.doctor_id})"
