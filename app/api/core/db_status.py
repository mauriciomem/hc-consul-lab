# core/db_status.py
from typing import Dict, Any, Optional
from datetime import datetime

class DatabaseStatus:
    """Singleton class to manage database connection status"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseStatus, cls).__new__(cls)
            cls._instance.status = {
                "is_connected": False,
                "last_check": None
            }
        return cls._instance
    
    def update_status(self, is_connected: bool) -> None:
        """Update the database connection status"""
        self.status["is_connected"] = is_connected
        self.status["last_check"] = datetime.now().isoformat()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current database status"""
        return {
            "database_connected": self.status["is_connected"],
            "last_check": self.status["last_check"]
        }

db_status = DatabaseStatus()