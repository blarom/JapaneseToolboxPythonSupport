#!/usr/bin/python -tt

import re
import JapaneseToolboxConverter
current_entry = ''


class Word:
    def __init__(self, kanji, hiragana, french_meanings, spanish_meanings):
        self.kanji = kanji
        self.hiragana = hiragana
        self.french_meanings = french_meanings
        self.spanish_meanings = spanish_meanings




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
                kanji = match.group()

            match = re.search("<reb>(\w+)</reb>", current_entry)
            hiragana = ''
            if match:
                hiragana = match.group()

            match_tuples = re.findall("<gloss xml:lang=\"fre\">(\w+)</gloss>", current_entry)
            french_meanings = []
            for i in range(len(match_tuples)):
                french_meanings.append(match_tuples[i])

            match_tuples = re.findall("<gloss xml:lang=\"spa\">(\w+)</gloss>", current_entry)
            spanish_meanings = []
            for i in range(len(match_tuples)):
                spanish_meanings.append(match_tuples[i])

            if not kanji == '' and not hiragana == '' and not (len(french_meanings) == 0 and len(spanish_meanings) == 0):
                word = Word(kanji, hiragana, french_meanings, spanish_meanings)
                words.append(word)

            current_entry = ''
