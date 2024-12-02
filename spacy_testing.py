import spacy
from collections import Counter
import json
import sys

nlp = spacy.load("en_core_web_sm")

def get_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return Counter(ngrams)

def querying_transformation(query):
    query = query.lower()
    doc = nlp(query)
    filtered_tokens = [
        token.lemma_ for token in doc if not token.is_punct and not token.is_space and not token.is_stop
    ]
    result = {
        "total_length": len([token for token in doc if not token.is_space and not token.is_punct]),
        "tokens": [],
        "bigrams": [],
        "trigrams": [],
        "named_entities": [],
        "parts_of_speech": []
    }
    token_freq = Counter(filtered_tokens)
    sorted_tokens = sorted(
        token_freq.items(),
        key=lambda x: (-x[1], x[0])  # Sort by frequency descending, then alphabetically
    )
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
    bigram_freq = get_ngrams(filtered_tokens, 2)
    sorted_bigrams = sorted(
        bigram_freq.items(),
        key=lambda x: (-x[1], x[0])  # Sort by frequency descending, then alphabetically
    )
    result["bigrams"] = [
        {"bigram": list(bigram), "frequency": freq}
        for bigram, freq in sorted_bigrams
    ]
    trigram_freq = get_ngrams(filtered_tokens, 3)
    sorted_trigrams = sorted(
        trigram_freq.items(),
        key=lambda x: (-x[1], x[0])  # Sort by frequency descending, then alphabetically
    )
    result["trigrams"] = [
        {"trigram": list(trigram), "frequency": freq}
        for trigram, freq in sorted_trigrams
    ]
    for ent in doc.ents:
        result["named_entities"].append({
            "entity": ent.text,
            "type": ent.label_,
            "position": [ent.start_char, ent.end_char]
        })
    for token in doc:
        if not token.is_punct and not token.is_space and not token.is_stop:
            result["parts_of_speech"].append({
                "token": token.text,
                "pos_tag": token.pos_,
                "position": token.idx
            })
    return result

if len(sys.argv) != 2:
    print("Please provide the input file as a command-line argument.")
    sys.exit(1)

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

output = querying_transformation(query)
output_file = "output.json"
with open(output_file, "w") as file:
    json.dump(output, file, indent=4)

print(f"JSON output has been saved to {output_file}")