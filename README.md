# Text Processing and Document Transformation Pipeline

## Overview

This project represents the Text Transformation component of a larger Search Engine system, developed by our team under my leadership as Team Lead. The pipeline processes raw text documents through sophisticated NLP operations before storing results in MongoDB. Working alongside other teams, we implemented core text processing features including tokenization, lemmatization, part-of-speech tagging, named entity recognition, and n-gram generation - providing the foundation for the search engine's text analysis capabilities.

## Features
- Document processing and transformation
- Language detection
- Tokenization and lemmatization
- Part-of-speech (POS) tagging
- Named Entity Recognition (NER)
- N-gram generation (bigrams, trigrams)
- MongoDB integration for document storage
- Unique URL indexing
- Error handling and logging

## Prerequisites
- Python 3.x
- MongoDB instance
- Required Python packages (see [Requirements](#requirements))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/text-processing-pipeline.git
cd text-processing-pipeline
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up dependencies by running the setup script:
```bash
python src/setup.py
```

This will download necessary NLTK packages and spaCy models as shown in:

```3:20:src/setup.py
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
```


## Configuration

### MongoDB Setup
The system requires a MongoDB instance. Update the MongoDB connection URI in:

```4:5:src/test_DDS_endpoint.py
# MongoDB URI
MONGO_URI = "mongodb://128.113.126.79:27017"
```


## Usage

### Basic Usage
Run the main script to process a sample document:
```bash
python src/main.py
```

The output will include processed information such as:
- Document ID
- Detected language
- Tokens and lemmas
- POS tags
- Named entities
- Sentences
- N-grams
- Metadata

### Processing Documents from MongoDB
To process documents from MongoDB:
```bash
python src/test_DDS_endpoint.py
```

## Data Structure
The system processes documents and generates structured output as shown in the example JSON:

```1:101:src/test.json
{
    "url": "https://www.google.com",
    "doc_id": "doc123",
    "total_length": 6,
    "tokens": [
        {
            "frequency": 1,
            "lemma": "capital",
            "position": 10,
            "token": "capital"
        },
        {
            "frequency": 1,
            "lemma": "france",
            "position": 21,
            "token": "france"
        },
        {
            "frequency": 1,
            "lemma": "s",
            "position": 4,
            "token": "s"
        }
    ],
    "bigrams": [
        {
            "bigram": [
                "capital",
                "france"
            ],
            "frequency": 1
        },
        {
            "bigram": [
                "s",
                "capital"
            ],
            "frequency": 1
        }
    ],
    "trigrams": [
        {
            "frequency": 1,
            "trigram": [
                "s",
                "capital",
                "france"
            ]
        }
    ],
    "named_entities": [
        {
            "entity": "france",
            "position": [
                21,
                27
            ],
            "type": "GPE"
        },
        {
            "entity": "france",
            "position": [
                21,
                27
            ],
            "type": "GPE"
        }
    ],
    "parts_of_speech": [
        {
            "pos_tag": "VERB",
            "position": 4,
            "token": "s"
        },
        {
            "pos_tag": "NOUN",
            "position": 10,
            "token": "capital"
        },
        {
            "pos_tag": "PROPN",
            "position": 21,
            "token": "france"
        },
        {
            "pos_tag": "VERB",
            "position": 4,
            "token": "s"
        },
        {
            "pos_tag": "NOUN",
            "position": 10,
            "token": "capital"
        },
        {
            "pos_tag": "PROPN",
            "position": 21,
            "token": "france"
        }
    ]
}
```


### Output Fields
- `url`: Document source URL
- `doc_id`: Unique document identifier
- `tokens`: List of processed tokens with frequency and position
- `bigrams`: Word pairs with frequency
- `trigrams`: Word triplets with frequency
- `named_entities`: Identified named entities with type and position
- `parts_of_speech`: POS tags for each token

## Requirements
Key dependencies include:

```1:4:src/requirements.txt
beautifulsoup4>=4.12.0
langdetect>=1.0.9
nltk>=3.8.1 
spacy>=3.8.2
```


## Error Handling
The system includes comprehensive error handling for:
- MongoDB operations
- Document processing
- Model loading
- Data transformation