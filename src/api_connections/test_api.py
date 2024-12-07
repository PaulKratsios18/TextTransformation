import unittest
import requests
import json
from typing import Dict, Any
import logging

class TestTextTransformationAPI(unittest.TestCase):
    def setUp(self):
        """Set up test case - define the base URL"""
        self.base_url = "http://128.113.126.77:5001"
        
    def test_new_document(self):
        """Test adding a new document to the queue"""
        url = f"{self.base_url}/newDocument"
        data = {"document_id": "doc123"}
        response = requests.post(url, json=data, timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertIn("added to processing queue", response.json()["message"])

    # def test_add_transformed_document(self):
    #     """Test adding a transformed document"""
    #     url = f"{self.base_url}/addTransformedDocument"
    #     data = {
    #         "id": "doc123",
    #         "tokens": ["hello", "world"],
    #         "named_entities": ["world"],
    #         "ngrams": ["hello world"]
    #     }
    #     response = requests.post(url, json=data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.json()["success"])

    def test_transform_query(self):
        """Test query transformation"""
        url = f"{self.base_url}/transformQuery"
        data = {"query": "Hello World!"}
        response = requests.post(url, json=data, timeout=5)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("original", result)
        self.assertIn("tokens", result)
        self.assertIn("named_entities", result)

    # def test_get_raw_documents(self):
    #     """Test retrieving raw documents"""
    #     url = f"{self.base_url}/getRawDocuments"
    #     data = {"document_id": "doc123"}
    #     response = requests.post(url, json=data)
    #     self.assertEqual(response.status_code, 200)
    #     result = response.json()
    #     self.assertIn("id", result)
    #     self.assertIn("content", result)

    # def test_error_handling(self):
    #     """Test error handling for missing required fields"""
    #     # Test missing document_id in newDocument
    #     url = f"{self.base_url}/newDocument"
    #     response = requests.post(url, json={})
    #     self.assertEqual(response.status_code, 400)
        
    #     # # Test missing required fields in addTransformedDocument
    #     # url = f"{self.base_url}/addTransformedDocument"
    #     # data = {"id": "doc123"}  # Missing required fields
    #     # response = requests.post(url, json=data)
    #     # self.assertEqual(response.status_code, 400)
        
    #     # Test missing query in transformQuery
    #     url = f"{self.base_url}/transformQuery"
    #     response = requests.post(url, json={})
    #     self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main() 