# Takoboto-to-Anki
I created this Python code for
1. Tranferring saved entries in [Takoboto Japanese dictionary](https://takoboto.jp/) to [Anki](https://apps.ankiweb.net/) as flashcards
2. Modifying the format of cards imported to Anki from Takoboto into a format that I prefer

Feel free to change the code to fit your needs.

## Instructions

### Transferring Authored Takoboto lists to Anki

Requirements:
- Takoboto app
- AnkiDroid or AnkiWeb

Advantages:
- Do not need to have AnkiDroid app installed
- Able to immediately download all 'Authored lists'
- Contains all different readings of the word entries

Limitations:
- Only includes 'Authored lists' created by yourself, does not include 'Downloaded lists'
- Does not include additional information, e.g., example sentences

File: `tako_to_anki_own.py`

1. Go to the word lists view in the Takoboto app (... > 'Lists of words')
2. Export entire collection as a .csv file (... > 'Export to file...' > 'SAVE')
3. Move the .csv file to be the same file location as `tako_to_anki_own.py`
4. From within `tako_to_anki_own.py`, edit `INPUT_CSV` variable to match the name of the .csv file.
5. Run `tako_to_anki_own.py`
6. From Anki Desktop, select 'Import File' and select the desired output file to import into Anki.

### Reformatting Anki Cards Exported from Takoboto App (Recommended)

Requirements:
- Takoboto App
- AnkiDroid
- AnkiWeb

Advantages:
- Able to make/modify cards for 'Downloaded lists' as well as 'Authored
- Contains additional information, e.g., example sentences.

Limitations:
- Need to have AnkiDroid app installed
- Can only export each deck one by one to AnkiDroid, which can be time consuming if you have many decks.
- Only contains one reading of the 'head' Japanese word in the dictionary entry.

File: `tako_to_anki_reformat.py`

1. Export own 'Authored lists' or 'Downloaded lists' from within the Takoboto app to AnkiDroid. (... > 'Lists of words' > Open a list > ... > 'Send to AnkiDroid')
2. Download the 'Takoboto' deck from within AnkiDroid or Anki Desktop (Select a deck > 'Export deck' > Export format: 'Notes in Plain Text (.txt)'; Include: 'Takoboto') > 'OK')
3. Open the .txt file and copy all file contents using Ctrl+A, Ctrl+C.
4. Open Microsoft Excel or Google Sheets, paste the contents (Ctrl+V), and save as a .csv file.
5. Move the .csv file to be the same file location as `tako_to_anki_reformat.py`
6. From within `tako_to_anki_reformat.py`, edit `INPUT_CSV` variable to match the name of the .csv file.
7. Run `tako_to_anki_reformat.py`
8. From Anki Desktop, select 'Import File' and select the desired output file to import into Anki.

## Planned future improvements
- Change output CSV file generation to have words separated by tag names