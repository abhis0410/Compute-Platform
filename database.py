import sqlite3
import pandas as pd
from datetime import datetime

class DatabaseHandler:
    '''
    db model used: 
    user_id, file_name, column_name, operation, result, date, time
    '''
    def __init__(self, db_name="results.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        """Establish a connection to the database."""
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        """Create the results table if it doesn't exist."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    file_name TEXT,
                    column_name TEXT,
                    operation TEXT,
                    result TEXT,
                    date TEXT,
                    time TEXT
                )
            ''')
            conn.commit()

    def store_result(self, user_id, file_name, column_name, operation, result):
        """Store a result in the database."""
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (user_id, file_name, column_name, operation, result, date, time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, file_name, column_name, operation, result, current_date, current_time))
            conn.commit()

    def fetch_results(self, user_id):
        """Fetch all results for a given user ID, sorted by date and time in descending order."""
        with self._connect() as conn:
            query = '''
                SELECT user_id, file_name, column_name, operation, result, date, time
                FROM results
                WHERE user_id = ?
                ORDER BY date DESC, time DESC
            '''
            df = pd.read_sql_query(query, conn, params=(user_id,))
        return df
