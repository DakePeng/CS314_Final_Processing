import spacy

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Read the text file
with open("1602.07868.txt", "r") as file:
    text = file.read()

# Process the text using spaCy
doc = nlp(text)

# Iterate through each sentence
for sent in doc.sents:
    # Initialize lists to store noun phrases and verb phrases
    noun_phrases = []
    verb_phrases = []
    
    # Extract noun phrases and verb phrases
    for token in sent:
        if "subj" in token.dep_:
            noun_phrases.append(token.text)
        elif "obj" in token.dep_:
            noun_phrases.append(token.text)
        elif "ROOT" in token.dep_:
            verb_phrases.append(token.text)
        elif "aux" in token.dep_:
            verb_phrases.append(token.text)
            
    # Print the sentence and its noun phrase and verb phrase
    print("Sentence:", sent.text)
    print("Noun Phrase:", " ".join(noun_phrases))
    print("Verb Phrase:", " ".join(verb_phrases))
    print()