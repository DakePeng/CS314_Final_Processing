# Functionality:
# 1. Counts the frequency of words (more precisely, the root, uninflected version of words) in a folder of txt files; 
# 2. Filters out words above a certain frequency; 
# 3. Generates a csv file
# code generated by ChatGPT, https://chatgpt.com/share/e7c22574-ebc2-48d0-8715-9ea03cc1e9b9 and 
# https://chatgpt.com/share/80e61ee9-e3db-4824-a05e-274ea2bc7173
import spacy
from collections import Counter
import csv
import os

# only keep words above a certain frequency
freq_threshhold = 5

# Load the English language model
nlp = spacy.load("en_core_web_sm")

custom_stop_words =["al", 'et', 'arxiv', 'pp', 'ae', 'es','TRUE',
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


for word in custom_stop_words:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True

# Function to check if a token is a legitimate word
def is_legit_word(token):
    return token.is_alpha and not token.is_stop

# Function to process text and count word frequencies
def process_text(text):
    doc = nlp(text)
    words = [token.lemma_.lower() for token in doc if is_legit_word(token)]
    return Counter(words)

# Folder containing text files
folder_path = "./OpenAI_Research_Text/"

# Output CSV file
csv_file = "word_frequencies.csv"

# Initialize word frequencies counter
word_freq = Counter()

# Iterate over files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Process only text files
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            word_freq += process_text(text)

# Sort word frequencies by frequency in descending order
sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

# Write sorted word frequencies to a CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Word", "Frequency"])
    for word, freq in sorted_word_freq:
        if freq > freq_threshhold:
            writer.writerow([word, freq])

print(f"Word frequencies saved to {csv_file}")

