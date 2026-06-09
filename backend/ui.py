"""
Console User Interface for Healthcare Management System
"""

from services import AuthenticationService, MedicalRecordService, AccessControlService
from storage import FileStorage
from blockchain import Blockchain
from audit_logger import AuditLogger


class UserInterface:
    """Console-based user interface"""
    
    def __init__(self):
        self.storage = FileStorage()
        self.audit_logger = AuditLogger()
        self.blockchain = self.storage.load_blockchain()
        self.auth_service = AuthenticationService(self.storage, self.audit_logger)
        self.record_service = MedicalRecordService(self.storage, self.blockchain, self.audit_logger)
        self.access_service = AccessControlService(self.blockchain, self.audit_logger)
    
    def start(self):
        """Start the main application loop"""
        print("=== Decentralized Healthcare Management System ===")
        print("System initialized successfully!")
        
        while True:
            self.display_main_menu()
            choice = self.get_int_input("Choose an option: ")
            
            if choice == 1:
                self.register_patient()
            elif choice == 2:
                self.register_doctor()
            elif choice == 3:
                self.login()
            elif choice == 4:
                self.show_system_info()
            elif choice == 5:
                print("Thank you for using the Decentralized Healthcare Management System!")
                break
            else:
                print("Invalid option. Please try again.")
    
    def display_main_menu(self):
        """Display the main menu"""
        print("\n=== MAIN MENU ===")
        print("1. Register as Patient")
        print("2. Register as Doctor")
        print("3. Login")
        print("4. System Information")
        print("5. Exit")
    
    def register_patient(self):
        """Register a new patient"""
        print("\n=== PATIENT REGISTRATION ===")
        
        name = input("Enter your full name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        date_of_birth = input("Enter your date of birth (YYYY-MM-DD): ")
        address = input("Enter your address: ")
        
        try:
            patient = self.auth_service.register_patient(name, email, phone, date_of_birth, address)
            print("✅ Patient registered successfully!")
            print(f"Your patient ID: {patient.patient_id}")
        except ValueError as e:
            print(f"❌ Registration failed: {e}")
    
    def register_doctor(self):
        """Register a new doctor"""
        print("\n=== DOCTOR REGISTRATION ===")
        
        name = input("Enter your full name: ")
        email = input("Enter your email: ")
        specialization = input("Enter your specialization: ")
        license_number = input("Enter your license number: ")
        password = input("Enter your password: ")
        
        try:
            doctor = self.auth_service.register_doctor(name, email, specialization, license_number, password)
            print("✅ Doctor registered successfully!")
            print(f"Your doctor ID: {doctor.doctor_id}")
        except ValueError as e:
            print(f"❌ Registration failed: {e}")
    
    def login(self):
        """Handle user login"""
        print("\n=== LOGIN ===")
        print("1. Login as Doctor")
        print("2. Login as Admin")
        print("3. Back to Main Menu")
        
        choice = self.get_int_input("Choose an option: ")
        
        if choice == 1:
            self.login_as_doctor()
        elif choice == 2:
            self.login_as_admin()
        elif choice == 3:
            return
        else:
            print("Invalid option.")
    
    def login_as_doctor(self):
        """Login as a doctor"""
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        
        if self.auth_service.authenticate_doctor(email, password):
            print("✅ Login successful!")
            self.doctor_dashboard()
        else:
            print("❌ Invalid credentials.")
    
    def login_as_admin(self):
        """Login as admin"""
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        
        if self.auth_service.authenticate_admin(username, password):
            print("✅ Admin login successful!")
            self.admin_dashboard()
        else:
            print("❌ Invalid admin credentials.")
    
    def doctor_dashboard(self):
        """Doctor dashboard"""
        while True:
            self.display_doctor_menu()
            choice = self.get_int_input("Choose an option: ")
            
            if choice == 1:
                self.create_medical_record()
            elif choice == 2:
                self.view_medical_records()
            elif choice == 3:
                self.view_patients()
            elif choice == 4:
                self.grant_access()
            elif choice == 5:
                self.revoke_access()
            elif choice == 6:
                self.view_blockchain()
            elif choice == 7:
                break
            else:
                print("Invalid option.")
    
    def display_doctor_menu(self):
        """Display doctor menu"""
        print("\n=== DOCTOR DASHBOARD ===")
        print("1. Create Medical Record")
        print("2. View Medical Records")
        print("3. View Patients")
        print("4. Grant Access")
        print("5. Revoke Access")
        print("6. View Blockchain")
        print("7. Logout")
    
    def create_medical_record(self):
        """Create a medical record"""
        print("\n=== CREATE MEDICAL RECORD ===")
        
        patient_id = input("Enter patient ID: ")
        doctor_id = input("Enter your doctor ID: ")
        diagnosis = input("Enter diagnosis: ")
        treatment = input("Enter treatment: ")
        prescription = input("Enter prescription: ")
        notes = input("Enter additional notes: ")
        
        try:
            record = self.record_service.create_medical_record(
                patient_id, doctor_id, diagnosis, treatment, prescription, notes
            )
            print("✅ Medical record created successfully!")
            print(f"Record ID: {record.record_id}")
        except ValueError as e:
            print(f"❌ Failed to create medical record: {e}")
    
    def view_medical_records(self):
        """View all medical records"""
        print("\n=== MEDICAL RECORDS ===")
        records = self.record_service.get_all_medical_records()
        
        if not records:
            print("No medical records found.")
            return
        
        for record in records:
            print(f"\nRecord ID: {record.record_id}")
            print(f"Patient ID: {record.patient_id}")
            print(f"Doctor ID: {record.doctor_id}")
            print(f"Diagnosis: {record.diagnosis}")
            print(f"Treatment: {record.treatment}")
            print(f"Creation Date: {record.creation_date}")
            print(f"Record Hash: {record.record_hash}")
            print("-" * 50)
    
    def view_patients(self):
        """View all patients"""
        print("\n=== PATIENTS ===")
        patients = self.auth_service.get_all_patients()
        
        if not patients:
            print("No patients found.")
            return
        
        for patient in patients:
            print(f"\nPatient ID: {patient.patient_id}")
            print(f"Name: {patient.name}")
            print(f"Email: {patient.email}")
            print(f"Phone: {patient.phone}")
            print(f"Registration Date: {patient.registration_date}")
            print("-" * 50)
    
    def grant_access(self):
        """Grant access to patient records"""
        print("\n=== GRANT ACCESS ===")
        doctor_id = input("Enter doctor ID: ")
        patient_id = input("Enter patient ID: ")
        
        self.access_service.grant_access(doctor_id, patient_id)
        print("✅ Access granted successfully!")
    
    def revoke_access(self):
        """Revoke access to patient records"""
        print("\n=== REVOKE ACCESS ===")
        doctor_id = input("Enter doctor ID: ")
        patient_id = input("Enter patient ID: ")
        
        self.access_service.revoke_access(doctor_id, patient_id)
        print("✅ Access revoked successfully!")
    
    def view_blockchain(self):
        """View the blockchain"""
        print("\n=== BLOCKCHAIN ===")
        print(f"Chain Size: {self.blockchain.get_size()}")
        print(f"Chain Valid: {'✅ YES' if self.blockchain.is_chain_valid() else '❌ NO'}")
        print("-" * 50)
        
        for block in self.blockchain.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 50)
    
    def admin_dashboard(self):
        """Admin dashboard"""
        while True:
            self.display_admin_menu()
            choice = self.get_int_input("Choose an option: ")
            
            if choice == 1:
                self.view_all_patients()
            elif choice == 2:
                self.view_all_doctors()
            elif choice == 3:
                self.view_all_records()
            elif choice == 4:
                self.view_audit_log()
            elif choice == 5:
                self.verify_blockchain()
            elif choice == 6:
                self.clear_audit_log()
            elif choice == 7:
                break
            else:
                print("Invalid option.")
    
    def display_admin_menu(self):
        """Display admin menu"""
        print("\n=== ADMIN DASHBOARD ===")
        print("1. View All Patients")
        print("2. View All Doctors")
        print("3. View All Records")
        print("4. View Audit Log")
        print("5. Verify Blockchain")
        print("6. Clear Audit Log")
        print("7. Logout")
    
    def view_all_patients(self):
        """View all patients (admin)"""
        self.view_patients()
    
    def view_all_doctors(self):
        """View all doctors (admin)"""
        print("\n=== DOCTORS ===")
        doctors = self.auth_service.get_all_doctors()
        
        if not doctors:
            print("No doctors found.")
            return
        
        for doctor in doctors:
            print(f"\nDoctor ID: {doctor.doctor_id}")
            print(f"Name: {doctor.name}")
            print(f"Email: {doctor.email}")
            print(f"Specialization: {doctor.specialization}")
            print(f"License Number: {doctor.license_number}")
            print(f"Registration Date: {doctor.registration_date}")
            print("-" * 50)
    
    def view_all_records(self):
        """View all records (admin)"""
        self.view_medical_records()
    
    def view_audit_log(self):
        """View audit log"""
        self.audit_logger.print_audit_log()
    
    def verify_blockchain(self):
        """Verify blockchain integrity"""
        is_valid = self.blockchain.is_chain_valid()
        
        print("\n=== BLOCKCHAIN VERIFICATION ===")
        print(f"Chain Valid: {'✅ YES' if is_valid else '❌ NO'}")
        print(f"Chain Size: {self.blockchain.get_size()}")
        
        if not is_valid:
            print("⚠️ Blockchain integrity is compromised!")
    
    def clear_audit_log(self):
        """Clear audit log"""
        confirmation = input("Are you sure you want to clear the audit log? (yes/no): ")
        
        if confirmation.lower() == 'yes':
            self.audit_logger.clear_audit_log()
            print("✅ Audit log cleared successfully!")
        else:
            print("Operation cancelled.")
    
    def show_system_info(self):
        """Display system information"""
        print("\n=== SYSTEM INFORMATION ===")
        print("Decentralized Healthcare Management System")
        print("Version: 2.0.0 (Python Backend)")
        print("\nFeatures:")
        print("- Patient and Doctor Registration")
        print("- Medical Record Management with SHA-256 Encryption")
        print("- Blockchain Technology for Data Integrity")
        print("- Access Control and Audit Logging")
        print("- Role-based Authentication")
        
        print("\nTechnologies Used:")
        print("- Python 3.x")
        print("- SHA-256 Cryptographic Hashing")
        print("- Blockchain with Proof-of-Work Mining")
        print("- JSON-based Data Storage")
        
        print("\nSecurity Features:")
        print("- Password Hashing for Authentication")
        print("- Medical Record Encryption")
        print("- Immutable Blockchain Ledger")
        print("- Comprehensive Audit Trail")
        
        print("\nData Storage:")
        print("- Local File System (healthcare_data/)")
        print("- JSON Serialization")
        print("- Blockchain Persistence")
        print("- Text-based Audit Log")
    
    def get_int_input(self, prompt):
        """Get integer input from user"""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    ui = UserInterface()
    ui.start()
