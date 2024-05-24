# Processes text files in a folder and creates a noun-verb pairing table
# Code modified from: https://chatgpt.com/share/9bfa3e0d-c47c-49a9-8a7e-49f3a75f4a67 
# and https://chatgpt.com/share/96a30754-276d-4d5c-b3d3-205f128f8858
# Parsing process: 
# For each file, In each sentence:
#   find verbs that are of the types ("ROOT", "acl", "advcl", "ccomp", "xcomp")
#   For each verb:
#       1. Get the left subtree and the first ["NOUN", "PROPN", "PRON"]; add the noun 
#       as "Root Noun" and the left subtree as "Noun Phrase" of this verb
#       2. Get the right subtree. Add the verb found as "Root Verb" 
#       and the right sub tree as "Verb Phrase" of this verb
#       3. Omit if any of the 4 elements are missing
#       4. Write the "Root Noun", "Root Verb", "Noun Phrase" and "Verb Phrase" to a csv file
import spacy
import os
import csv
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")
import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def get_subtree_string(token):
    return ' '.join([t.text for t in token.subtree])

def get_noun_root(tokens):
    # Find the first noun in the tokens
    for token in tokens:
        if token.pos_ in ["NOUN", "PROPN", "PRON"]:
            return token.lemma_
    return ""

def get_root_and_subtrees(root):
    # Get the left subtree as a string
    left_subtree = [child for child in root.lefts]
    left_subtree_str = ' '.join([get_subtree_string(child) for child in left_subtree]) if left_subtree else ""
    
    # Get the right subtree as a string
    right_subtree = [child for child in root.rights]
    right_subtree_str = ' '.join([get_subtree_string(child) for child in right_subtree]) if right_subtree else ""
    
    root_noun = get_noun_root(left_subtree)

    return  left_subtree_str, root_noun, root.text + " " + right_subtree_str, root.lemma_

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
                np, rootn, vp, rootv = get_root_and_subtrees(token)
                if rootn == "" or rootv == "": continue
                line.append([source, sentence.text, rootn, rootv, np,vp])
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
            # Extract the file name without the extension
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            # Construct the URL
            arxiv_url = f"https://arxiv.org/pdf/{file_name}"
            list.extend(extract_verb_noun_pairs(arxiv_url, doc))
    return list

def save_to_csv(list, output_path):
    """
    Save the frequency of verb-noun phrase pairs to a CSV file with separate columns for verbs and noun phrases.
    """
    header = ["Source", "Sentence", "Root Noun", "Root Verb", "Noun Phrase","Verb Phrase"]
    with open(output_path, mode='w', encoding='utf-8', newline='\n') as file:
        writer = csv.writer(file, escapechar='\\', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)  # Write the header
        writer.writerows(list)   # Write the data
    
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
    input_folder = "./OpenAI_Research_Text/"  # Update this with the path to your text files
    output_csv = "verb_noun_pairs.csv"  # Update this with the desired output CSV path
    main(input_folder, output_csv)
