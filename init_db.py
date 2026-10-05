"""
Initialize the Electero database
"""
from models import Database

if __name__ == '__main__':
    db = Database()
    db.init_db()
    print("Database initialized successfully!")
    print("Table 'calculations' created")
