import logging

from flask import Flask, request, jsonify
from flask_cors import CORS

from typing import Dict, Any

from ..processor import TextTransformer
from ..queue_processing import QueueProcessor

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Initialize TextTransformer
text_transformer = TextTransformer()
queue_processor = QueueProcessor()


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Endpoint: newDocument()
@app.route('/newDocument', methods=['POST'])
def new_document():
    """
    Adds a JSON file containing a new document ID to the processing queue.
    Input: JSON with document_id.
    Output: Status message.
    """
    data = request.json
    document_id = data.get("document_id")
    if not document_id:
        logger.warning("Received request without document_id")
        return jsonify({"error": "document_id is required"}), 400

    if queue_processor.add_document_to_db(document_id):
        logger.info(f"Added document ID {document_id} to the queue")
        return jsonify({"message": f"Document ID {document_id} added to the queue"}), 200
    else:
        return jsonify({"error": f"Document ID {document_id} already exists in queue. Waiting to be processed."}), 400
    

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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
