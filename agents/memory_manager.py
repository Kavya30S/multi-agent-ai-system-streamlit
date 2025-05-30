import sqlite3
import os
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, db_path="memory/memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS context (
                        thread_id TEXT PRIMARY KEY,
                        format TEXT,
                        intent TEXT,
                        extracted_fields TEXT,
                        anomalies TEXT,
                        content TEXT,
                        timestamp TEXT
                    )
                """)
                conn.commit()
                logger.info("Initialized database at %s", self.db_path)
        except sqlite3.Error as e:
            logger.error("Error initializing database: %s", e)

    def store_context(self, data):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO context
                    (thread_id, format, intent, extracted_fields, anomalies, content, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data.get("thread_id"),
                    data.get("format"),
                    data.get("intent"),
                    json.dumps(data.get("extracted_fields", {})),
                    json.dumps(data.get("anomalies", [])),
                    data.get("content"),
                    datetime.now().isoformat()
                ))
                conn.commit()
                logger.info("Stored context for thread_id: %s", data.get("thread_id"))
        except sqlite3.Error as e:
            logger.error("Error storing context: %s", e)

    def clear_memory(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM context")
                conn.commit()
                logger.info("Cleared memory database")
        except sqlite3.Error as e:
            logger.error("Error clearing memory: %s", e)