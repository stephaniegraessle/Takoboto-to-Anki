import csv
import re

# TODO: Add a "~" to the head word if the definitions includes a suffix--separate by suffix and non-suffix entries?

# INPUT_CSV files:
# 0 - Download in Takoboto app: Word lists > ... > Export to file... > SAVE
# 1 - Export shared decks from app to Anki > Download Takoboto deck from Anki

# Change file names to match the names of the downloaded files
INPUT_CSV = ['Takoboto.20241101-160953.csv', 'Takoboto - Sheet1.csv'] # [0,1]
MAX_ROWS_PER_FILE = 2500

with open(INPUT_CSV[0],'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    # Get necessary info from column
    tags_0 = []
    jap_0 = []
    eng_0 = []
    for row in csv_reader:
        tags_0.append(row[0])
        jap_0.append(row[3])
        eng_0.append(row[4])

with open(INPUT_CSV[1],'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    head_words_1 = [] # head Japanese entries, front of Anki card
    readings_1 = []
    translations_1 = []
    parts_of_speech_1 = [] # part-of-speech
    sents_1 = [] # example sentences
    sents_eng_1 = [] # example sentence translations
    tags_1 = []

    for row in csv_reader:
        head_words_1.append(row[0])
        readings_1.append(row[1])
        translations_1.append(row[2])
        parts_of_speech_1.append(row[3])
        sents_1.append(row[4])
        sents_eng_1.append(row[5])
        tags_1.append(row[7])

# Remove first row from lists in CSV 0 (column names)
tags_0.pop(0)
jap_0.pop(0)
eng_0.pop(0)

# Modify some tag names
tags_0 = [tag.replace('Contributions','TAKOBOTO_貢献') for tag in tags_0]
tags_0 = [tag.replace('Favorites','TAKOBOTO_お気に入り') for tag in tags_0]
tags_0 = [tag.replace('History','TAKOBOTO_歴史') for tag in tags_0]
tags_1 = [tag.replace('Common','一般的な言葉') for tag in tags_1]

# Split apart Japanese words--first word on front of card
jap_lists_0 = [re.split(r'[;,]\s*', entry) for entry in jap_0]

head_words_0 = []
readings_0 = []

for entry in jap_lists_0:
    if len(entry) > 0:
        head_words_0.append(entry[0])
        readings_0.append(entry[1:] if len(entry) > 1 else [''])

# TODO: Remove non-English entries from translations_1
# If there are multiple translations in a list, (1., 2., etc.),
# delete any listed translations after the last English translation.

# Combine information from both CSVs
print("Combining imported CSVs...")
head_words = list(set(head_words_0 + head_words_1))
tags = [] # TODO: Make each set of tags a single string within the list, not list within list
readings = []
translations = []
sents = []
sents_eng = []

for word in head_words:
    # Combine tags and split on spaces
    tags_combined = set()
    if word in head_words_0:
        index_0 = head_words_0.index(word)
        tags_combined.update(tags_0[index_0].split())  # Split tags by spaces
    if word in head_words_1:
        index_1 = head_words_1.index(word)
        tags_combined.update(tags_1[index_1].split())  # Split tags by spaces
    tags.append(list(tags_combined))  # Keep as list of individual tags

    
    # Combine readings, CSV 0 readings preferred
    if word in head_words_0:
        index_0 = head_words_0.index(word)
        readings.append(readings_0[index_0])
    else:
        index_1 = head_words_1.index(word)
        readings.append(readings_1[index_1])
    
    # Combine translations, CSV 0 translations preferred
    if word in head_words_1:
        index_1 = head_words_1.index(word)
        translations.append(translations_1[index_1])
    else:
        index_0 = head_words_0.index(word)
        translations.append(eng_0[index_0])
    
    # Combine sentences
    if word in head_words_1:
        index_1 = head_words_1.index(word)
        sents.append(sents_1[index_1])
        sents_eng.append(sents_eng_1[index_1])
    else:
        sents.append('')
        sents_eng.append('')

# Remove any 'Deleted' words at the start of the lists
for i in range(len(head_words)):
    head_words_temp = head_words

    if head_words[i] == '':
        head_words_temp.pop(0)
        tags.pop(0)
        readings.pop(0)
        translations.pop(0)
        sents.pop(0)
        sents_eng.pop(0)
    else:
        head_words = head_words_temp
        break

print("Creating cards...")
fronts = head_words # head japanese entry
backs = [] # alternate Japanese entries + English translations + sentences

for i in range(len(fronts)):
    back_contents = ''

    # Add reading and alternate readings of Japanese word
    if type(readings[i]) == list:
        for reading in readings[i]:
            back_contents += reading
            back_contents += '<br>'
        back_contents += '<br>'
    elif type(readings[i]) == str:
        if readings[i] != '':
            back_contents += readings[i]
            back_contents += '<br><br>'

    # Add translations
    back_contents += translations[i]
    
    if sents[i] != '': # Add Japanese sentence if there is one
        back_contents+='<br><br>'
        back_contents+=sents[i]
        
        if sents_eng != '': # Add English translation if there is one
            back_contents+='<br>'
            back_contents+=sents_eng[i]

    backs.append(back_contents) 

#print(fronts[:10])
#print()
#print(backs[:10])
#print()
#print(tags[:10])

print("Writing to output CSV files...")
if len(tags) == len(fronts) == len(backs):
    tag_files = {}  # Dictionary to track open files for each tag

    for i in range(len(fronts)):
        for tag in tags[i]:  # Each tag in the current entry
            if tag not in tag_files:
                tag_files[tag] = open(f'output_{tag}.csv', 'w', newline='')
                writer = csv.writer(tag_files[tag])

            # Write the data to the relevant file(s)
            writer = csv.writer(tag_files[tag])
            writer.writerow([fronts[i], backs[i], ' '.join(tags[i])])  # Include all tags in one cell

    # Close all open files
    for file in tag_files.values():
        file.close()

print("Completed.")
# (Optional) when importing to Anki, add 'TAKOBOTO' as a tag for all cards