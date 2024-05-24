# CS314_Final_Processing

Written by Dake Peng, Carleton College, S24

For the Final Project of CS 314: Data Visualization offered in Spring 2024, taught by Prof. Eric Alexander

Joint (sub-) project with the reasearch project [AI Cognition](https://github.com/DakePeng/AICognition), by Dake Peng and Prof. Jay McKinney

## Prerequisites:

Start with a folder of txt files that are from arxiv

Install the following packages:

spacy, csv

## Running:

Modify the input_path (file_path, folder_path) in main() in all .py Code before running

Run the 4 pieces of code in order:

refine_text.py

get_single_word_frequency.py

get_noun_verb_pairs.py

get_pair_frequency.py

## Results:

The code will generate 3 csv files for the project:

### word_frequencies.csv 

This file contains 2 columns: [Word, Frequency]. 

This is a list of the most frequently appearing words in the text files and the # of times they occurred.

For now, the _freq_threshhold_ in _get_single_word_frequency.py_ is set to 5, meaning that only words that appear >= 5 times will be included.

### verb_noun_pairs.csv

This file contains 6 columns: [Source,Sentence,Root Noun,Root Verb,Noun Phrase,Verb Phrase]

For each verb in each document, Natural Language Processing is done to obtain the Noun Phrase and the Verb Phrase that the verb is involved in. 

Then, the Root Noun and Root Verb (uninflected tense) are found.

This information is then logged as a row in this csv file along with the entire sentence the word comes from and a link to the source of this 

For more information on how the Phrases and Heads are generated, check the comments on _get_noun_verb_pairs.py_

### verb_noun_pair_frequency.csv

This file contains 3 columns: [Pair,Count,RowsInPairTable]

**Pair** includes different Nound-Verb pairings of words that are both in the Root columns of _verb_noun_pairs.csv_ and are included in _word_frequencies.csv_ 

**Count** indicates the number of times that pairing appeared in the text

**RowsInPairTable** contains a list of indexes for the _verb_noun_pairs.csv_ in which the pairings appeared.


