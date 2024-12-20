import sys
import os
import spacy
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.processor import TextTransformer

class TestTextTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TextTransformer()
        
    def test_query_processing(self):
        test_query = "What is the capital of France?"
        result = self.transformer.process_query(test_query)
        print ("Query result:", result)
    def test_html_cleaning(self):
        test_doc = {
            'doc_id': '124',
            'content': '<p>Hello <b>World</b></p>',
            'type': 'html',
            'metadata': {}
        }
        
        result = self.transformer.process_document(test_doc)
        self.assertEqual(result['tokens'], ['Hello', 'World'])

    def test_book_1984_processing(self):
        with open('book-1984.txt', 'r') as file:
            content = file.read()
        
        test_doc = {
            'doc_id': '1984',
            'content': content,
            'metadata': {'source': 'book'}
        }
        
        result = self.transformer.process_document(test_doc)
        
        # Example assertions (adjust based on expected outcomes)
        self.assertEqual(result['doc_id'], '1984')
        self.assertEqual(result['language'], 'en')
        # print(content)
        # Add more assertions based on expected entities, tokens, etc.

if __name__ == "__main__":
    unittest.main() 

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Test document
doc = nlp("OpenAI is located in San Francisco.")

# # Print recognized entities
# for ent in doc.ents:
#     print(ent.text, ent.label_)