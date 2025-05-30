import re
import logging
from agents.memory_manager import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailAgent:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def process_email(self, thread_id, email_content):
        try:
            extracted_fields = {}
            anomalies = []

            sender_match = re.search(r"From: (.*?)\n", email_content)
            if sender_match:
                extracted_fields["sender"] = sender_match.group(1).strip()
            else:
                anomalies.append("Missing sender")

            subject_match = re.search(r"Subject: (.*?)\n", email_content)
            if subject_match:
                extracted_fields["subject"] = subject_match.group(1).strip()
            else:
                anomalies.append("Missing subject")

            extracted_fields["urgency"] = "High" if "urgent" in email_content.lower() else "Normal"

            self.memory_manager.store_context({
                "thread_id": thread_id,
                "format": "Email",
                "extracted_fields": extracted_fields,
                "anomalies": anomalies
            })

            return {
                "extracted_fields": extracted_fields,
                "anomalies": anomalies
            }

        except Exception as e:
            logger.error(f"Error processing email: {e}")
            return {"extracted_fields": {}, "anomalies": [f"Error: {e}"]}