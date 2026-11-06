
import sqlite3
import os


# Database File Location
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "techresolve.db"
)


# 1. Connect to Database
def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


# 2. Create Diagnostic History Table
def initialize_database():

    os.makedirs(
        os.path.dirname(DATABASE_PATH),
        exist_ok=True
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS diagnostic_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            internet_status TEXT,

            performance_status TEXT,

            storage_status TEXT,

            dns_status TEXT,

            cpu_usage REAL,

            ram_usage REAL,

            timestamp TEXT

        )

    """)

    connection.commit()

    connection.close()


# 3. Save Diagnostic Report
def save_diagnostic(report):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO diagnostic_history (

            internet_status,
            performance_status,
            storage_status,
            dns_status,
            cpu_usage,
            ram_usage,
            timestamp

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        report["internet"]["status"],

        report["performance"]["status"],

        report["storage"]["status"],

        report["dns"]["status"],

        report["performance"]["cpu"],

        report["performance"]["ram"],

        report["timestamp"]

    ))

    connection.commit()

    connection.close()


# 4. Get Diagnostic History
def get_diagnostic_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        SELECT * FROM diagnostic_history

        ORDER BY id DESC

    """)

    records = [
        dict(row)
        for row in cursor.fetchall()
    ]

    connection.close()

    return records
