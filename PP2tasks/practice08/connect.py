import psycopg2
import config

def connect():
    try:
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password
        )
        return conn
    except Exception as e:
        print("Connection failed:", e)
        return None