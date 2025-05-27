import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class TrainerType(Enum):
    YOGA = "yoga"
    MEDITATION = "meditation"
    NUTRITION = "nutrition"
    GENERAL = "general"

class VerificationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

class TrainerVerificationManager:
    def __init__(self):
        self.verifications_file = "trainer_verifications.json"
        self.certifications_file = "certifications.json"
        self.specializations_file = "specializations.json"
        self._load_data()

    def _load_data(self):
        """Load verification and certification data from JSON files"""
        if os.path.exists(self.verifications_file):
            with open(self.verifications_file, 'r', encoding='utf-8') as f:
                self.verifications = json.load(f)
        else:
            self.verifications = {}

        if os.path.exists(self.certifications_file):
            with open(self.certifications_file, 'r', encoding='utf-8') as f:
                self.certifications = json.load(f)
        else:
            self.certifications = {}

        if os.path.exists(self.specializations_file):
            with open(self.specializations_file, 'r', encoding='utf-8') as f:
                self.specializations = json.load(f)
        else:
            self.specializations = {}

    def _save_data(self):
        """Save verification and certification data to JSON files"""
        with open(self.verifications_file, 'w', encoding='utf-8') as f:
            json.dump(self.verifications, f, ensure_ascii=False, indent=4)
        
        with open(self.certifications_file, 'w', encoding='utf-8') as f:
            json.dump(self.certifications, f, ensure_ascii=False, indent=4)
        
        with open(self.specializations_file, 'w', encoding='utf-8') as f:
            json.dump(self.specializations, f, ensure_ascii=False, indent=4)

    def register_specialization(self, trainer_id: str, trainer_type: TrainerType,
                              specialization_data: Dict) -> bool:
        """Register a trainer's specialization"""
        if trainer_id not in self.specializations:
            self.specializations[trainer_id] = []

        specialization = {
            "id": str(uuid.uuid4()),
            "type": trainer_type.value,
            "data": specialization_data,
            "status": VerificationStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "verified_at": None,
            "expires_at": None
        }

        self.specializations[trainer_id].append(specialization)
        self._save_data()
        return True

    def submit_certification(self, trainer_id: str, certification_data: Dict) -> str:
        """Submit a certification for verification"""
        certification_id = str(uuid.uuid4())
        self.certifications[certification_id] = {
            "trainer_id": trainer_id,
            "data": certification_data,
            "status": VerificationStatus.PENDING.value,
            "submitted_at": datetime.now().isoformat(),
            "verified_at": None,
            "expires_at": None,
            "verifier_notes": ""
        }
        self._save_data()
        return certification_id

    def verify_certification(self, certification_id: str, 
                           verifier_id: str, approved: bool,
                           notes: str = "") -> bool:
        """Verify a certification"""
        if certification_id not in self.certifications:
            return False

        certification = self.certifications[certification_id]
        certification["status"] = (
            VerificationStatus.APPROVED.value if approved 
            else VerificationStatus.REJECTED.value
        )
        certification["verified_at"] = datetime.now().isoformat()
        certification["verifier_id"] = verifier_id
        certification["verifier_notes"] = notes

        if approved:
            # Set expiration date (e.g., 2 years from now)
            certification["expires_at"] = (
                datetime.now() + timedelta(days=730)
            ).isoformat()

        self._save_data()
        return True

    def verify_specialization(self, trainer_id: str, specialization_id: str,
                            verifier_id: str, approved: bool,
                            notes: str = "") -> bool:
        """Verify a trainer's specialization"""
        if trainer_id not in self.specializations:
            return False

        for specialization in self.specializations[trainer_id]:
            if specialization["id"] == specialization_id:
                specialization["status"] = (
                    VerificationStatus.APPROVED.value if approved 
                    else VerificationStatus.REJECTED.value
                )
                specialization["verified_at"] = datetime.now().isoformat()
                specialization["verifier_id"] = verifier_id
                specialization["verifier_notes"] = notes

                if approved:
                    # Set expiration date (e.g., 2 years from now)
                    specialization["expires_at"] = (
                        datetime.now() + timedelta(days=730)
                    ).isoformat()

                self._save_data()
                return True

        return False

    def get_trainer_verifications(self, trainer_id: str) -> Dict:
        """Get all verifications for a trainer"""
        return {
            "specializations": self.specializations.get(trainer_id, []),
            "certifications": [
                cert for cert_id, cert in self.certifications.items()
                if cert["trainer_id"] == trainer_id
            ]
        }

    def check_verification_status(self, trainer_id: str, 
                                trainer_type: TrainerType) -> Dict:
        """Check verification status for a specific trainer type"""
        if trainer_id not in self.specializations:
            return {
                "verified": False,
                "status": VerificationStatus.PENDING.value,
                "expires_at": None
            }

        for specialization in self.specializations[trainer_id]:
            if specialization["type"] == trainer_type.value:
                return {
                    "verified": specialization["status"] == VerificationStatus.APPROVED.value,
                    "status": specialization["status"],
                    "expires_at": specialization["expires_at"]
                }

        return {
            "verified": False,
            "status": VerificationStatus.PENDING.value,
            "expires_at": None
        }

    def get_pending_verifications(self) -> Dict:
        """Get all pending verifications"""
        pending = {
            "certifications": [],
            "specializations": []
        }

        for cert_id, cert in self.certifications.items():
            if cert["status"] == VerificationStatus.PENDING.value:
                pending["certifications"].append({
                    "id": cert_id,
                    **cert
                })

        for trainer_id, specializations in self.specializations.items():
            for spec in specializations:
                if spec["status"] == VerificationStatus.PENDING.value:
                    pending["specializations"].append({
                        "trainer_id": trainer_id,
                        **spec
                    })

        return pending

    def get_expired_verifications(self) -> Dict:
        """Get all expired verifications"""
        expired = {
            "certifications": [],
            "specializations": []
        }
        now = datetime.now()

        for cert_id, cert in self.certifications.items():
            if cert["expires_at"]:
                expires_at = datetime.fromisoformat(cert["expires_at"])
                if expires_at < now:
                    expired["certifications"].append({
                        "id": cert_id,
                        **cert
                    })

        for trainer_id, specializations in self.specializations.items():
            for spec in specializations:
                if spec["expires_at"]:
                    expires_at = datetime.fromisoformat(spec["expires_at"])
                    if expires_at < now:
                        expired["specializations"].append({
                            "trainer_id": trainer_id,
                            **spec
                        })

        return expired

    def renew_verification(self, trainer_id: str, verification_type: str,
                         verification_id: str) -> bool:
        """Request renewal of an expired verification"""
        if verification_type == "certification":
            if verification_id not in self.certifications:
                return False
            
            cert = self.certifications[verification_id]
            if cert["trainer_id"] != trainer_id:
                return False

            cert["status"] = VerificationStatus.PENDING.value
            cert["renewal_requested_at"] = datetime.now().isoformat()

        elif verification_type == "specialization":
            if trainer_id not in self.specializations:
                return False

            for spec in self.specializations[trainer_id]:
                if spec["id"] == verification_id:
                    spec["status"] = VerificationStatus.PENDING.value
                    spec["renewal_requested_at"] = datetime.now().isoformat()
                    break
            else:
                return False

        self._save_data()
        return True 