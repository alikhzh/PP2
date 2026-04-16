import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="phonebook",
            user="alikh",
            password="Alixan08!",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None