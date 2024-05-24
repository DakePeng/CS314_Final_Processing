import csv
from collections import Counter
    
# Initialize an empty list to store the words
word_frequency_dict = {}
pairs_to_columns_dict = {}
pairs_counter = Counter()

# Open the CSV file
with open('word_frequencies.csv', newline='') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)
    
    # Skip the first line
    next(csv_reader)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Add the word from the first column to the list
        word_frequency_dict[row[0]] = row[1]

# Open the CSV file
with open('verb_noun_pairs.csv', newline='') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)
    
    # Skip the first line
    next(csv_reader)
     
    #keep track of which column this is
    column_number = 1
    
    # Iterate over each row in the CSV file
    for row in csv_reader:
        noun_root = row[2]
        verb_root = row[3]
        noun_phrase = row[4]
        if noun_root in word_frequency_dict and verb_root in word_frequency_dict:
            pair = (noun_root, verb_root)
            pairs_counter[pair] += 1;
            if(pairs_counter[pair] == 1):
                pairs_to_columns_dict[pair] = [column_number]
            else:
                pairs_to_columns_dict[pair].append(column_number)
        column_number += 1
                
output_file_path = 'verb_noun_pair_frequency.csv'

with open(output_file_path, 'w', encoding='utf-8', newline='\n') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Pair', 'Count', 'RowsInPairTable'])
    for pair, count in pairs_counter.items():
        writer.writerow([pair, count, pairs_to_columns_dict[pair]])
