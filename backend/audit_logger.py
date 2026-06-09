"""
Audit Logger for Healthcare Management System
"""

import os
from datetime import datetime
from pathlib import Path


class AuditLogger:
    """Audit logging for system activities"""
    
    def __init__(self, data_directory="healthcare_data"):
        self.data_directory = data_directory
        self.audit_file = os.path.join(data_directory, "audit.log")
        self._create_data_directory()
    
    def _create_data_directory(self):
        """Create data directory if it doesn't exist"""
        Path(self.data_directory).mkdir(parents=True, exist_ok=True)
    
    def log_audit(self, user_id, user_role, action, target_id, details):
        """Log an audit entry"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {user_id}|{user_role}|{action}|{target_id}|{details}\n"
        
        try:
            with open(self.audit_file, 'a') as f:
                f.write(log_entry)
        except IOError as e:
            print(f"Error writing to audit log: {e}")
    
    def print_audit_log(self):
        """Print the audit log to console"""
        if not os.path.exists(self.audit_file):
            print("No audit log found.")
            return
        
        try:
            with open(self.audit_file, 'r') as f:
                print("=== AUDIT LOG ===")
                print(f.read())
        except IOError as e:
            print(f"Error reading audit log: {e}")
    
    def clear_audit_log(self):
        """Clear the audit log"""
        if os.path.exists(self.audit_file):
            os.remove(self.audit_file)
        self.log_audit("SYSTEM", "ADMIN", "CLEAR_AUDIT", "SYSTEM", "Audit log cleared")
    
    def get_audit_entries(self):
        """Get all audit entries as a list"""
        if not os.path.exists(self.audit_file):
            return []
        
        try:
            with open(self.audit_file, 'r') as f:
                lines = f.readlines()
                entries = []
                for line in lines:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) >= 6:
                            timestamp = parts[0].strip('[]')
                            user_id = parts[1]
                            user_role = parts[2]
                            action = parts[3]
                            target_id = parts[4]
                            details = '|'.join(parts[5:])
                            entries.append({
                                'timestamp': timestamp,
                                'user_id': user_id,
                                'user_role': user_role,
                                'action': action,
                                'target_id': target_id,
                                'details': details
                            })
                return entries
        except IOError as e:
            print(f"Error reading audit log: {e}")
            return []
