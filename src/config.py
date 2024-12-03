# spaCy model configuration
DEFAULT_MODEL = "en_core_web_sm"

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de']

# N-gram configuration
NGRAM_SIZES = [2, 3]  # bi-grams and tri-grams

# Entity types to extract
ENTITY_TYPES = [
    'PERSON',
    'ORG',
    'GPE',
    'DATE',
    'TIME',
    'MONEY',
    'PRODUCT'
] 