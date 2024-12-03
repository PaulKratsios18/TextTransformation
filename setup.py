import spacy

def setup_dependencies():
    # Download required NLTK data
    nltk_packages = [
        'punkt',
        'stopwords',
        'averaged_perceptron_tagger',
        'maxent_ne_chunker',
        'words'
    ]
    
    # Download spaCy model
    print("\nDownloading spaCy model...")
    try:
        spacy.cli.download("en_core_web_sm")
        print("✓ Successfully downloaded spaCy model")
    except Exception as e:
        print(f"✗ Error downloading spaCy model: {e}")

if __name__ == "__main__":
    setup_dependencies() 