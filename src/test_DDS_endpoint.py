from pymongo import MongoClient, UpdateOne
from processor import TextTransformer  # Import the TextTransformer class

# MongoDB URI
MONGO_URI = "mongodb://128.113.126.79:27017"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client.test
collection = db.RAW
transformed_collection = db.TRANSFORMED

# Ensure an index on the 'url' field
transformed_collection.create_index("url", unique=True)

def get_raw_documents(docID):
    """Retrieve a raw document from the MongoDB collection by document ID."""
    try:
        document = collection.find_one({"_id": docID})
        if document:
            print(f"Retrieved document: {document}")
            return document
        else:
            print(f"No document found with ID: {docID}")
            return None
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return None

def add_transformed_document(docID, transformed_content, url):
    """Insert or update a transformed document in the MongoDB collection."""
    try:
        transformed_document = {
            "url": url,
            "doc_id": docID,
            "text": transformed_content,
            "metadata": {"processed": True}
        }
        
        # Check if the document already exists
        existing_doc = transformed_collection.find_one({"doc_id": docID})
        
        if existing_doc:
            # Update the existing document
            print(f"Updating transformed document with ID: {docID}")
            result = transformed_collection.update_one(
                {"doc_id": docID},
                {"$set": transformed_document}
            )
            print(f"Updated transformed document with ID: {docID}")
        else:
            # Insert the new document
            result = transformed_collection.insert_one(transformed_document)
            print(f"Inserted transformed document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting or updating transformed document: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the transformer
    transformer = TextTransformer()

    # Example document ID
    doc_id = "wl94r5rsun319rxu5zcrl41s"

    # Get raw document
    raw_document = get_raw_documents(doc_id)
    
    # If a raw document is found, process it and add the transformed document
    if raw_document:
        # Process the document
        processed_result = transformer.process_document(raw_document)
        print("Processed result: ", processed_result)
        # Extract the URL from the raw document
        url = raw_document.get('url', 'http://default-url.com')  # Use a default if 'url' is not present
        
        # Add the processed document to the transformed collection
        add_transformed_document(doc_id, processed_result, url)