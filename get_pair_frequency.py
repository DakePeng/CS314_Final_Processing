import spacy
import os
import pandas as pd
from collections import Counter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_verb_noun_pairs(source, doc):
    """
    Extract major verbs and their corresponding noun phrases from a spaCy doc.
    Returns a list of (verb, noun phrase) pairs.
    """
    line = []
    for sentence in doc.sents:
        sent_doc = nlp(sentence.text)
        for token in sent_doc:
            if token.pos_ == "VERB" and token.dep_ in ("ROOT", "acl", "advcl", "ccomp", "xcomp"):
                verb = token.lemma_
                for np in sent_doc.noun_chunks:
                    if token in np.root.head.ancestors or token == np.root.head:
                        line.append((sentence.text, verb, np.text, np.root.lemma_))
    return line

def process_files(file_list):
    """
    Process a list of files to extract verb-noun phrase pairs and count their frequencies.
    """
    list = []
    for file_path in file_list:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            doc = nlp(text)
            list.extend(extract_verb_noun_pairs(doc))

def save_to_csv(pair_counts, output_path):
    """
    Save the frequency of verb-noun phrase pairs to a CSV file with separate columns for verbs and noun phrases.
    """
    data = [{"Sentence": sentence, "Verb": verb, "Noun Phrase": noun_phrase, "Root Noun": root_noun, "Frequency": freq} 
            for (sentence, verb, noun_phrase, root_noun), freq in pair_counts.items()]
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    
def main(input_folder, output_csv):
    """
    Main function to process text files in a folder and save the results to a CSV file.
    """
    # List all text files in the input folder
    file_list = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.txt')]

    # Process files to get verb-noun phrase pairs and their frequencies
    pair_counts = process_files(file_list)

    # Save the results to a CSV file
    save_to_csv(pair_counts, output_csv)

if __name__ == "__main__":
    input_folder = "./test_subset/"  # Update this with the path to your text files
    output_csv = "verb_noun_pairs_frequency.csv"  # Update this with the desired output CSV path
    main(input_folder, output_csv)
