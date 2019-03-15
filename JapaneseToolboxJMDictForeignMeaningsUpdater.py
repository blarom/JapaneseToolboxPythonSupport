#!/usr/bin/python -tt

import re
import openpyxl
from JapaneseToolboxConverter import Converter

current_entry = ''

# region Preparations
localWordsWorkbook = openpyxl.load_workbook(
    filename='C:/Users/Bar/Dropbox/Japanese/Grammar - 3000 kanji.xlsx', data_only=True)
wsLocalMeanings = localWordsWorkbook["Meanings"]
wsLocalMeaningsFR = localWordsWorkbook["MeaningsFR"]
wsLocalMeaningsES = localWordsWorkbook["MeaningsES"]
wsLocalTypes = localWordsWorkbook["Types"]


class Word:
    def __init__(self, kanji, hiragana, romaji, french_meanings, spanish_meanings):
        self.kanji = kanji
        self.hiragana = hiragana
        self.romaji = romaji
        self.uniqueID = romaji + "zzz" + kanji
        self.french_meanings = french_meanings
        self.spanish_meanings = spanish_meanings


converter = Converter()
# endregion

# region Filling the foreign words list
words = []
reached_first_entry = False
with open("JMDict", encoding='utf-8') as infile:
    for line in infile:

        if "<entry>" in line:
            reached_first_entry = True
        if not reached_first_entry:
            continue

        current_entry += line

        if "</entry>" in line:
            match = re.search("<keb>(\w+)</keb>", current_entry)
            kanji = ''
            if match:
                kanji = match.group(1)

            match = re.search("<reb>(\w+)</reb>", current_entry)
            hiragana = ''
            if match:
                hiragana = match.group(1)

            match_tuples = re.findall("<gloss xml:lang=\"fre\">(\w+)</gloss>", current_entry)
            french_meanings = []
            for i in range(len(match_tuples)):
                french_meanings.append(match_tuples[i])

            match_tuples = re.findall("<gloss xml:lang=\"spa\">(\w+)</gloss>", current_entry)
            spanish_meanings = []
            for i in range(len(match_tuples)):
                spanish_meanings.append(match_tuples[i])

            if not kanji == '' and not hiragana == '' \
                    and not (len(french_meanings) == 0 and len(spanish_meanings) == 0):
                word = Word(kanji,
                            hiragana,
                            converter.get_latin_hiragana_katakana(hiragana)[converter.TYPE_LATIN],
                            french_meanings,
                            spanish_meanings)
                words.append(word)

            current_entry = ''


# endregion

#region Updating the Types and Meaning sheets with the values
def binary_search(words_list, text, lo=0, hi=None):
    # https://stackoverflow.com/questions/4161629/search-a-list-of-objects-in-python
    if hi is None:
        hi = len(words_list)
    while lo < hi:
        mid = (lo + hi) // 2

        if text > words_list[mid].uniqueID:
            lo = mid + 1
        elif text < words_list[mid].uniqueID:
            hi = mid
        elif text == words_list[mid].uniqueID:
            return mid
        else:
            return -1

    return -1


typesIndex = 1
workingWordsList = list(words)
workingWordsList.sort(key=lambda x: x.uniqueID)
meaningFRindex = 2
meaningESindex = 2
while True:
    romaji = wsLocalTypes.cell(row=typesIndex, column=3).value
    kanji = wsLocalTypes.cell(row=typesIndex, column=4).value
    meaningIndexes = wsLocalTypes.cell(row=typesIndex, column=5).value

    if romaji == "" or not romaji:
        break

    uniqueID = romaji + "zzz" + kanji
    print(uniqueID + "\n")

    index_of_first_hit = binary_search(workingWordsList, uniqueID)
    if index_of_first_hit != -1:

        word = workingWordsList[index_of_first_hit]

        #print(word.romaji + "-" + word.kanji + "\n")
        meaningIndex = int(meaningIndexes.split(";")[0])
        firstENmeaning = str(wsLocalMeanings.cell(row=meaningIndex, column=2).value)
        firstENtype = str(wsLocalMeanings.cell(row=meaningIndex, column=3).value)

        for i in range(len(word.french_meanings)):
            wsLocalMeaningsFR.cell(row=meaningFRindex, column=2).value = word.french_meanings[i]
            meaningFRindex += 1

        for i in range(len(word.spanish_meanings)):
            wsLocalMeanings.cell(row=meaningESindex, column=13).value = word.spanish_meanings[i]
            meaningESindex += 1

    typesIndex += 1
#endregion

# Saving the results
localWordsWorkbook.save(filename='C:/Users/Bar/Dropbox/Japanese/Grammar - 3000 kanji - updated with JMDict_foreign.xlsx')
