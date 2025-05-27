from datetime import datetime, timedelta
import json
import os
import schedule
import time
import threading

class ReminderSystem:
    def __init__(self):
        self.reminders_file = "reminders.json"
        self.reminders = self._load_reminders()
        self.notification_thread = None
        self.is_running = False

    def _load_reminders(self):
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_reminders(self):
        with open(self.reminders_file, 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, ensure_ascii=False, indent=4)

    def add_reminder(self, user_id, reminder_type, time, message, repeat_daily=False):
        if user_id not in self.reminders:
            self.reminders[user_id] = []
        
        reminder = {
            "type": reminder_type,  # workout, emotion, water, etc.
            "time": time,  # HH:MM format
            "message": message,
            "repeat_daily": repeat_daily,
            "created_at": datetime.now().isoformat(),
            "last_triggered": None
        }
        
        self.reminders[user_id].append(reminder)
        self._save_reminders()
        return reminder

    def get_reminders(self, user_id):
        return self.reminders.get(user_id, [])

    def remove_reminder(self, user_id, reminder_index):
        if user_id in self.reminders and 0 <= reminder_index < len(self.reminders[user_id]):
            self.reminders[user_id].pop(reminder_index)
            self._save_reminders()
            return True
        return False

    def start_notification_service(self):
        if self.notification_thread is None or not self.notification_thread.is_alive():
            self.is_running = True
            self.notification_thread = threading.Thread(target=self._check_reminders)
            self.notification_thread.daemon = True
            self.notification_thread.start()

    def stop_notification_service(self):
        self.is_running = False
        if self.notification_thread:
            self.notification_thread.join()

    def _check_reminders(self):
        while self.is_running:
            current_time = datetime.now().strftime("%H:%M")
            for user_id, user_reminders in self.reminders.items():
                for reminder in user_reminders:
                    if reminder["time"] == current_time:
                        self._send_notification(user_id, reminder)
                        reminder["last_triggered"] = datetime.now().isoformat()
                        self._save_reminders()
            time.sleep(30)  # Check every 30 seconds

    def _send_notification(self, user_id, reminder):
        # In a real application, this would send a push notification
        # For now, we'll just print to console
        print(f"\n🔔 Reminder for user {user_id}:")
        print(f"Message: {reminder['message']}")
        print(f"Type: {reminder['type']}")
        print("----------------------------------------") 