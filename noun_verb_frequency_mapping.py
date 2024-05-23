# code from https://chatgpt.com/share/795d150d-7da9-4967-b409-32f6ee5d488f

import spacy
import os
import csv
from collections import Counter

# Load the English language model in SpaCy
nlp = spacy.load("en_core_web_sm")

def extract_verbs_and_noun_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    doc = nlp(text)
    verb_noun_pairs = []

    # Extract verbs and corresponding noun phrases
    for token in doc:
        if token.pos_ == 'VERB':
            noun_phrases = []
            for chunk in token.children:
                if chunk.dep_ in ('nsubj', 'dobj', 'attr') and chunk.head.text == 'model':
                    noun_phrase = ' '.join([t.text for t in chunk.subtree])
                    noun_phrases.append(noun_phrase)
            if noun_phrases:
                combined_noun_phrase = ', '.join(noun_phrases)
                verb_noun_pairs.append((token.lemma_, combined_noun_phrase))

    return verb_noun_pairs


# Function to process all text files in a directory
def process_files_in_directory(directory):
    all_pairs = []

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            pairs = extract_verbs_and_noun_phrases(file_path)
            all_pairs.extend(pairs)

    return all_pairs

# Function to write verb-noun pairs and their frequencies to a CSV file
def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Verb', 'Noun Phrase', 'Frequency'])
        for row in data:
            csv_writer.writerow(row)

# Directory containing the text files
directory_path = './test_subset/'

# Process all text files in the directory
pairs = process_files_in_directory(directory_path)

# Count the frequency of each verb-noun pair
pair_counter = Counter(pairs)

# Write the data to a CSV file
output_file = 'verb_noun_pairs.csv'
write_to_csv(pair_counter.items(), output_file)

print("CSV file created successfully.")
