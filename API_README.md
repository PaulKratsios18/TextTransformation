### **API Functionalities**

1. **`newDocument()`**
   - **Input**: JSON with `document_id`.
   - **Output**: Acknowledgment message (`void` in real implementation).
   - **Side Effect**: Adds the document ID to the processing queue.

2. **`addTransformedDocument()`**
   - **Input**: JSON with `id` (document ID) and `transformed_text`.
   - **Output**: Acknowledgment message (`void` in real implementation).
   - **Side Effect**: Stores the transformed document in the system.

3. **`transformQuery()`**
   - **Input**: JSON with a `query` string.
   - **Output**: JSON containing the transformed query.
   - **Side Effect**: Stores the transformed query for potential debugging or analytics.

---

### **Sample Requests**

#### **1. newDocument()**
- **Request**:
  ```bash
  curl -X POST http://<vm_ip>:5000/newDocument \
  -H "Content-Type: application/json" \
  -d '{"document_id": "12345"}'
  ```
- **Response**:
  ```json
  {
      "message": "Document ID 12345 added to processing queue"
  }
  ```

#### **2. addTransformedDocument()**
- **Request**:
  ```bash
  curl -X POST http://<vm_ip>:5000/addTransformedDocument \
  -H "Content-Type: application/json" \
  -d '{"id": "12345", "transformed_text": "This is transformed content"}'
  ```
- **Response**:
  ```json
  {
      "message": "Transformed document for ID 12345 added successfully"
  }
  ```

#### **3. transformQuery()**
- **Request**:
  ```bash
  curl -X POST http://<vm_ip>:5000/transformQuery \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RPI?"}'
  ```
- **Response**:
  ```json
  {
      "original_query": "What is RPI?",
      "transformed_query": ["what", "is", "rpi?"]
  }
  ```