import spacy
from collections import Counter
import json
import sys

# Load the English NLP model from spaCy
nlp = spacy.load("en_core_web_sm")

def get_ngrams(tokens, n):
    """
    Generate n-grams from a list of tokens and count their frequencies.
    """
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return Counter(ngrams)

def querying_transformation(query):
    """
    Process the input query and return a JSON-like result with token frequencies,
    bigrams, trigrams, named entities, and parts of speech.
    """
    query = query.lower()  # Convert query to lowercase for uniform processing
    doc = nlp(query)  # Tokenize and process the text with spaCy

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
        "named_entities": [],
        "parts_of_speech": []
    }

    # Count and sort tokens by frequency and alphabetically
    token_freq = Counter(filtered_tokens)
    sorted_tokens = sorted(
        token_freq.items(),
        key=lambda x: (-x[1], x[0])  # Sort by frequency (descending), then alphabetically
    )

    # Add each token to the result, repeated for its occurrences with respective positions
    for token, freq in sorted_tokens:
        positions = [doc_token.idx for doc_token in doc if doc_token.lemma_ == token and not doc_token.is_punct and not doc_token.is_space and not doc_token.is_stop]
        for pos in positions:
            result["tokens"].append({
                "token": token,
                "lemma": token,
                "frequency": freq,
                "position": pos
            })

    # Generate and sort bigrams
    bigram_freq = get_ngrams(filtered_tokens, 2)
    sorted_bigrams = sorted(
        bigram_freq.items(),
        key=lambda x: (-x[1], x[0])
    )
    result["bigrams"] = [
        {"bigram": list(bigram), "frequency": freq}
        for bigram, freq in sorted_bigrams
    ]

    # Generate and sort trigrams
    trigram_freq = get_ngrams(filtered_tokens, 3)
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

# Ensure the correct number of command-line arguments
if len(sys.argv) != 2:
    print("Please provide the input file as a command-line argument.")
    sys.exit(1)

# Read the input file
input_file = sys.argv[1]
try:
    with open(input_file, "r") as file:
        query = file.read().strip()
except FileNotFoundError:
    print(f"Error: The file '{input_file}' does not exist.")
    sys.exit(1)
except IOError:
    print(f"Error: Unable to read the file '{input_file}'.")
    sys.exit(1)

# Process the query and save the output to a JSON file
output = querying_transformation(query)
output_file = "output.json"
with open(output_file, "w") as file:
    json.dump(output, file, indent=4)

print(f"JSON output has been saved to {output_file}")