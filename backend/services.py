"""
Business Services for Healthcare Management System
"""

from models import Patient, Doctor, MedicalRecord
from blockchain import Blockchain
from storage import FileStorage
from audit_logger import AuditLogger


class AuthenticationService:
    """Authentication and user management service"""
    
    def __init__(self, storage=None, audit_logger=None):
        self.storage = storage or FileStorage()
        self.audit_logger = audit_logger or AuditLogger()
    
    def register_patient(self, name, email, phone, date_of_birth, address):
        """Register a new patient"""
        patients = self.storage.load_patients()
        
        # Check if patient already exists
        for patient in patients:
            if patient.email == email:
                raise ValueError("Patient with this email already exists")
        
        new_patient = Patient(name, email, phone, date_of_birth, address)
        patients.append(new_patient)
        self.storage.save_patients(patients)
        
        self.audit_logger.log_audit(
            new_patient.patient_id, "PATIENT", "REGISTRATION",
            new_patient.patient_id, f"Patient registered: {name}"
        )
        
        return new_patient
    
    def register_doctor(self, name, email, specialization, license_number, password):
        """Register a new doctor"""
        doctors = self.storage.load_doctors()
        
        # Check if doctor already exists
        for doctor in doctors:
            if doctor.email == email:
                raise ValueError("Doctor with this email already exists")
        
        new_doctor = Doctor(name, email, specialization, license_number, password)
        doctors.append(new_doctor)
        self.storage.save_doctors(doctors)
        
        self.audit_logger.log_audit(
            new_doctor.doctor_id, "DOCTOR", "REGISTRATION",
            new_doctor.doctor_id, f"Doctor registered: {name}"
        )
        
        return new_doctor
    
    def authenticate_doctor(self, email, password):
        """Authenticate a doctor"""
        doctors = self.storage.load_doctors()
        
        for doctor in doctors:
            if doctor.email == email and doctor.verify_password(password):
                self.audit_logger.log_audit(
                    doctor.doctor_id, "DOCTOR", "LOGIN",
                    doctor.doctor_id, f"Doctor login successful: {email}"
                )
                return True
        
        self.audit_logger.log_audit(
            "UNKNOWN", "DOCTOR", "LOGIN_FAILED",
            "UNKNOWN", f"Failed login attempt: {email}"
        )
        return False
    
    def authenticate_admin(self, username, password):
        """Authenticate admin (default: admin/admin123)"""
        if username == "admin" and password == "admin123":
            self.audit_logger.log_audit(
                "ADMIN", "ADMIN", "LOGIN",
                "SYSTEM", "Admin login successful"
            )
            return True
        
        self.audit_logger.log_audit(
            "UNKNOWN", "ADMIN", "LOGIN_FAILED",
            "SYSTEM", "Failed admin login attempt"
        )
        return False
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        return self.storage.get_patient_by_id(patient_id)
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        return self.storage.get_doctor_by_id(doctor_id)
    
    def get_all_patients(self):
        """Get all patients"""
        return self.storage.load_patients()
    
    def get_all_doctors(self):
        """Get all doctors"""
        return self.storage.load_doctors()


class MedicalRecordService:
    """Medical record management service"""
    
    def __init__(self, storage=None, blockchain=None, audit_logger=None):
        self.storage = storage or FileStorage()
        self.blockchain = blockchain or Blockchain()
        self.audit_logger = audit_logger or AuditLogger()
    
    def create_medical_record(self, patient_id, doctor_id, diagnosis, treatment, prescription, notes):
        """Create a new medical record"""
        # Verify patient exists
        patient = self.storage.get_patient_by_id(patient_id)
        if patient is None:
            raise ValueError(f"Patient not found: {patient_id}")
        
        # Verify doctor exists
        doctor = self.storage.get_doctor_by_id(doctor_id)
        if doctor is None:
            raise ValueError(f"Doctor not found: {doctor_id}")
        
        record = MedicalRecord(patient_id, doctor_id, diagnosis, treatment, prescription, notes)
        
        # Save medical record
        records = self.storage.load_medical_records()
        records.append(record)
        self.storage.save_medical_records(records)
        
        # Add to blockchain
        block_data = f"MEDICAL_RECORD:{record.record_id}:{record.record_hash}"
        self.blockchain.add_block(block_data)
        self.storage.save_blockchain(self.blockchain)
        
        # Log audit
        self.audit_logger.log_audit(
            doctor_id, "DOCTOR", "CREATE_RECORD",
            record.record_id, f"Medical record created for patient {patient_id}"
        )
        
        return record
    
    def get_medical_record_by_id(self, record_id):
        """Get medical record by ID"""
        return self.storage.get_record_by_id(record_id)
    
    def get_medical_records_by_patient(self, patient_id):
        """Get all medical records for a patient"""
        records = self.storage.load_medical_records()
        return [record for record in records if record.patient_id == patient_id]
    
    def get_medical_records_by_doctor(self, doctor_id):
        """Get all medical records created by a doctor"""
        records = self.storage.load_medical_records()
        return [record for record in records if record.doctor_id == doctor_id]
    
    def get_all_medical_records(self):
        """Get all medical records"""
        return self.storage.load_medical_records()
    
    def verify_medical_record(self, record):
        """Verify the integrity of a medical record"""
        # Recalculate hash and compare
        data = f"{record.record_id}|{record.patient_id}|{record.doctor_id}|{record.diagnosis}|{record.treatment}|{record.prescription}|{record.notes}"
        import hashlib
        calculated_hash = hashlib.sha256(data.encode()).hexdigest()
        return calculated_hash == record.record_hash


class AccessControlService:
    """Access control and permission management service"""
    
    def __init__(self, blockchain=None, audit_logger=None):
        self.blockchain = blockchain or Blockchain()
        self.audit_logger = audit_logger or AuditLogger()
    
    def grant_access(self, doctor_id, patient_id):
        """Grant access to a patient's records"""
        access_data = f"ACCESS_GRANT:{doctor_id}:{patient_id}"
        self.blockchain.add_block(access_data)
        
        self.audit_logger.log_audit(
            doctor_id, "DOCTOR", "GRANT_ACCESS",
            patient_id, "Access granted to patient records"
        )
        
        return True
    
    def revoke_access(self, doctor_id, patient_id):
        """Revoke access to a patient's records"""
        access_data = f"ACCESS_REVOKE:{doctor_id}:{patient_id}"
        self.blockchain.add_block(access_data)
        
        self.audit_logger.log_audit(
            doctor_id, "DOCTOR", "REVOKE_ACCESS",
            patient_id, "Access revoked from patient records"
        )
        
        return True
    
    def check_access(self, doctor_id, patient_id):
        """Check if a doctor has access to a patient's records"""
        # Check blockchain for access grants
        for i in range(len(self.blockchain.chain) - 1, -1, -1):
            block = self.blockchain.chain[i]
            data = block.data
            
            if data.startswith(f"ACCESS_GRANT:{doctor_id}:{patient_id}"):
                # Check if access was revoked after grant
                for j in range(i + 1, len(self.blockchain.chain)):
                    later_block = self.blockchain.chain[j]
                    later_data = later_block.data
                    if later_data.startswith(f"ACCESS_REVOKE:{doctor_id}:{patient_id}"):
                        return False
                return True
        return False
    
    def get_blockchain(self):
        """Get the blockchain"""
        return self.blockchain
