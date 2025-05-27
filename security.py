import json
import os
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    def __init__(self):
        self.security_data_file = "security_data.json"
        self.security_data = self._load_security_data()
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        self.jwt_secret = os.getenv("JWT_SECRET", secrets.token_hex(32))
        self.jwt_algorithm = "HS256"
        self.jwt_expiry = timedelta(days=1)

    def _load_security_data(self):
        """Load security data from JSON file"""
        if os.path.exists(self.security_data_file):
            with open(self.security_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "users": {},
            "sessions": {},
            "backups": [],
            "privacy_settings": {}
        }

    def _save_security_data(self):
        """Save security data to JSON file"""
        with open(self.security_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.security_data, f, ensure_ascii=False, indent=4)

    def _generate_encryption_key(self):
        """Generate encryption key for data encryption"""
        if os.path.exists("encryption.key"):
            with open("encryption.key", "rb") as f:
                return f.read()
        
        key = Fernet.generate_key()
        with open("encryption.key", "wb") as f:
            f.write(key)
        return key

    def _hash_password(self, password, salt=None):
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode(), salt

    def register_user(self, user_id, password, email):
        """Register a new user with secure password storage"""
        if user_id in self.security_data["users"]:
            return False, "User already exists"

        # Hash password
        hashed_password, salt = self._hash_password(password)
        
        # Store user data
        self.security_data["users"][user_id] = {
            "password_hash": hashed_password,
            "salt": salt,
            "email": self.encrypt_data(email),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None,
            "failed_attempts": 0,
            "two_factor_enabled": False,
            "two_factor_secret": None
        }
        
        # Initialize privacy settings
        self.security_data["privacy_settings"][user_id] = {
            "profile_visibility": "private",
            "activity_sharing": False,
            "data_collection": True,
            "location_sharing": False,
            "notifications": True
        }
        
        self._save_security_data()
        return True, "User registered successfully"

    def authenticate_user(self, user_id, password):
        """Authenticate user with password"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        user_data = self.security_data["users"][user_id]
        
        # Check for too many failed attempts
        if user_data["failed_attempts"] >= 5:
            return False, "Account locked due to too many failed attempts"

        # Verify password
        hashed_password, _ = self._hash_password(password, user_data["salt"])
        if hashed_password != user_data["password_hash"]:
            user_data["failed_attempts"] += 1
            self._save_security_data()
            return False, "Invalid password"

        # Reset failed attempts and update last login
        user_data["failed_attempts"] = 0
        user_data["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_security_data()

        # Generate JWT token
        token = self._generate_jwt_token(user_id)
        return True, token

    def _generate_jwt_token(self, user_id):
        """Generate JWT token for user"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + self.jwt_expiry
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return True, payload["user_id"]
        except jwt.ExpiredSignatureError:
            return False, "Token expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"

    def enable_two_factor(self, user_id):
        """Enable two-factor authentication for user"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        # Generate secret key for 2FA
        secret = secrets.token_hex(16)
        self.security_data["users"][user_id]["two_factor_enabled"] = True
        self.security_data["users"][user_id]["two_factor_secret"] = self.encrypt_data(secret)
        self._save_security_data()
        return True, secret

    def verify_two_factor(self, user_id, code):
        """Verify two-factor authentication code"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        user_data = self.security_data["users"][user_id]
        if not user_data["two_factor_enabled"]:
            return False, "2FA not enabled"

        # In a real app, you would verify the code against the secret
        # This is a simplified version
        return True, "2FA verified"

    def encrypt_data(self, data):
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data).decode()

    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return None

    def update_privacy_settings(self, user_id, settings):
        """Update user's privacy settings"""
        if user_id not in self.security_data["privacy_settings"]:
            return False, "User not found"

        self.security_data["privacy_settings"][user_id].update(settings)
        self._save_security_data()
        return True, "Privacy settings updated"

    def get_privacy_settings(self, user_id):
        """Get user's privacy settings"""
        if user_id not in self.security_data["privacy_settings"]:
            return None
        return self.security_data["privacy_settings"][user_id]

    def create_backup(self, user_id):
        """Create a backup of user's data"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        backup = {
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data": self.encrypt_data(json.dumps(self.security_data["users"][user_id]))
        }
        
        self.security_data["backups"].append(backup)
        self._save_security_data()
        return True, "Backup created successfully"

    def restore_backup(self, user_id, backup_timestamp):
        """Restore user's data from backup"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        # Find backup
        backup = next((b for b in self.security_data["backups"]
                      if b["user_id"] == user_id and b["timestamp"] == backup_timestamp), None)
        
        if not backup:
            return False, "Backup not found"

        # Restore data
        try:
            decrypted_data = json.loads(self.decrypt_data(backup["data"]))
            self.security_data["users"][user_id] = decrypted_data
            self._save_security_data()
            return True, "Backup restored successfully"
        except Exception as e:
            return False, f"Error restoring backup: {str(e)}"

    def delete_user_data(self, user_id):
        """Delete user's data (GDPR compliance)"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        # Remove user data
        del self.security_data["users"][user_id]
        del self.security_data["privacy_settings"][user_id]
        
        # Remove user's backups
        self.security_data["backups"] = [b for b in self.security_data["backups"]
                                       if b["user_id"] != user_id]
        
        self._save_security_data()
        return True, "User data deleted successfully"

    def get_security_logs(self, user_id):
        """Get security logs for user"""
        if user_id not in self.security_data["users"]:
            return None

        user_data = self.security_data["users"][user_id]
        return {
            "last_login": user_data["last_login"],
            "failed_attempts": user_data["failed_attempts"],
            "two_factor_enabled": user_data["two_factor_enabled"],
            "created_at": user_data["created_at"]
        }

    def change_password(self, user_id, old_password, new_password):
        """Change user's password"""
        if user_id not in self.security_data["users"]:
            return False, "User not found"

        user_data = self.security_data["users"][user_id]
        
        # Verify old password
        hashed_password, _ = self._hash_password(old_password, user_data["salt"])
        if hashed_password != user_data["password_hash"]:
            return False, "Invalid old password"

        # Hash new password
        new_hashed_password, new_salt = self._hash_password(new_password)
        
        # Update password
        user_data["password_hash"] = new_hashed_password
        user_data["salt"] = new_salt
        user_data["failed_attempts"] = 0
        
        self._save_security_data()
        return True, "Password changed successfully" 