import spacy
from bs4 import BeautifulSoup
from langdetect import detect
from typing import Dict, List, Any
from .utils import remove_stopwords, extract_ngrams

class TextTransformer:
    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the TextTransformer with specified spaCy model."""
        self.nlp = spacy.load(model_name)
        
    def process_document(self, raw_document: Dict[str, Any]) -> Dict[str, Any]:
        """Process a raw document and return structured data."""
        doc_id = raw_document['doc_id']
        content = raw_document['content']
        
        # Clean HTML if present
        if raw_document.get('type') == 'html':
            content = self._clean_html(content)
            
        # Detect language
        lang = detect(content)
        
        # Process with spaCy
        doc = self.nlp(content)
        
        # Extract structured data
        processed_data = {
            'doc_id': doc_id,
            'language': lang,
            'tokens': [token.text for token in doc],
            'lemmas': [token.lemma_ for token in doc],
            'pos_tags': [(token.text, token.pos_) for token in doc],
            'entities': self._extract_entities(doc),
            'sentences': [str(sent) for sent in doc.sents],
            'ngrams': extract_ngrams(doc),
            'non_stop_words': remove_stopwords(doc),
            'metadata': raw_document.get('metadata', {})
        }
        
        return processed_data
    
    def _clean_html(self, html_content: str) -> str:
        """Remove HTML tags and extract clean text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def _extract_entities(self, doc) -> Dict[str, List[str]]:
        """Extract named entities from processed document."""
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities 

    # spaCy's pipeline components
    nlp = spacy.load("en_core_web_sm")
    print(nlp.pipe_names)  # ['tok2vec', 'tagger', 'parser', 'ner', ...]

    # spaCy's built-in features
    doc = nlp("OpenAI costs $20 billion")
    for ent in doc.ents:
        print(ent.text, ent.label_)  # Named Entity Recognition

    for token in doc:
        print(token.like_num)  # Number detection
        print(token.like_email)  # Email detection
        print(token.like_url)  # URL detection