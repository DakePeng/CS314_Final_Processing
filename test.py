import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

# Function to extract main verbs and their corresponding nouns
def extract_verbs_and_nouns(text):
    # Process the text using SpaCy
    doc = nlp(text)
    
    # Initialize lists to store verbs and corresponding nouns
    verbs = []
    nouns = []
    
    # Iterate over tokens in the document
    for token in doc:
        # Check if the token is a verb and if it's the main verb
        if token.pos_ == "VERB" and token.dep_ in ("ROOT", "conj"):
            # Add the verb to the list
            verbs.append(token.text)
            
            # Find the corresponding subject of the verb
            subject = None
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subject = child.text
                    break
            
            # If a subject is found, add it to the list of nouns
            if subject:
                nouns.append(subject)
            else:
                # If no subject is found, add an empty string to maintain alignment
                nouns.append("")
    
    # Return lists of verbs and corresponding nouns
    return verbs, nouns

# Function to read text from a file
def read_text_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
    return text

# Main function
def main():
    # Read text from file
    filename = "./test_subset/1602.07868.txt"  # Replace with the path to your text file
    text = read_text_from_file(filename)
    
    # Extract verbs and nouns
    verbs, nouns = extract_verbs_and_nouns(text)
    
    # Print verbs and corresponding nouns
    for verb, noun in zip(verbs, nouns):
        print(f"Verb: {verb}, Noun: {noun}")

if __name__ == "__main__":
    main()
