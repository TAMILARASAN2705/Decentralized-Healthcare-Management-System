# Decentralized Healthcare Management System

A comprehensive Python-based simulation of a decentralized healthcare management system with blockchain technology for secure medical record management.

## 🏥 System Overview

This system demonstrates the integration of blockchain technology in healthcare for secure, decentralized management of medical records with role-based access control and comprehensive audit logging.

## ✨ Key Features

### 🔐 Security Features
- **SHA-256 Encryption**: All medical records are encrypted using SHA-256 hashing
- **Blockchain Ledger**: Immutable record storage with mining simulation
- **Password Hashing**: Secure doctor authentication with salt-based hashing
- **Access Control**: Smart contract-like permission management
- **Audit Trail**: Complete logging of all system activities

### 👥 User Roles
- **Patient**: Registration with unique ID generation
- **Doctor**: Medical record creation and access
- **Admin**: System management and access control

### 🗄️ Data Management
- **Local File Storage**: Persistent storage in `healthcare_data/` directory
- **Blockchain Integrity**: Verification of record authenticity
- **Audit Logging**: Comprehensive activity tracking

## 🏗️ System Architecture

```
Medical/
├── backend/                         # Python backend
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Application entry point
│   ├── models.py                   # Data models (Patient, Doctor, MedicalRecord)
│   ├── blockchain.py               # Blockchain implementation (Block, Blockchain)
│   ├── storage.py                  # File storage utilities
│   ├── services.py                 # Business logic services
│   ├── audit_logger.py             # Audit logging
│   └── ui.py                       # Console user interface
├── web/                            # Web frontend
│   ├── index.html                  # Main HTML interface
│   ├── styles.css                  # CSS styling
│   ├── app.js                      # JavaScript application
│   └── server.py                   # Web server
├── healthcare_data/                # Runtime data directory
│   ├── patients.json               # Patient records
│   ├── doctors.json                # Doctor credentials
│   ├── medical_records.json        # Medical records
│   ├── blockchain.json             # Blockchain data
│   └── audit.log                   # System audit trail
├── run_system.bat                  # Windows launcher script
├── run_backend.py                  # Python launcher script
└── README.md                       # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Command line interface
- Modern web browser (for web interface)

### Installation & Running

#### Option 1: Using Launcher Script (Recommended)

**Windows:**
```bash
run_system.bat
```

**Python:**
```bash
python run_backend.py
```

#### Option 2: Manual Execution

**Run Backend (Console Interface):**
```bash
cd backend
python main.py
```

**Run Web Server (Web Interface):**
```bash
cd web
python server.py
```

**Access Web Interface:**
```
http://localhost:8080
```

## 📋 User Guide

### Main Menu Options

1. **Register as Patient**
   - Enter personal information
   - Receive unique patient ID
   - Data stored securely with audit logging

2. **Register as Doctor**
   - Enter professional details
   - Set password for authentication
   - Receive unique doctor ID

3. **Login**
   - Doctor login with email/password
   - Admin login (username: admin, password: admin123)

4. **System Information**
   - View system features and capabilities
   - Display default credentials

### Doctor Functions
- **Create Medical Record**: Add new patient records with diagnosis, treatment, and prescriptions
- **View Patient Records**: Access patient medical history
- **Verify Record Integrity**: Check blockchain authenticity of records
- **Check Access Permissions**: Verify access to patient data

### Admin Functions
- **Grant Access**: Authorize doctors to access patient records
- **Revoke Access**: Remove doctor access permissions
- **View Access Permissions**: Monitor current access rights
- **View All Records**: System-wide record overview
- **View Audit Log**: Complete system activity log
- **View Access Control Log**: Blockchain-based access history

## 🔐 Security Implementation

### Encryption Methods
- **SHA-256**: Primary hashing algorithm for records and passwords
- **Salt Generation**: Random salt for password security
- **Unique IDs**: Cryptographically generated identifiers

### Blockchain Features
- **Genesis Block**: Initial block created on system startup
- **Mining Simulation**: Proof-of-work with adjustable difficulty
- **Chain Validation**: Integrity verification of entire blockchain
- **Immutable Records**: Once added, records cannot be altered

### Access Control
- **Role-Based Permissions**: Different access levels for different roles
- **Smart Contract Logic**: Programmable access granting/revoking
- **Audit Trail**: Every access attempt logged and tracked

## 📊 Data Storage

### File Structure
```
healthcare_data/
├── patients.json      # Patient records
├── doctors.json       # Doctor credentials and profiles
├── medical_records.json # Medical records with hashes
├── blockchain.json    # Blockchain data
└── audit.log          # Comprehensive system audit trail
```

### Blockchain Storage
- Each medical record creates a new blockchain block
- Access control operations are also recorded on-chain
- Chain integrity can be verified at any time

## 🎯 Demonstration Workflow

### 1. System Initialization
```bash
# The system starts with:
- Genesis block creation
- Data directory setup
- Service initialization
```

### 2. User Registration
```bash
# Register patients and doctors
- Unique ID generation
- Secure data storage
- Audit logging
```

### 3. Medical Record Management
```bash
# Create and manage records
- SHA-256 encryption
- Blockchain integration
- Access control
```

### 4. Access Control
```bash
# Manage permissions
- Grant/revoke access
- Smart contract logic
- Audit logging
```

## 🔍 System Verification

### Record Integrity
- Original hash vs calculated hash comparison
- Blockchain chain validation
- Tamper detection

### Access Monitoring
- Complete audit trail
- Access attempt logging
- Permission tracking

## 🛠️ Technical Specifications

### Algorithms Used
- **SHA-256**: Cryptographic hashing
- **Proof of Work**: Blockchain mining simulation
- **UUID**: Unique identifier generation

### Data Structures
- **Python Lists**: Blockchain implementation
- **Dictionaries**: Data management
- **JSON**: Data serialization and storage

### Design Patterns
- **Service Layer**: Business logic separation
- **Repository Pattern**: Data access abstraction
- **MVC Architecture**: UI separation

## 🚨 Security Considerations

### Implemented Protections
- Input validation and sanitization
- Secure password storage
- Comprehensive audit logging
- Access control enforcement

### Limitations (Educational Purpose)
- Simplified blockchain implementation
- Local file storage (not production-ready)
- Basic authentication mechanism

## 🔮 Future Enhancements

### Planned Features
- Web-based user interface
- Real-time notifications
- Enhanced encryption algorithms
- Distributed blockchain network
- Mobile application support
- Integration with external healthcare systems

### Scalability Improvements
- Database integration
- Cloud storage support
- Load balancing
- Caching mechanisms

## 📞 Support & Troubleshooting

### Common Issues
1. **Python Version**: Ensure Python 3.7+ is installed
2. **File Permissions**: Check write access to application directory
3. **Port Conflict**: Ensure port 8080 is not in use for web server

### Debug Commands
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Run backend with verbose output
python backend/main.py

# Run web server with verbose output
python web/server.py
```

## 📄 License

This project is developed for educational purposes to demonstrate:
- Blockchain concepts in healthcare
- Secure data management principles
- Access control mechanisms
- Audit logging importance

Feel free to use, modify, and learn from this implementation.

## 🙏 Acknowledgments

This system serves as a comprehensive demonstration of how blockchain technology can revolutionize healthcare data management, ensuring security, privacy, and integrity in medical record handling.

---

**Note**: This is an educational simulation. For production healthcare systems, additional security measures, compliance requirements, and professional audits are necessary.
#   D H M S 
 
 