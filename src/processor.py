from collections import Counter
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import spacy
from bs4 import BeautifulSoup
from langdetect import detect
from typing import Dict, List, Any

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
            #'ngrams': extract_ngrams(doc),
            #'non_stop_words': remove_stopwords(doc),
            'metadata': raw_document.get('metadata', {})
        }
        
        return processed_data
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process the input query and return a JSON-like result with token frequencies,
        bigrams, trigrams, named entities, and parts of speech.
        """
        query = query.lower()
        doc = self.nlp(query)  # Tokenize and process the text with spaCy

        # Filter tokens to exclude punctuation, spaces, and stop words, using lemmas
        filtered_tokens = [
            token.lemma_ for token in doc if not token.is_punct and not token.is_space and not token.is_stop
        ]

        # Initialize result dictionary
        result = {
            "total_length": len([token for token in doc if not token.is_space and not token.is_punct]),  # Word count excluding punctuation and spaces
            "tokens": [],
            "bigrams": [],
            "trigrams": [],
            "named_entities": self._extract_entities(doc),  
            "parts_of_speech": self._extract_pos(doc)  
        }

        # Count and sort tokens by frequency and alphabetically
        token_freq = Counter(filtered_tokens)
        sorted_tokens = sorted(
            token_freq.items(),
            key=lambda x: (-x[1], x[0])  # Sort by frequency (descending), then alphabetically
        )

        # Add each token to the result, repeated for its occurrences with respective positions
        for token, freq in sorted_tokens:
            # Find all positions where this lemma occurs
            positions = [doc_token.idx for doc_token in doc if doc_token.lemma_ == token and not doc_token.is_punct and not doc_token.is_space and not doc_token.is_stop]
            # Add the token multiple times with each position
            for pos in positions:
                result["tokens"].append({
                    "token": token,
                    "lemma": token,
                    "frequency": freq,
                    "position": pos
                })

        # Generate and sort bigrams
        bigram_freq = self._extract_ngrams(filtered_tokens, 2)
        sorted_bigrams = sorted(
            bigram_freq.items(),
            key=lambda x: (-x[1], x[0])
        )
        result["bigrams"] = [
            {"bigram": list(bigram), "frequency": freq}
            for bigram, freq in sorted_bigrams
        ]

        # Generate and sort trigrams
        trigram_freq = self._extract_ngrams(filtered_tokens, 3)
        sorted_trigrams = sorted(
            trigram_freq.items(),
            key=lambda x: (-x[1], x[0])
        )
        result["trigrams"] = [
            {"trigram": list(trigram), "frequency": freq}
            for trigram, freq in sorted_trigrams
        ]

        # Extract named entities with their character positions
        for ent in doc.ents:
            result["named_entities"].append({
                "entity": ent.text,
                "type": ent.label_,
                "position": [ent.start_char, ent.end_char]
            })

        # Add parts of speech for valid tokens
        for token in doc:
            if not token.is_punct and not token.is_space and not token.is_stop:
                result["parts_of_speech"].append({
                    "token": token.text,
                    "pos_tag": token.pos_,
                    "position": token.idx
                })

        return result
    def _clean_html(self, html_content: str) -> str:
        """Remove HTML tags and extract clean text."""
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def _extract_ngrams(self,tokens, n) -> Counter:
        """
        Generate n-grams from a list of tokens and count their frequencies.
        """
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return Counter(ngrams)
    
    def _extract_entities(self, doc) -> List[Dict[str, Any]]:
            """
            Extract named entities from a spaCy document with their character positions.
            """
            entities = []
            for ent in doc.ents:
                entities.append({
                    "entity": ent.text,
                    "type": ent.label_,
                    "position": [ent.start_char, ent.end_char]
                })
            return entities

    def _extract_pos(self, doc) -> List[Dict[str, Any]]:
        """
        Extract parts of speech for valid tokens from a spaCy document.
        """
        pos_tags = []
        for token in doc:
            if not token.is_punct and not token.is_space and not token.is_stop:
                pos_tags.append({
                    "token": token.text,
                    "pos_tag": token.pos_,
                    "position": token.idx
                })
        return pos_tags
    
    