"""Database utilities for storing emission calculations."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class EmissionDatabase:
    """Simple SQLite database for storing emission calculations."""
    
    def __init__(self, db_path: str = "emissions.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS emissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    transport_emissions REAL NOT NULL,
                    energy_emissions REAL NOT NULL,
                    food_emissions REAL NOT NULL,
                    total_emissions REAL NOT NULL,
                    inputs_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def save_calculation(self, transport: float, energy: float, food: float, 
                        inputs: Dict[str, Any] = None) -> int:
        """Save an emission calculation to the database."""
        total = transport + energy + food
        date = datetime.now().strftime("%Y-%m-%d")
        inputs_json = json.dumps(inputs) if inputs else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO emissions (date, transport_emissions, energy_emissions, 
                                    food_emissions, total_emissions, inputs_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date, transport, energy, food, total, inputs_json))
            conn.commit()
            return cursor.lastrowid
    
    def get_historical_data(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get historical emission calculations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM emissions 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, float]:
        """Get monthly emission summary."""
        date_start = f"{year:04d}-{month:02d}-01"
        if month == 12:
            date_end = f"{year+1:04d}-01-01"
        else:
            date_end = f"{year:04d}-{month+1:02d}-01"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    AVG(transport_emissions) as avg_transport,
                    AVG(energy_emissions) as avg_energy,
                    AVG(food_emissions) as avg_food,
                    AVG(total_emissions) as avg_total,
                    COUNT(*) as calculation_count
                FROM emissions 
                WHERE date >= ? AND date < ?
            """, (date_start, date_end))
            row = cursor.fetchone()
            return {
                'avg_transport': row[0] or 0,
                'avg_energy': row[1] or 0,
                'avg_food': row[2] or 0,
                'avg_total': row[3] or 0,
                'calculation_count': row[4] or 0
            }
