import unittest
from src.processor import TextTransformer

class TestTextTransformer(unittest):
    def setUp(self):
        self.transformer = TextTransformer()
        
    def test_basic_processing(self):
        test_doc = {
            'doc_id': '123',
            'content': 'OpenAI is located in San Francisco.',
            'metadata': {'source': 'web'}
        }
        
        result = self.transformer.process_document(test_doc)
        
        self.assertEqual(result['doc_id'], '123')
        self.assertEqual(result['language'], 'en')
        self.assertIn('OpenAI', result['entities'].get('ORG', []))
        self.assertIn('San Francisco', result['entities'].get('GPE', []))
        
    def test_html_cleaning(self):
        test_doc = {
            'doc_id': '124',
            'content': '<p>Hello <b>World</b></p>',
            'type': 'html',
            'metadata': {}
        }
        
        result = self.transformer.process_document(test_doc)
        self.assertEqual(result['tokens'], ['Hello', 'World'])

if __name__ == '__main__':
    unittest.main() 