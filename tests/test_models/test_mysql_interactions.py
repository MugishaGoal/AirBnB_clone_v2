import unittest
import MySQLdb
from your_project_module import create_state_in_console

class TestMySQLInteractions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up MySQL connection for testing"""
        cls.db = MySQLdb.connect(user='hbnb_test', passwd='hbnb_test_pwd', host='localhost', db='hbnb_test_db')
        cls.cursor = cls.db.cursor()

    @classmethod
    def tearDownClass(cls):
        """Close MySQL connection after testing"""
        cls.db.close()

    def test_create_state_in_console(self):
        """Get the initial number of records"""
        initial_count = self.get_records_count()

        """Execute the console command"""
        create_state_in_console("California")

        """Get the updated number of records"""
        updated_count = self.get_records_count()

        """Validate the difference is +1"""
        self.assertEqual(updated_count - initial_count, 1)

    def get_records_count(self):
        """Query the database to get the number of records in the states table"""
        self.cursor.execute("SELECT COUNT(*) FROM states")
        return self.cursor.fetchone()[0]

if __name__ == '__main__':
    unittest.main()
