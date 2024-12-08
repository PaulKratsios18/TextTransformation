import sqlite3
import os
import unittest
from src.queue_processing import init_db, add_document_to_db  # Replace 'your_module' with the actual module name

class TestQueueDatabase(unittest.TestCase):
    DB_FILE = "test_doc_id_queue.db"

    def setUp(self):
        """
        Set up a temporary database file for testing.
        """
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)
        global DB_FILE
        DB_FILE = self.DB_FILE  # Redirect to test database
        init_db()
    """
    def tearDown(self):
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)
    """

    def test_init_db(self):
        """
        Test if the database initializes correctly.
        """
        self.assertTrue(os.path.exists(self.DB_FILE))
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents';")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table)

    def test_add_document_to_db(self):
        """
        Test adding a document to the database.
        """
        result = add_document_to_db("doc_123")
        self.assertTrue(result)

        # Verify the document exists in the database
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT document_id FROM documents WHERE document_id = ?", ("doc_123",))
        document = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(document)
        self.assertEqual(document[0], "doc_123")

    def test_add_duplicate_document(self):
        """
        Test adding a duplicate document ID.
        """
        add_document_to_db("doc_123")  # First insertion
        result = add_document_to_db("doc_123")  # Duplicate insertion
        self.assertFalse(result)

