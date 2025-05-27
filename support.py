import json
import os
from datetime import datetime
import uuid

class SupportSystem:
    def __init__(self):
        self.support_data_file = "support_data.json"
        self.support_data = self._load_support_data()
        self.faq_categories = [
            "general",
            "account",
            "workout",
            "mindfulness",
            "nutrition",
            "technical",
            "privacy"
        ]

    def _load_support_data(self):
        """Load support data from JSON file"""
        if os.path.exists(self.support_data_file):
            with open(self.support_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "tickets": {},
            "faqs": {},
            "chat_sessions": {},
            "guides": {},
            "reports": {}
        }

    def _save_support_data(self):
        """Save support data to JSON file"""
        with open(self.support_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.support_data, f, ensure_ascii=False, indent=4)

    def create_ticket(self, user_id, subject, description, category, priority="medium"):
        """Create a new support ticket"""
        ticket_id = str(uuid.uuid4())
        ticket = {
            "id": ticket_id,
            "user_id": user_id,
            "subject": subject,
            "description": description,
            "category": category,
            "priority": priority,
            "status": "open",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "responses": []
        }
        
        self.support_data["tickets"][ticket_id] = ticket
        self._save_support_data()
        return ticket_id

    def add_ticket_response(self, ticket_id, user_id, message, is_staff=False):
        """Add a response to a support ticket"""
        if ticket_id not in self.support_data["tickets"]:
            return False, "Ticket not found"

        response = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "message": message,
            "is_staff": is_staff,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.support_data["tickets"][ticket_id]["responses"].append(response)
        self.support_data["tickets"][ticket_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_support_data()
        return True, "Response added successfully"

    def update_ticket_status(self, ticket_id, status):
        """Update the status of a support ticket"""
        if ticket_id not in self.support_data["tickets"]:
            return False, "Ticket not found"

        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return False, "Invalid status"

        self.support_data["tickets"][ticket_id]["status"] = status
        self.support_data["tickets"][ticket_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_support_data()
        return True, "Status updated successfully"

    def get_ticket(self, ticket_id):
        """Get ticket details"""
        return self.support_data["tickets"].get(ticket_id)

    def get_user_tickets(self, user_id):
        """Get all tickets for a user"""
        return [ticket for ticket in self.support_data["tickets"].values()
                if ticket["user_id"] == user_id]

    def add_faq(self, question, answer, category):
        """Add a new FAQ"""
        if category not in self.faq_categories:
            return False, "Invalid category"

        faq_id = str(uuid.uuid4())
        faq = {
            "id": faq_id,
            "question": question,
            "answer": answer,
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if category not in self.support_data["faqs"]:
            self.support_data["faqs"][category] = {}
        
        self.support_data["faqs"][category][faq_id] = faq
        self._save_support_data()
        return True, "FAQ added successfully"

    def get_faqs(self, category=None):
        """Get FAQs, optionally filtered by category"""
        if category:
            if category not in self.support_data["faqs"]:
                return []
            return list(self.support_data["faqs"][category].values())
        
        all_faqs = []
        for category_faqs in self.support_data["faqs"].values():
            all_faqs.extend(list(category_faqs.values()))
        return all_faqs

    def search_faqs(self, query):
        """Search FAQs by question or answer"""
        results = []
        query = query.lower()
        
        for category_faqs in self.support_data["faqs"].values():
            for faq in category_faqs.values():
                if (query in faq["question"].lower() or
                    query in faq["answer"].lower()):
                    results.append(faq)
        
        return results

    def start_chat_session(self, user_id):
        """Start a new chat support session"""
        session_id = str(uuid.uuid4())
        session = {
            "id": session_id,
            "user_id": user_id,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ended_at": None,
            "messages": [],
            "status": "active"
        }
        
        self.support_data["chat_sessions"][session_id] = session
        self._save_support_data()
        return session_id

    def add_chat_message(self, session_id, user_id, message, is_staff=False):
        """Add a message to a chat session"""
        if session_id not in self.support_data["chat_sessions"]:
            return False, "Session not found"

        chat_message = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "message": message,
            "is_staff": is_staff,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.support_data["chat_sessions"][session_id]["messages"].append(chat_message)
        self._save_support_data()
        return True, "Message added successfully"

    def end_chat_session(self, session_id):
        """End a chat support session"""
        if session_id not in self.support_data["chat_sessions"]:
            return False, "Session not found"

        self.support_data["chat_sessions"][session_id]["ended_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.support_data["chat_sessions"][session_id]["status"] = "ended"
        self._save_support_data()
        return True, "Session ended successfully"

    def get_chat_session(self, session_id):
        """Get chat session details"""
        return self.support_data["chat_sessions"].get(session_id)

    def get_user_chat_sessions(self, user_id):
        """Get all chat sessions for a user"""
        return [session for session in self.support_data["chat_sessions"].values()
                if session["user_id"] == user_id]

    def add_guide(self, title, content, category):
        """Add a new user guide"""
        if category not in self.faq_categories:
            return False, "Invalid category"

        guide_id = str(uuid.uuid4())
        guide = {
            "id": guide_id,
            "title": title,
            "content": content,
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if category not in self.support_data["guides"]:
            self.support_data["guides"][category] = {}
        
        self.support_data["guides"][category][guide_id] = guide
        self._save_support_data()
        return True, "Guide added successfully"

    def get_guides(self, category=None):
        """Get user guides, optionally filtered by category"""
        if category:
            if category not in self.support_data["guides"]:
                return []
            return list(self.support_data["guides"][category].values())
        
        all_guides = []
        for category_guides in self.support_data["guides"].values():
            all_guides.extend(list(category_guides.values()))
        return all_guides

    def search_guides(self, query):
        """Search guides by title or content"""
        results = []
        query = query.lower()
        
        for category_guides in self.support_data["guides"].values():
            for guide in category_guides.values():
                if (query in guide["title"].lower() or
                    query in guide["content"].lower()):
                    results.append(guide)
        
        return results

    def report_issue(self, user_id, issue_type, description, severity="medium"):
        """Report a technical issue"""
        report_id = str(uuid.uuid4())
        report = {
            "id": report_id,
            "user_id": user_id,
            "issue_type": issue_type,
            "description": description,
            "severity": severity,
            "status": "open",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resolution": None
        }
        
        self.support_data["reports"][report_id] = report
        self._save_support_data()
        return report_id

    def update_issue_status(self, report_id, status, resolution=None):
        """Update the status of a reported issue"""
        if report_id not in self.support_data["reports"]:
            return False, "Report not found"

        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            return False, "Invalid status"

        self.support_data["reports"][report_id]["status"] = status
        if resolution:
            self.support_data["reports"][report_id]["resolution"] = resolution
        self.support_data["reports"][report_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._save_support_data()
        return True, "Status updated successfully"

    def get_issue_report(self, report_id):
        """Get issue report details"""
        return self.support_data["reports"].get(report_id)

    def get_user_issue_reports(self, user_id):
        """Get all issue reports for a user"""
        return [report for report in self.support_data["reports"].values()
                if report["user_id"] == user_id] 