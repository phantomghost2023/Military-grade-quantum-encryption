import unittest
from src.database import connect_db, disconnect_db, execute_query

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Set up a test database connection (e.g., in-memory SQLite)
        self.conn = connect_db(':memory:')

    def tearDown(self):
        # Disconnect from the test database
        disconnect_db(self.conn)

    def test_connect_and_disconnect_db(self):
        self.assertIsNotNone(self.conn)
        # Test if disconnect works without errors
        disconnect_db(self.conn)
        self.assertIsNone(self.conn.cursor().connection) # Check if connection is closed

    def test_execute_query(self):
        # Create a test table and insert data
        execute_query(self.conn, 'CREATE TABLE test_table (id INTEGER, name TEXT)')
        execute_query(self.conn, "INSERT INTO test_table (id, name) VALUES (1, 'test_name')")

        # Fetch data and assert
        result = execute_query(self.conn, 'SELECT * FROM test_table')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (1, 'test_name'))

if __name__ == '__main__';
    unittest.main()