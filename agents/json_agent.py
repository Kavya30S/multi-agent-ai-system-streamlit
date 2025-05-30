import json
import logging
from agents.memory_manager import MemoryManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JsonAgent:
    def __init__(self):
        self.memory_manager = MemoryManager()

    def process_json(self, thread_id, json_data):
        try:
            if isinstance(json_data, str):
                data = json.loads(json_data)
            else:
                data = json_data

            expected_fields = {
                "invoice_number": str,
                "amount": float,
                "date": str,
                "sender": str
            }

            extracted_fields = {}
            anomalies = []

            for field, expected_type in expected_fields.items():
                if field in data:
                    value = data[field]
                    try:
                        if expected_type == float and not isinstance(value, (int, float)):
                            value = float(value)
                        if not isinstance(value, expected_type):
                            anomalies.append(f"Invalid type for {field}: expected {expected_type}, got {type(value)}")
                        extracted_fields[field] = value
                    except (ValueError, TypeError):
                        anomalies.append(f"Invalid value for {field}: {value}")
                else:
                    anomalies.append(f"Missing field: {field}")

            self.memory_manager.store_context({
                "thread_id": thread_id,
                "format": "JSON",
                "extracted_fields": extracted_fields,
                "anomalies": anomalies
            })

            return {
                "extracted_fields": extracted_fields,
                "anomalies": anomalies
            }

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON data: {e}")
            return {"extracted_fields": {}, "anomalies": [f"Invalid JSON: {e}"]}
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
            return {"extracted_fields": {}, "anomalies": [f"Error: {e}"]}