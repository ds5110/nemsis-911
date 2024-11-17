import sqlite3


def create_database(db_path):
    try:
        # Connect to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the database with required tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pub_PCRevents (
                PcrKey TEXT PRIMARY KEY,
                eDispatch_01 INTEGER,
                eArrest_01 INTEGER,
                eArrest_02 INTEGER,
                eMedications_01 TEXT,
                eMedications_02 TEXT,
                -- Add more columns as needed
                ageinyear INTEGER
            )
        ''')

        print(f"Database created at: {db_path}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    # Set the path for the SQLite database file
    db_path = "NEMSIS_PUB.db"
    create_database(db_path)
