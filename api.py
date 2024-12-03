from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated queues and storage for demonstration purposes
new_document_queue = []
transformed_documents = {}
queries_transformed = {}

# Endpoint: newDocument()
@app.route('/newDocument', methods=['POST'])
def new_document():
    """
    Adds a JSON file containing a new document ID to the processing queue.
    Input: JSON with document_id.
    Output: Status message (void in the real implementation).
    """
    data = request.json
    document_id = data.get("document_id")
    if not document_id:
        return jsonify({"error": "document_id is required"}), 400
    
    new_document_queue.append({"id": document_id})
    return jsonify({"message": f"Document ID {document_id} added to processing queue"}), 200

# # Endpoint: addTransformedDocument()
# @app.route('/addTransformedDocument', methods=['POST'])
# def add_transformed_document():
#     """
#     Add transformed document to Document Data Store.
#     Input: JSON with transformed document data
#     Output: Success status
#     """
#     try:
#         transformed_document = request.json
#         if not transformed_document or 'id' not in transformed_document:
#             return jsonify({"error": "Invalid document format"}), 400

#         # TODO: Implement actual document storage logic
#         # Validate document structure
#         required_fields = ['id', 'tokens', 'named_entities', 'ngrams']
#         if not all(field in transformed_document for field in required_fields):
#             return jsonify({"error": "Missing required fields"}), 400

#         logger.info(f"Stored transformed document {transformed_document['id']}")
#         return jsonify({"success": True})

#     except Exception as e:
#         logger.error(f"Error storing transformed document: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# Endpoint: transformQuery()
@app.route('/transformQuery', methods=['POST'])
def transform_query():
    """
    Transform search query for the Querying team.
    Input: Query string
    Output: Transformed query in JSON format
    """
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({"error": "Missing query"}), 400

        # TODO: Implement actual query transformation logic
        transformed_query = {
            "original": query,
            "tokens": query.split(),
            "named_entities": []
        }
        
        logger.info(f"Transformed query: {query}")
        return jsonify(transformed_query)

    except Exception as e:
        logger.error(f"Error transforming query: {str(e)}")
        return jsonify({"error": str(e)}), 500

# # Endpoint: getRawDocuments()
# @app.route('/getRawDocuments', methods=['POST'])
# def get_raw_documents():
#     """
#     Retrieve raw documents from Document Data Store.
#     Input: JSON with document_id
#     Output: Raw document content
#     """
#     try:
#         document_id = request.json.get('document_id')
#         if not document_id:
#             return jsonify({"error": "Missing document_id"}), 400
            
#         # TODO: Implement actual document fetching logic
#         raw_document = {"id": document_id, "content": "This is a raw document."}
#         logger.info(f"Retrieved raw document {document_id}")
#         return jsonify(raw_document)
        
#     except Exception as e:
#         logger.error(f"Error retrieving document: {str(e)}")
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
