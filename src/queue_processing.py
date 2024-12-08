import sqlite3
import os
import logging
from pymongo import MongoClient
from .processor import TextTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# SQLite database file
DB_FILE = "doc_id_queue.db"

# MongoDB URI
MONGO_URI = "mongodb://128.113.126.79:27017"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collections
db = client.test
collection = db.RAW
transformed_collection = db.TRANSFORMED

# Ensure an index on the 'url' field
transformed_collection.create_index("url", unique=True)

# Initialize TextTransformer
text_transformer = TextTransformer()

def init_db():
    """
    Initializes the SQLite database by creating the necessary tables if they don't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

def add_document_to_db(document_id):
    """
    Adds a document ID to the SQLite database.
    Automatically initializes the database if it doesn't exist.
    """
    # Check if the database file exists
    if not os.path.exists(DB_FILE):
        logger.info("Database file not found. Initializing...")
        init_db()
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO documents (document_id) VALUES (?)", (document_id,))
        conn.commit()
        logger.info(f"Document ID {document_id} added to the database.")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Document ID {document_id} already exists in the database.")
        return False
    finally:
        conn.close()

def get_raw_documents(docID):
    """Retrieve a raw document from the MongoDB collection by document ID."""
    try:
        document = collection.find_one({"_id": docID})
        if document:
            logger.info(f"Retrieved document: {document}")
            return document
        else:
            logger.warning(f"No document found with ID: {docID}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving document with ID {docID}: {e}")
        return None

def add_transformed_document(docID, transformed_document):
    """Insert or update a transformed document in the MongoDB collection."""
    try:
        # Check if the document already exists
        existing_doc = transformed_collection.find_one({"doc_id": docID})

        if existing_doc:
            result = transformed_collection.update_one(
                {"doc_id": docID},
                {"$set": transformed_document}
            )
            logger.info(f"Updated transformed document with ID: {docID}")
        else:
            result = transformed_collection.insert_one(transformed_document)
            logger.info(f"Inserted transformed document with ID: {result.inserted_id}")
    except Exception as e:
        logger.error(f"Error inserting or updating transformed document: {e}")

def run_queue():
    """
    Process the entire document queue stored in the SQLite database.
    Attempts to retrieve each document from MongoDB and process it.
    """
    if not os.path.exists(DB_FILE):
        logger.error("Database file not found. Ensure the queue is initialized.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        # Fetch all document IDs from the database
        cursor.execute("SELECT document_id FROM documents")
        rows = cursor.fetchall()

        for row in rows:
            document_id = row[0]
            logger.info(f"Processing document ID: {document_id}")

            # Attempt to retrieve the document from MongoDB
            document = get_raw_documents(document_id)
            if document:
                try:
                    transformed_content, url = text_transformer.process_document(document)
                    add_transformed_document(document_id, transformed_content)

                    # Delete the document ID from the SQLite queue
                    cursor.execute("DELETE FROM documents WHERE document_id = ?", (document_id,))
                    conn.commit()

                    logger.info(f"Successfully processed and removed document ID: {document_id} from queue")
                except Exception as e:
                    logger.error(f"Error processing document ID {document_id}: {e}")
            else:
                logger.warning(f"Failed to process document ID: {document_id}")

    except Exception as e:
        logger.error(f"Error while processing the queue: {e}")

    finally:
        conn.close()