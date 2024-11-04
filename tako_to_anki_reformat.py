import csv
import re

# Export shared decks from app to Anki
# Download Takoboto deck from Anki
INPUT_CSV = 'Takoboto_Shared_Decks.csv' # put name of downloaded file here
MAX_ROWS_PER_FILE = 2500
OUTPUT_DIR = 'output' # Name of folder/directory for output CSV files

with open(INPUT_CSV,'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    fronts = [] # head Japanese entries, front of Anki card
    readings = []
    translations = []
    parts_of_speech = [] # part-of-speech
    sents = [] # example sentences
    sents_eng = [] # example sentence translations
    tags = []

    for row in csv_reader:
        fronts.append(row[0])
        readings.append(row[1])
        translations.append(row[2])
        parts_of_speech.append(row[3])
        sents.append(row[4])
        sents_eng.append(row[5])
        tags.append(row[7])

# Modify some tag names
tags = [tag.replace('common','一般的な言葉') for tag in tags]

backs = []

for i in range(len(fronts)):
    back_contents = ''
    
    if len(readings[i]) > 0:
        back_contents += (readings[i] + '<br><br>')

    back_contents += translations[i]
    
    if sents[i] != '':
        back_contents += ('<br><br>' + sents[i])

    if sents_eng[i] != '':
        back_contents += ('<br>' + sents_eng[i])  

    backs.append(back_contents)

print(fronts[:10])
print(backs[:10])
print(tags[:10])

# TODO: Print to separate CSV files based on which tags the words have
# Words with multiple tags shoudl only be printed to one file, doesn't matter which
# Still include tag field in the ouput CSV files

# Ensure the 'Output' directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Writing to output CSV files...")
if len(tags) == len(fronts) == len(backs):
    file_count = 1
    row_count = 0

    # Open the first CSV file for writing
    file = open(os.path.join(OUTPUT_DIR, f'output_{file_count}.csv'), 'w', newline='')
    writer = csv.writer(file)

    for i in range(len(fronts)):
        if row_count >= MAX_ROWS_PER_FILE:
            # Close the current file and open a new one
            file.close()
            file_count += 1
            row_count = 0
            file = open(os.path.join(OUTPUT_DIR, f'output_{file_count}.csv'), 'w', newline='')
            writer = csv.writer(file)

        # Write the data to the file
        writer.writerow([fronts[i], backs[i], tags[i]])
        row_count += 1

    # Close the last file
    file.close()
else:
    print("Lists are not of the same length.")

print("Completed.")
# (Optional) when importing to Anki, add 'TAKOBOTO' as a tag for all cards