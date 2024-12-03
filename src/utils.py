from typing import List, Set
from spacy.tokens import Doc

def remove_stopwords(doc: Doc) -> List[str]:
    """Remove stopwords from a spaCy Doc."""
    return [token.text for token in doc if not token.is_stop]

def extract_ngrams(doc: Doc, n: int = 2) -> List[str]:
    """Extract n-grams using spaCy tokens."""
    tokens = [token.text.lower() for token in doc]
    if len(tokens) < n:
        return []
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]