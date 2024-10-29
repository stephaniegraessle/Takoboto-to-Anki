import csv
import re
#from  langdetect import detect

# Download in Takoboto app: Word lists > ... > Export to file... > SAVE
INPUT_CSV = 'Takoboto.20241017-214545.csv' # put name of downloaded file here
MAX_ROWS_PER_FILE = 1000
# (Optional) when importing to Anki, add 'TAKOBOTO' as a tag for all cards

print("Reading information from input CSV file...")
with open(INPUT_CSV,'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    # Get necessary info from column
    tags = []
    jap = []
    eng = []
    for row in csv_reader:
        tags.append(row[0])
        jap.append(row[3])
        eng.append(row[4])

print("Removing first row from lists...")
# Remove first row from lists (column names)
tags.pop(0)
jap.pop(0)
eng.pop(0)

print("Modifying tag names...")
# Change some tag names
tags = [tag.replace('Contributions','TAKOBOTO_貢献') for tag in tags]
tags = [tag.replace('Favorites','TAKOBOTO_お気に入り') for tag in tags]
tags = [tag.replace('History','TAKOBOTO_歴史') for tag in tags]

print("Splitting Japanese words apart...")
# Split apart Japanese words--first word on front of card
jap_lists = [re.split(r'[;,]\s*', entry) for entry in jap]

"""
print("Removing non-English words from translations...")
def is_english(word):
    try:
        return detect(word) == 'en'
    except:
        return False

eng_lists = []
for entry in eng:
    if is_english(entry):
        words = entry.split()
        eng_lists.append(words)
    else:
        words = entry.split()
        temp = [word for word in words if is_english(word)]
        eng_lists.append(temp)
"""

print("Formatting columens for output CSV...")
front = [] # head Japanese entry
back = [] # alternate Japanese entries + English translations

for i in range(len(tags)):
    front.append(jap_lists[i][0]) # get head word from JP entry

    # Add alternate readings of Japanese word
    if (len(jap_lists[i]) > 0):
        back_contents = "<br>".join(jap_lists[i][1:])
        back_contents += "<br><br>"
    else:
        back_contents = ""

    # Add English translations
    #back_contents += ''.join(eng_lists[i])
    back_contents += eng[i]
    back.append(back_contents) 

#print(tags[:10])
#print(front[:10])
#print(back[:10])

# Combine the tags of duplicate entries
combined_entries = {}
for i in range(len(front)):
    if front[i] in combined_entries:
        combined_entries[front[i]]['tags'].append(tags[i])
    else:
        combined_entries[front[i]] = {'tags': [tags[i]], 'back': back[i]}

# TODO: Print to separate CSV files based on which tags the words have
# Words with multiple tags shoudl only be printed to one file, doesn't matter which
# Still include tag field in the ouput CSV files

print("Writing processed information to output CSV files...")
if len(tags) == len(front) == len(back):
    file_count = 1
    row_count = 0

    # Open the first CSV file for writing
    file = open(f'output_{file_count}.csv', 'w', newline='')
    writer = csv.writer(file)

    for key in combined_entries:
        if row_count >= MAX_ROWS_PER_FILE:
            # Close the current file and open a new one
            file.close()
            file_count += 1
            row_count = 0
            file = open(f'output_{file_count}.csv', 'w', newline='')
            writer = csv.writer(file)

        # Combine tags into a single string
        tags_combined = ' '.join(combined_entries[key]['tags'])
        # Write the data to the file
        writer.writerow([key, combined_entries[key]['back'], tags_combined])
        row_count += 1

    # Close the last file
    file.close()
else:
    print("Lists are not of the same length.")

print("Completed.")