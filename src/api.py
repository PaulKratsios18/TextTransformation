from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
import logging
import json
import os
from pymongo import MongoClient
from processor import TextTransformer

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB URI
MONGO_URI = "mongodb://128.113.126.79:27017"
client = MongoClient(MONGO_URI)
db = client.test
transformed_collection = db.TRANSFORMED

# Simulated queues and storage for demonstration purposes
new_document_queue = []

# Load queue from file if it exists
if os.path.exists('queue.json'):
    with open('queue.json', 'r') as f:
        new_document_queue = json.load(f)

def save_queue():
    """Save the current queue to a file."""
    with open('queue.json', 'w') as f:
        json.dump(new_document_queue, f)
    logger.info(f"Queue saved with {len(new_document_queue)} documents.")

def process_and_add_transformed_document(document_id):
    """Process a document and store the transformed result."""
    logger.info(f"Processing document ID: {document_id}")
    
    # Retrieve the raw document from the RAW collection
    raw_document = db.RAW.find_one({"_id": document_id})
    if not raw_document:
        logger.error(f"No document found with ID: {document_id}")
        return
    
    logger.info(f"Retrieved raw document: {raw_document}")
    
    # Initialize the transformer
    transformer = TextTransformer()
    
    # Process the document
    processed_result = transformer.process_document(raw_document)
    logger.info(f"Processed document result: {processed_result}")
    
    # Store the transformed document
    transformed_document = {
        "url": raw_document.get('url'),
        "doc_id": document_id,
        "text": processed_result,
        "metadata": {"processed": True}
    }
    
    # Insert or update the document in the TRANSFORMED collection
    existing_doc = transformed_collection.find_one({"url": raw_document.get('url')})
    if existing_doc:
        transformed_collection.update_one({"url": raw_document.get('url')}, {"$set": transformed_document})
        logger.info(f"Updated transformed document with URL: {raw_document.get('url')}")
    else:
        transformed_collection.insert_one(transformed_document)
        logger.info(f"Inserted transformed document with ID: {document_id}")

# Endpoint: newDocument()
@app.route('/newDocument', methods=['POST'])
def new_document():
    data = request.json
    document_id = data.get("document_id")
    if not document_id:
        logger.warning("Received request without document_id")
        return jsonify({"error": "document_id is required"}), 400
    
    new_document_queue.append({"id": document_id})
    logger.info(f"Added document ID {document_id} to processing queue")
    save_queue()
    return jsonify({"message": f"Document ID {document_id} added to processing queue"}), 200

@app.route('/processQueue', methods=['POST'])
def process_queue():
    """Process all documents in the queue."""
    for document in new_document_queue:
        process_and_add_transformed_document(document['id'])
    return jsonify({"message": "All documents processed"}), 200

@app.route('/transformQuery', methods=['POST'])
def transform_query():
    """
    Transform search query for the Querying team.
    Input: JSON with "query".
    Output: Transformed query in JSON format.
    """
    try:
        data = request.json
        query = data.get('query')
        if not query:
            return jsonify({"error": "Missing query"}), 400
        transformed_query = text_transformer.process_query(query)
        logger.info(f"Query: {query}")
        logger.info(f"Transformed query: {transformed_query}")
        return jsonify(transformed_query), 200

    except Exception as e:
        logger.error(f"Error transforming query: {str(e)}")
        return jsonify({"error": str(e)}), 500

text_transformer = TextTransformer()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
