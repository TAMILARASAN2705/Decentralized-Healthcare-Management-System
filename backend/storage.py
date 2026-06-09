"""
File Storage for Healthcare Management System
"""

import json
import os
from pathlib import Path


class FileStorage:
    """File-based storage for healthcare data"""
    
    def __init__(self, data_directory="healthcare_data"):
        self.data_directory = data_directory
        self._create_data_directory()
    
    def _create_data_directory(self):
        """Create data directory if it doesn't exist"""
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, filename):
        """Get full path for a data file"""
        return os.path.join(self.data_directory, filename)
    
    def save_json(self, filename, data):
        """Save data to JSON file"""
        filepath = self._get_file_path(filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving {filename}: {e}")
    
    def load_json(self, filename):
        """Load data from JSON file"""
        filepath = self._get_file_path(filename)
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def save_patients(self, patients):
        """Save patients to file"""
        patients_data = [patient.to_dict() for patient in patients]
        self.save_json('patients.json', patients_data)
    
    def load_patients(self):
        """Load patients from file"""
        patients_data = self.load_json('patients.json')
        if patients_data is None:
            return []
        
        from models import Patient
        return [Patient.from_dict(data) for data in patients_data]
    
    def save_doctors(self, doctors):
        """Save doctors to file"""
        doctors_data = [doctor.to_dict() for doctor in doctors]
        self.save_json('doctors.json', doctors_data)
    
    def load_doctors(self):
        """Load doctors from file"""
        doctors_data = self.load_json('doctors.json')
        if doctors_data is None:
            return []
        
        from models import Doctor
        return [Doctor.from_dict(data) for data in doctors_data]
    
    def save_medical_records(self, records):
        """Save medical records to file"""
        records_data = [record.to_dict() for record in records]
        self.save_json('medical_records.json', records_data)
    
    def load_medical_records(self):
        """Load medical records from file"""
        records_data = self.load_json('medical_records.json')
        if records_data is None:
            return []
        
        from models import MedicalRecord
        return [MedicalRecord.from_dict(data) for data in records_data]
    
    def save_blockchain(self, blockchain):
        """Save blockchain to file"""
        blockchain_data = blockchain.to_dict()
        self.save_json('blockchain.json', blockchain_data)
    
    def load_blockchain(self):
        """Load blockchain from file"""
        blockchain_data = self.load_json('blockchain.json')
        if blockchain_data is None:
            from blockchain import Blockchain
            return Blockchain()
        
        from blockchain import Blockchain
        return Blockchain.from_dict(blockchain_data)
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        patients = self.load_patients()
        for patient in patients:
            if patient.patient_id == patient_id:
                return patient
        return None
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        doctors = self.load_doctors()
        for doctor in doctors:
            if doctor.doctor_id == doctor_id:
                return doctor
        return None
    
    def get_record_by_id(self, record_id):
        """Get medical record by ID"""
        records = self.load_medical_records()
        for record in records:
            if record.record_id == record_id:
                return record
        return None
