import json
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from decimal import Decimal

class TrainerPaymentManager:
    def __init__(self):
        self.payments_file = "trainer_payments.json"
        self.accounts_file = "trainer_accounts.json"
        self.withdrawals_file = "trainer_withdrawals.json"
        self._load_data()

    def _load_data(self):
        """Load payment and account data from JSON files"""
        if os.path.exists(self.payments_file):
            with open(self.payments_file, 'r', encoding='utf-8') as f:
                self.payments = json.load(f)
        else:
            self.payments = {}

        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {}

        if os.path.exists(self.withdrawals_file):
            with open(self.withdrawals_file, 'r', encoding='utf-8') as f:
                self.withdrawals = json.load(f)
        else:
            self.withdrawals = {}

    def _save_data(self):
        """Save payment and account data to JSON files"""
        with open(self.payments_file, 'w', encoding='utf-8') as f:
            json.dump(self.payments, f, ensure_ascii=False, indent=4)
        
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=4)
        
        with open(self.withdrawals_file, 'w', encoding='utf-8') as f:
            json.dump(self.withdrawals, f, ensure_ascii=False, indent=4)

    def create_trainer_account(self, trainer_id: str, bank_info: Dict) -> bool:
        """Create a financial account for a trainer"""
        if trainer_id in self.accounts:
            return False

        self.accounts[trainer_id] = {
            "bank_info": bank_info,
            "balance": 0.0,
            "total_earnings": 0.0,
            "pending_withdrawals": 0.0,
            "payment_methods": [],
            "created_at": datetime.now().isoformat()
        }
        self._save_data()
        return True

    def add_payment_method(self, trainer_id: str, payment_method: Dict) -> bool:
        """Add a payment method for a trainer"""
        if trainer_id not in self.accounts:
            return False

        payment_method_id = str(uuid.uuid4())
        self.accounts[trainer_id]["payment_methods"].append({
            "id": payment_method_id,
            **payment_method
        })
        self._save_data()
        return True

    def process_session_payment(self, session_id: str, amount: float) -> bool:
        """Process payment for a training session"""
        if session_id not in self.payments:
            return False

        payment = self.payments[session_id]
        trainer_id = payment["trainer_id"]
        
        if trainer_id not in self.accounts:
            return False

        # Calculate platform fee (e.g., 20%)
        platform_fee = amount * 0.20
        trainer_amount = amount - platform_fee

        # Update trainer's balance
        self.accounts[trainer_id]["balance"] += trainer_amount
        self.accounts[trainer_id]["total_earnings"] += trainer_amount

        # Update payment record
        payment["status"] = "completed"
        payment["platform_fee"] = platform_fee
        payment["trainer_amount"] = trainer_amount
        payment["completed_at"] = datetime.now().isoformat()

        self._save_data()
        return True

    def request_withdrawal(self, trainer_id: str, amount: float, 
                          payment_method_id: str) -> Optional[str]:
        """Request a withdrawal of earnings"""
        if trainer_id not in self.accounts:
            return None

        account = self.accounts[trainer_id]
        if amount > account["balance"]:
            return None

        withdrawal_id = str(uuid.uuid4())
        self.withdrawals[withdrawal_id] = {
            "trainer_id": trainer_id,
            "amount": amount,
            "payment_method_id": payment_method_id,
            "status": "pending",
            "requested_at": datetime.now().isoformat()
        }

        # Update account balance
        account["balance"] -= amount
        account["pending_withdrawals"] += amount

        self._save_data()
        return withdrawal_id

    def process_withdrawal(self, withdrawal_id: str) -> bool:
        """Process a withdrawal request"""
        if withdrawal_id not in self.withdrawals:
            return False

        withdrawal = self.withdrawals[withdrawal_id]
        trainer_id = withdrawal["trainer_id"]

        if trainer_id not in self.accounts:
            return False

        # Update withdrawal status
        withdrawal["status"] = "completed"
        withdrawal["completed_at"] = datetime.now().isoformat()

        # Update account
        self.accounts[trainer_id]["pending_withdrawals"] -= withdrawal["amount"]

        self._save_data()
        return True

    def get_trainer_earnings(self, trainer_id: str, 
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> Dict:
        """Get trainer's earnings summary"""
        if trainer_id not in self.accounts:
            return None

        earnings = {
            "total_earnings": 0.0,
            "available_balance": 0.0,
            "pending_withdrawals": 0.0,
            "platform_fees": 0.0,
            "sessions": []
        }

        for session_id, payment in self.payments.items():
            if payment["trainer_id"] == trainer_id:
                if start_date and payment["date"] < start_date:
                    continue
                if end_date and payment["date"] > end_date:
                    continue

                if payment["status"] == "completed":
                    earnings["total_earnings"] += payment["trainer_amount"]
                    earnings["platform_fees"] += payment["platform_fee"]
                    earnings["sessions"].append(payment)

        account = self.accounts[trainer_id]
        earnings["available_balance"] = account["balance"]
        earnings["pending_withdrawals"] = account["pending_withdrawals"]

        return earnings

    def get_payment_history(self, trainer_id: str) -> List[Dict]:
        """Get trainer's payment history"""
        history = []
        for session_id, payment in self.payments.items():
            if payment["trainer_id"] == trainer_id:
                history.append(payment)
        return sorted(history, key=lambda x: x["date"], reverse=True)

    def get_withdrawal_history(self, trainer_id: str) -> List[Dict]:
        """Get trainer's withdrawal history"""
        history = []
        for withdrawal_id, withdrawal in self.withdrawals.items():
            if withdrawal["trainer_id"] == trainer_id:
                history.append(withdrawal)
        return sorted(history, key=lambda x: x["requested_at"], reverse=True)

    def calculate_monthly_earnings(self, trainer_id: str, year: int, 
                                 month: int) -> Dict:
        """Calculate trainer's earnings for a specific month"""
        if trainer_id not in self.accounts:
            return None

        monthly_earnings = {
            "total_earnings": 0.0,
            "platform_fees": 0.0,
            "sessions_count": 0,
            "average_session_amount": 0.0
        }

        for session_id, payment in self.payments.items():
            if payment["trainer_id"] == trainer_id:
                payment_date = datetime.fromisoformat(payment["date"])
                if (payment_date.year == year and 
                    payment_date.month == month and 
                    payment["status"] == "completed"):
                    monthly_earnings["total_earnings"] += payment["trainer_amount"]
                    monthly_earnings["platform_fees"] += payment["platform_fee"]
                    monthly_earnings["sessions_count"] += 1

        if monthly_earnings["sessions_count"] > 0:
            monthly_earnings["average_session_amount"] = (
                monthly_earnings["total_earnings"] / monthly_earnings["sessions_count"]
            )

        return monthly_earnings 