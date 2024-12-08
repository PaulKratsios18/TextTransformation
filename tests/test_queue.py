import sqlite3
import os
import unittest
from src.queue_processing import QueueProcessor

class TestQueueDatabase(unittest.TestCase):
    DB_FILE = "test_doc_id_queue.db"

    def setUp(self):
        """
        Set up a temporary QueueProcessor instance with a test database file.
        """
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)
        self.queue_processor = QueueProcessor(db_file=self.DB_FILE)
        self.queue_processor.init_db()
    
    def tearDown(self):
        if os.path.exists(self.DB_FILE):
            os.remove(self.DB_FILE)
    
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
        result = self.queue_processor.add_document_to_db("doc_123")
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
        self.queue_processor.add_document_to_db("doc_123")  # First insertion
        result = self.queue_processor.add_document_to_db("doc_123")  # Duplicate insertion
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()