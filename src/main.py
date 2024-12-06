from src.processor import TextTransformer

def main():
    # Initialize the transformer
    transformer = TextTransformer()
    
    # Example document
    test_doc = {
        'doc_id': '123',
        'content': 'OpenAI is developing advanced AI models in San Francisco. ' 
                  'The company was founded by Sam Altman and others in 2015.',
        'metadata': {
            'source': 'web',
            'timestamp': '2024-03-20'
        }
    }
    
    # Process the document
    result = transformer.process_document(test_doc)
    
    # Print results in a readable format
    print("\n=== Processed Document Results ===")
    print(f"Document ID: {result['doc_id']}")
    print(f"Language: {result['language']}")
    print("\nTokens:", result['tokens'][:10], "...")
    print("\nLemmas:", result['lemmas'][:10], "...")
    print("\nPOS Tags:", result['pos_tags'][:5], "...")
    print("\nNamed Entities:", result['entities'])
    print("\nSentences:", result['sentences'])
    print("\nN-grams (first 5):", result['ngrams'][:5])
    print("\nMetadata:", result['metadata'])

if __name__ == "__main__":
    main() 