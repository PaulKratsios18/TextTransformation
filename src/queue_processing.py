import sqlite3
import os
import logging
from pymongo import MongoClient
from .processor import TextTransformer
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QueueProcessor:
    def __init__(self, db_file="doc_id_queue.db", mongo_uri="mongodb://128.113.126.79:27017"):
        self.db_file = db_file
        self.mongo_uri = mongo_uri
        self.client = None  # MongoClient is initialized lazily
        self.db = None
        self.collection = None
        self.transformed_collection = None
        self.text_transformer = TextTransformer()

        if not os.path.exists(self.db_file):
            logging.info(f"Database file {self.db_file} not found. Initializing...")
            self._init_db()

    def _init_db(self):
        """
        Initializes the SQLite database by creating the necessary tables if they don't exist.
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database initialized.")

    def _initialize_mongo(self):
        """Ensure MongoDB client and collections are initialized."""
        if not self.client:
            self.client = MongoClient(self.mongo_uri)
        try:
            self.client.admin.command('ping')  # Test the connection
            self.db = self.client.test
            self.collection = self.db.RAW
            self.transformed_collection = self.db.TRANSFORMED
            self.transformed_collection.create_index("url", unique=True)
        except Exception as e:
            logging.error(f"MongoDB connection failed: {e}")
            raise

    def _close_mongo(self):
        """Close the MongoDB client."""
        if self.client:
            self.client.close()
            self.client = None

    def add_document_to_db(self, document_id):
        """
        Adds a document ID to the SQLite database.
        """
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO documents (document_id) VALUES (?)", (document_id,))
            conn.commit()
            logging.info(f"Document ID {document_id} added to the database.")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"Document ID {document_id} already exists in the database.")
            return False
        except sqlite3.Error as e:
            logging.error(f"SQLite error occurred: {e}")
            return False
        finally:
            conn.close()

    def _get_raw_documents(self, docID):
        """Retrieve a raw document from the MongoDB collection by document ID."""
        try:
            document = self.collection.find_one({"_id": docID})
            if document:
                logging.info(f"Retrieved document: {document}")
                return document
            else:
                logging.warning(f"No document found with ID: {docID}")
                return None
        except Exception as e:
            logging.error(f"Error retrieving document with ID {docID}: {e}")
            return None

    def _add_transformed_document(self, docID, transformed_document):
        """Insert or update a transformed document in the MongoDB collection."""
        try:
            existing_doc = self.transformed_collection.find_one({"doc_id": docID})

            if existing_doc:
                self.transformed_collection.update_one(
                    {"doc_id": docID},
                    {"$set": transformed_document}
                )
                logging.info(f"Updated transformed document with ID: {docID}")
            else:
                result = self.transformed_collection.insert_one(transformed_document)
                logging.info(f"Inserted transformed document with ID: {result.inserted_id}")
        except Exception as e:
            logging.error(f"Error inserting or updating transformed document: {e}")

    def run_queue(self):
        """
        Process the entire document queue stored in the SQLite database.
        Attempts to retrieve each document from MongoDB and process it.
        """
        if not os.path.exists(self.db_file):
            logging.error("Database file not found. Ensure the queue is initialized.")
            return

        self._initialize_mongo()
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        try:
            # Fetch all document IDs from the database
            cursor.execute("SELECT document_id FROM documents")
            rows = cursor.fetchall()

            if not rows:
                logging.info("No documents in the queue to process.")

            for row in rows:
                document_id = row[0]
                logging.info(f"Processing document ID: {document_id}")

                # Attempt to retrieve the document from MongoDB
                document = self._get_raw_documents(document_id)
                if document:
                    try:
                        transformed_content, metadata = self.text_transformer.process_document(document)
                        transformed_document = {
                            "url": document.get("url", ""),
                            "doc_id": document_id,
                            "text": transformed_content,
                            "metadata": metadata
                        }
                        self._add_transformed_document(document_id, transformed_document)

                        # Delete the document ID from the SQLite queue
                        cursor.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
                        conn.commit()

                        logging.info(f"Successfully processed and removed document ID: {document_id} from queue")
                    except Exception as e:
                        logging.error(f"Error processing document ID {document_id}: {e}")
                else:
                    logging.warning(f"Failed to process document ID: {document_id}")

        except Exception as e:
            logging.error(f"Error while processing the queue: {e}")

        finally:
            conn.close()
            self._close_mongo()

# Example usage:
"""
if __name__ == "__main__":
    QueueProcessor = QueueProcessor()
    QueueProcessor.add_document_to_db("doc_123")
"""