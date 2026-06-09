// Healthcare Management System - Web Application
class HealthcareSystem {
    constructor() {
        this.patients = JSON.parse(localStorage.getItem('patients')) || [];
        this.doctors = JSON.parse(localStorage.getItem('doctors')) || [];
        this.medicalRecords = JSON.parse(localStorage.getItem('medicalRecords')) || [];
        this.blockchain = JSON.parse(localStorage.getItem('blockchain')) || [];
        this.auditLog = JSON.parse(localStorage.getItem('auditLog')) || [];
        
        this.initializeBlockchain();
        this.updateDashboard();
        this.loadAllData();
    }

    // Initialize blockchain with genesis block
    initializeBlockchain() {
        if (this.blockchain.length === 0) {
            const genesisBlock = {
                index: 0,
                timestamp: new Date().toISOString(),
                data: "Genesis Block - Healthcare System",
                previousHash: "0",
                nonce: 0,
                hash: this.calculateHash(0, "Genesis Block - Healthcare System", "0", 0)
            };
            this.blockchain.push(genesisBlock);
            this.saveBlockchain();
            this.logAudit("SYSTEM", "ADMIN", "BLOCKCHAIN_INIT", "0", "Genesis block created");
        }
    }

    // Calculate SHA-256 hash
    calculateHash(index, data, previousHash, nonce) {
        const input = index + data + previousHash + nonce;
        return CryptoJS.SHA256(input).toString();
    }

    // Mine a block (simplified proof of work)
    mineBlock(blockData) {
        const previousBlock = this.blockchain[this.blockchain.length - 1];
        const newBlock = {
            index: this.blockchain.length,
            timestamp: new Date().toISOString(),
            data: blockData,
            previousHash: previousBlock.hash,
            nonce: 0,
            hash: ""
        };

        // Simple mining (find hash starting with "00")
        let hash = this.calculateHash(newBlock.index, newBlock.data, newBlock.previousHash, newBlock.nonce);
        while (!hash.startsWith("00")) {
            newBlock.nonce++;
            hash = this.calculateHash(newBlock.index, newBlock.data, newBlock.previousHash, newBlock.nonce);
        }
        newBlock.hash = hash;

        this.blockchain.push(newBlock);
        this.saveBlockchain();
        return newBlock;
    }

    // Verify blockchain integrity
    verifyChain() {
        for (let i = 1; i < this.blockchain.length; i++) {
            const currentBlock = this.blockchain[i];
            const previousBlock = this.blockchain[i - 1];

            // Recalculate hash
            const calculatedHash = this.calculateHash(currentBlock.index, currentBlock.data, currentBlock.previousHash, currentBlock.nonce);
            
            if (currentBlock.hash !== calculatedHash) {
                return false;
            }

            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }
        return true;
    }

    // Generate unique ID
    generateUniqueId() {
        const timestamp = Date.now().toString();
        const random = Math.random().toString(36).substring(2);
        return CryptoJS.SHA256(timestamp + random).toString().substring(0, 32);
    }

    // Hash password
    hashPassword(password) {
        return CryptoJS.SHA256(password).toString();
    }

    // Audit logging
    logAudit(userId, userRole, action, targetId, details) {
        const entry = {
            timestamp: new Date().toISOString(),
            userId: userId,
            userRole: userRole,
            action: action,
            targetId: targetId,
            details: details
        };
        this.auditLog.unshift(entry);
        this.saveAuditLog();
    }

    // Patient registration
    registerPatient(patientData) {
        const patient = {
            patientId: this.generateUniqueId(),
            name: patientData.name,
            email: patientData.email,
            phone: patientData.phone,
            dateOfBirth: patientData.dateOfBirth,
            address: patientData.address,
            registrationDate: new Date().toISOString()
        };

        this.patients.push(patient);
        this.savePatients();
        this.logAudit(patient.patientId, "PATIENT", "REGISTRATION", patient.patientId, "Patient registered in system");
        this.updateDashboard();
        this.loadPatients();
        
        return patient;
    }

    // Doctor registration
    registerDoctor(doctorData) {
        const doctor = {
            doctorId: this.generateUniqueId(),
            name: doctorData.name,
            email: doctorData.email,
            specialization: doctorData.specialization,
            licenseNumber: doctorData.licenseNumber,
            passwordHash: this.hashPassword(doctorData.password),
            registrationDate: new Date().toISOString()
        };

        this.doctors.push(doctor);
        this.saveDoctors();
        this.logAudit(doctor.doctorId, "DOCTOR", "REGISTRATION", doctor.doctorId, "Doctor registered in system");
        this.updateDashboard();
        this.loadDoctors();
        
        return doctor;
    }

    // Create medical record
    createMedicalRecord(recordData) {
        const record = {
            recordId: this.generateUniqueId(),
            patientId: recordData.patientId,
            doctorId: recordData.doctorId,
            diagnosis: recordData.diagnosis,
            treatment: recordData.treatment,
            prescription: recordData.prescription,
            notes: recordData.notes,
            creationDate: new Date().toISOString()
        };

        // Create record hash
        const recordString = `${record.recordId}|${record.patientId}|${record.doctorId}|${record.diagnosis}|${record.treatment}|${record.prescription}|${record.notes}`;
        record.recordHash = CryptoJS.SHA256(recordString).toString();

        this.medicalRecords.push(record);
        this.saveMedicalRecords();

        // Add to blockchain
        const blockData = `MEDICAL_RECORD:${record.recordId}:${record.recordHash}`;
        this.mineBlock(blockData);

        this.logAudit(recordData.doctorId, "DOCTOR", "CREATE_RECORD", record.recordId, `Created medical record for patient ${record.patientId}`);
        this.updateDashboard();
        this.loadMedicalRecords();
        this.loadBlockchain();
        
        return record;
    }

    // Update dashboard
    updateDashboard() {
        document.getElementById('patientCount').textContent = this.patients.length;
        document.getElementById('doctorCount').textContent = this.doctors.length;
        document.getElementById('recordCount').textContent = this.medicalRecords.length;
        document.getElementById('blockCount').textContent = this.blockchain.length;

        // Update recent activity
        const recentActivity = document.getElementById('recentActivity');
        if (this.auditLog.length > 0) {
            const recent = this.auditLog.slice(0, 5);
            recentActivity.innerHTML = recent.map(entry => `
                <div class="alert alert-sm alert-info mb-2">
                    <small><strong>${entry.timestamp.split('T')[1].split('.')[0]}</strong> - ${entry.userRole} ${entry.userId}: ${entry.action}</small>
                </div>
            `).join('');
        }
    }

    // Load data into tables
    loadPatients() {
        const tbody = document.getElementById('patientsTableBody');
        if (this.patients.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No patients registered yet</td></tr>';
            return;
        }

        tbody.innerHTML = this.patients.map(patient => `
            <tr>
                <td><code>${patient.patientId.substring(0, 12)}...</code></td>
                <td>${patient.name}</td>
                <td>${patient.email}</td>
                <td>${patient.phone}</td>
                <td>${new Date(patient.registrationDate).toLocaleDateString()}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="viewPatient('${patient.patientId}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    loadDoctors() {
        const tbody = document.getElementById('doctorsTableBody');
        if (this.doctors.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No doctors registered yet</td></tr>';
            return;
        }

        tbody.innerHTML = this.doctors.map(doctor => `
            <tr>
                <td><code>${doctor.doctorId.substring(0, 12)}...</code></td>
                <td>${doctor.name}</td>
                <td>${doctor.email}</td>
                <td>${doctor.specialization}</td>
                <td>${doctor.licenseNumber}</td>
                <td>
                    <button class="btn btn-sm btn-outline-success" onclick="viewDoctor('${doctor.doctorId}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    loadMedicalRecords() {
        const tbody = document.getElementById('recordsTableBody');
        if (this.medicalRecords.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No medical records yet</td></tr>';
            return;
        }

        tbody.innerHTML = this.medicalRecords.map(record => `
            <tr>
                <td><code>${record.recordId.substring(0, 12)}...</code></td>
                <td><code>${record.patientId.substring(0, 8)}...</code></td>
                <td><code>${record.doctorId.substring(0, 8)}...</code></td>
                <td>${record.diagnosis.substring(0, 30)}...</td>
                <td>${record.treatment.substring(0, 20)}...</td>
                <td>${new Date(record.creationDate).toLocaleDateString()}</td>
                <td><code>${record.recordHash.substring(0, 12)}...</code></td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="viewRecord('${record.recordId}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    loadBlockchain() {
        const blockchainList = document.getElementById('blockchainList');
        blockchainList.innerHTML = this.blockchain.map((block, index) => `
            <div class="block-item">
                <div class="row">
                    <div class="col-md-8">
                        <h6><i class="fas fa-cube me-2"></i>Block #${block.index}</h6>
                        <p class="mb-1"><strong>Hash:</strong> <span class="block-hash">${block.hash}</span></p>
                        <p class="mb-1"><strong>Previous Hash:</strong> <span class="block-hash">${block.previousHash}</span></p>
                        <p class="mb-1"><strong>Nonce:</strong> ${block.nonce}</p>
                        <p class="mb-0"><strong>Timestamp:</strong> ${new Date(block.timestamp).toLocaleString()}</p>
                    </div>
                    <div class="col-md-4">
                        <p class="mb-2"><strong>Data:</strong></p>
                        <div class="block-data">${block.data}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    loadAuditLog() {
        const tbody = document.getElementById('auditTableBody');
        if (this.auditLog.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No audit entries yet</td></tr>';
            return;
        }

        tbody.innerHTML = this.auditLog.map(entry => `
            <tr>
                <td>${new Date(entry.timestamp).toLocaleString()}</td>
                <td><code>${entry.userId.substring(0, 8)}...</code></td>
                <td><span class="badge bg-secondary">${entry.userRole}</span></td>
                <td>${entry.action}</td>
                <td><code>${entry.targetId.substring(0, 8)}...</code></td>
                <td>${entry.details}</td>
            </tr>
        `).join('');
    }

    loadAllData() {
        this.loadPatients();
        this.loadDoctors();
        this.loadMedicalRecords();
        this.loadBlockchain();
        this.loadAuditLog();
    }

    // Storage methods
    savePatients() {
        localStorage.setItem('patients', JSON.stringify(this.patients));
    }

    saveDoctors() {
        localStorage.setItem('doctors', JSON.stringify(this.doctors));
    }

    saveMedicalRecords() {
        localStorage.setItem('medicalRecords', JSON.stringify(this.medicalRecords));
    }

    saveBlockchain() {
        localStorage.setItem('blockchain', JSON.stringify(this.blockchain));
    }

    saveAuditLog() {
        localStorage.setItem('auditLog', JSON.stringify(this.auditLog));
    }

    // View methods
    viewPatient(patientId) {
        const patient = this.patients.find(p => p.patientId === patientId);
        if (patient) {
            alert(`Patient Details:\n\nName: ${patient.name}\nEmail: ${patient.email}\nPhone: ${patient.phone}\nDOB: ${patient.dateOfBirth}\nAddress: ${patient.address}\nRegistered: ${new Date(patient.registrationDate).toLocaleString()}`);
        }
    }

    viewDoctor(doctorId) {
        const doctor = this.doctors.find(d => d.doctorId === doctorId);
        if (doctor) {
            alert(`Doctor Details:\n\nName: ${doctor.name}\nEmail: ${doctor.email}\nSpecialization: ${doctor.specialization}\nLicense: ${doctor.licenseNumber}\nRegistered: ${new Date(doctor.registrationDate).toLocaleString()}`);
        }
    }

    viewRecord(recordId) {
        const record = this.medicalRecords.find(r => r.recordId === recordId);
        if (record) {
            alert(`Medical Record Details:\n\nRecord ID: ${record.recordId}\nPatient ID: ${record.patientId}\nDoctor ID: ${record.doctorId}\nDiagnosis: ${record.diagnosis}\nTreatment: ${record.treatment}\nPrescription: ${record.prescription}\nNotes: ${record.notes}\nCreated: ${new Date(record.creationDate).toLocaleString()}\nHash: ${record.recordHash}`);
        }
    }

    // Clear audit log
    clearAuditLog() {
        if (confirm('Are you sure you want to clear the audit log?')) {
            this.auditLog = [];
            this.saveAuditLog();
            this.loadAuditLog();
            this.logAudit("SYSTEM", "ADMIN", "CLEAR_AUDIT", "SYSTEM", "Audit log cleared");
        }
    }

    // Verify chain
    verifyAndReportChain() {
        const isValid = this.verifyChain();
        const message = isValid ? 
            '✅ Blockchain integrity verified - All blocks are valid!' : 
            '❌ Blockchain integrity compromised - Some blocks are invalid!';
        
        alert(message);
        this.logAudit("SYSTEM", "ADMIN", "VERIFY_CHAIN", "BLOCKCHAIN", `Chain verification: ${isValid ? 'VALID' : 'INVALID'}`);
    }
}

// Initialize the system
let healthcareSystem;

// DOM loaded event
document.addEventListener('DOMContentLoaded', function() {
    healthcareSystem = new HealthcareSystem();
});

// Form submission handlers
function registerPatient() {
    const form = document.getElementById('patientForm');
    if (form.checkValidity()) {
        const patientData = {
            name: document.getElementById('patientName').value,
            email: document.getElementById('patientEmail').value,
            phone: document.getElementById('patientPhone').value,
            dateOfBirth: document.getElementById('patientDOB').value,
            address: document.getElementById('patientAddress').value
        };

        healthcareSystem.registerPatient(patientData);
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('patientModal'));
        modal.hide();
        form.reset();
        
        // Show success message
        showAlert('Patient registered successfully!', 'success');
    } else {
        form.reportValidity();
    }
}

function registerDoctor() {
    const form = document.getElementById('doctorForm');
    if (form.checkValidity()) {
        const doctorData = {
            name: document.getElementById('doctorName').value,
            email: document.getElementById('doctorEmail').value,
            specialization: document.getElementById('doctorSpecialization').value,
            licenseNumber: document.getElementById('doctorLicense').value,
            password: document.getElementById('doctorPassword').value
        };

        healthcareSystem.registerDoctor(doctorData);
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('doctorModal'));
        modal.hide();
        form.reset();
        
        // Show success message
        showAlert('Doctor registered successfully!', 'success');
    } else {
        form.reportValidity();
    }
}

function createMedicalRecord() {
    const form = document.getElementById('recordForm');
    if (form.checkValidity()) {
        const recordData = {
            patientId: document.getElementById('recordPatient').value,
            doctorId: document.getElementById('recordDoctor').value,
            diagnosis: document.getElementById('recordDiagnosis').value,
            treatment: document.getElementById('recordTreatment').value,
            prescription: document.getElementById('recordPrescription').value,
            notes: document.getElementById('recordNotes').value
        };

        // Verify patient and doctor exist
        const patient = healthcareSystem.patients.find(p => p.patientId === recordData.patientId);
        const doctor = healthcareSystem.doctors.find(d => d.doctorId === recordData.doctorId);

        if (!patient) {
            showAlert('Patient ID not found!', 'danger');
            return;
        }

        if (!doctor) {
            showAlert('Doctor ID not found!', 'danger');
            return;
        }

        healthcareSystem.createMedicalRecord(recordData);
        
        // Close modal and reset form
        const modal = bootstrap.Modal.getInstance(document.getElementById('recordModal'));
        modal.hide();
        form.reset();
        
        // Show success message
        showAlert('Medical record created successfully!', 'success');
    } else {
        form.reportValidity();
    }
}

// Utility functions
function viewPatient(patientId) {
    healthcareSystem.viewPatient(patientId);
}

function viewDoctor(doctorId) {
    healthcareSystem.viewDoctor(doctorId);
}

function viewRecord(recordId) {
    healthcareSystem.viewRecord(recordId);
}

function clearAuditLog() {
    healthcareSystem.clearAuditLog();
}

function verifyChain() {
    healthcareSystem.verifyAndReportChain();
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// Tab change event to refresh data
document.addEventListener('shown.bs.tab', function (event) {
    const target = event.target.getAttribute('data-bs-target');
    
    if (target === '#patients') {
        healthcareSystem.loadPatients();
    } else if (target === '#doctors') {
        healthcareSystem.loadDoctors();
    } else if (target === '#records') {
        healthcareSystem.loadMedicalRecords();
    } else if (target === '#blockchain') {
        healthcareSystem.loadBlockchain();
    } else if (target === '#audit') {
        healthcareSystem.loadAuditLog();
    }
});
