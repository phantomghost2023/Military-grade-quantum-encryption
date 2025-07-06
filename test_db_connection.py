import psycopg2

def test_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="quantum_encryption",
            user="postgres",
            password="your_postgres_password" # Replace with your actual password
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print("Successfully connected to the database and executed a query.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()