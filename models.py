"""
Database models for Electero
"""
import sqlite3
from datetime import datetime
import json


class Database:
    """Database manager for storing calculation history"""

    def __init__(self, db_path='electero.db'):
        self.db_path = db_path

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn

    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                calc_type TEXT NOT NULL,
                inputs TEXT NOT NULL,
                results TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_calculation(self, calc_type, inputs, results):
        """Save a calculation to history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO calculations (calc_type, inputs, results)
            VALUES (?, ?, ?)
        ''', (calc_type, json.dumps(inputs), json.dumps(results)))

        conn.commit()
        calc_id = cursor.lastrowid
        conn.close()

        return calc_id

    def get_history(self, limit=50):
        """Get calculation history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, calc_type, inputs, results, timestamp
            FROM calculations
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'calc_type': row['calc_type'],
                'inputs': json.loads(row['inputs']),
                'results': json.loads(row['results']),
                'timestamp': row['timestamp']
            })

        return history

    def delete_calculation(self, calc_id):
        """Delete a calculation from history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM calculations WHERE id = ?', (calc_id,))

        conn.commit()
        conn.close()

    def clear_history(self):
        """Clear all calculation history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM calculations')

        conn.commit()
        conn.close()
