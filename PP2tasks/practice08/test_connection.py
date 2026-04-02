import psycopg2

DB_HOST = "localhost"
DB_NAME = "phonebook"
DB_USER = "altynajzumagalieva"
DB_PASSWORD = "Alixan08!"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Connected to PostgreSQL successfully!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)