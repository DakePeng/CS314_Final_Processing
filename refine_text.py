# Process a list of txt files and does the following:
# 1. Remove all lines after a line that says "References"
# 2. Remove all [] surrounded numbers
# 3. Remove all "-" in the end of lines
# 4. Join all lines with " " 
import os
import re

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove newline characters
    content = content.replace('\n', ' ')

    # Remove "-" at the end of some lines
    content = content.replace('- ', '')

    # Remove words that are numbers surrounded by square brackets
    content = re.sub(r'\[\s*\d+\s*\]', '', content)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

import os

def remove_lines_after_references(file_path):
    lines = []
    found_references = False
    with open(file_path, 'r') as file:
        for line in file:
            if "references" in line.lower():
                found_references = True
            if not found_references:
                lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(lines)

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            remove_lines_after_references(file_path)
            process_file(file_path)

# Replace 'folder_path' with the path to your folder containing text files
folder_path = './OpenAI_Research_Text/'
process_folder(folder_path)
