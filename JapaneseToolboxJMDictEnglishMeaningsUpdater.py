#!/usr/bin/python -tt

import re
import openpyxl
from JapaneseToolboxConverter import Converter

UNIQUE_DELIMITER = "---"

current_entry = ''
LEGEND_DICT = {
    'MA': 'ZM',
    'X': 'IES',
    'abbr': 'Abr',
    'adj-i': 'Ai',
    'adj-ix': 'Ai',
    'adj-na': 'Ana',
    'adj-no': 'Ano',
    'adj-pn': 'Apn',
    'adj-t': 'Atr',
    'adj-f': 'Af',
    'adv': 'A',
    'adv-to': 'Ato',
    'arch': '',
    'ateji': '',
    'aux': '',
    'aux-v': 'Vx',
    'aux-adj': 'Ax',
    'Buddh': 'ZB',
    'chem': 'ZC',
    'chn': 'ZCL',
    'col': 'CEC',
    'comp': 'ZI',
    'conj': 'CO',
    'cop-da': '',
    'ctr': 'C',
    'derog': 'Dr',
    'eK': '',
    'ek': '',
    'exp': 'CE',
    'fam': 'LF',
    'fem': 'LFt',
    'food': 'ZF',
    'geom': 'ZG',
    'gikun': '',
    'hon': 'LHn',
    'hum': 'LHm',
    'iK': '',
    'id': 'CES',
    'ik': '',
    'int': 'OI',
    'io': '',
    'iv': '',
    'ling': 'ZL',
    'm-sl': 'ZMg',
    'male': 'LMt',
    'male-sl': 'LMt',
    'math': 'ZMt',
    'mil': 'ZMl',
    'n': 'N',
    'n-adv': 'NAdv',
    'n-suf': 'N;Sx',
    'n-pref': 'N;Px',
    'n-t': 'T',
    'num': 'num',
    'oK': '',
    'obs': 'Obs',
    'obsc': 'Obs',
    'ok': 'Obs',
    'oik': 'Obs',
    'on-mim': 'OI',
    'pn': 'P',
    'poet': 'ZP',
    'pol': 'LHn',
    'pref': 'Px',
    'proverb': 'CES',
    'prt': 'PP',
    'physics': 'ZPh',
    'quote': '',
    'rare': 'Obs',
    'sens': '',
    'sl': 'Sl',
    'suf': 'Sx',
    'uK': '',
    'uk': '',
    'unc': 'UNC',
    'yoji': '',
    'v1': 'Vrui',
    'v1-s': 'Vrui',
    'v2a-s': '',
    'v4h': '',
    'v4r': '',
    'v5aru': 'Varu',
    'v5b': 'Vbu',
    'v5g': 'Vgu',
    'v5k': 'Vku',
    'v5k-s': 'Viku',
    'v5m': 'Vmu',
    'v5n': 'Vnu',
    'v5r': 'Vru',
    'v5r-i': '',
    'v5s': 'Vsu',
    'v5t': 'Vtsu',
    'v5u': 'Vu',
    'v5u-s': 'Vus',
    'v5uru': '',
    'vz': 'Vrui',
    'vi': 'Vi',
    'vk': 'Vkuru',
    'vn': '',
    'vr': '',
    'vs': 'Vsuru',
    'vs-c': '',
    'vs-s': 'Vsuru',
    'vs-i': 'Vsuru',
    'kyb': '',
    'osb': '',
    'ksb': '',
    'ktb': '',
    'tsb': '',
    'thb': '',
    'tsug': '',
    'kyu': '',
    'rkb': '',
    'nab': '',
    'hob': '',
    'vt': 'Vt',
    'vulg': 'vul',
    'adj-kari': '',
    'adj-ku': '',
    'adj-shiku': '',
    'adj-nari': '',
    'n-pr': 'Ne',
    'v-unspec': '',
    'v4k': '',
    'v4g': '',
    'v4s': '',
    'v4t': '',
    'v4n': '',
    'v4b': '',
    'v4m': '',
    'v2k-k': '',
    'v2g-k': '',
    'v2t-k': '',
    'v2d-k': '',
    'v2h-k': '',
    'v2b-k': '',
    'v2m-k': '',
    'v2y-k': '',
    'v2r-k': '',
    'v2k-s': '',
    'v2g-s': '',
    'v2s-s': '',
    'v2z-s': '',
    'v2t-s': '',
    'v2d-s': '',
    'v2n-s': '',
    'v2h-s': '',
    'v2b-s': '',
    'v2m-s': '',
    'v2y-s': '',
    'v2r-s': '',
    'v2w-s': '',
    'archit': 'ZAc',
    'astron': 'ZAs',
    'baseb': 'ZBb',
    'biol': 'ZBi',
    'bot': 'ZBt',
    'bus': 'ZBs',
    'econ': 'ZEc',
    'engr': 'ZEg',
    'finc': 'ZFn',
    'geol': 'ZGg',
    'law': 'ZLw',
    'mahj': 'ZMj',
    'med': 'Md',
    'music': 'ZMc',
    'Shinto': 'ZSt',
    'shogi': 'ZSg',
    'sports': 'ZSp',
    'sumo': 'ZSm',
    'zool': 'ZZ',
    'joc': 'ZH',
    'anat': 'ZAn'
}
MAX_NUM_SURU_VERBS_TO_ADD = 50

# region Preparations
localWordsWorkbook = openpyxl.load_workbook(
    filename='C:/Users/Bar/Dropbox/Japanese/Grammar - 3000 kanji.xlsx', data_only=True)
localVerbsWorkbook = openpyxl.load_workbook(
    filename='C:/Users/Bar/Dropbox/Japanese/Verbs - 3000 kanji.xlsx', data_only=True)
wsLocalMeanings = localWordsWorkbook["Meanings"]
wsLocalTypes = localWordsWorkbook["Types"]
wsLocalVerbsForGrammar = localVerbsWorkbook["VerbsForGrammar"]


class Word:
    def __init__(self, akanji, aaltSpellings, ahiragana, aromaji, aenglish_meanings, atypes, acommon):
        self.kanji = akanji
        self.altSpellings = aaltSpellings
        self.hiragana = ahiragana
        self.romaji = aromaji
        self.uniqueID = self.romaji + UNIQUE_DELIMITER + self.kanji
        self.english_meanings = aenglish_meanings
        self.types = atypes
        self.common = acommon
        self.hasSuruTwin = False

    def __str__(self):
        return "Word:\n" \
               + "\t" + self.romaji \
               + "\t" + self.kanji


converter = Converter()
# endregion

# region Filling the english words list
words = []
suruVerbs = []
num_suru_verbs = 0
reached_first_entry = False
with open("JMDict_e", encoding='utf-8') as infile:
    for line in infile:

        if "<entry>" in line:
            reached_first_entry = True
        if not reached_first_entry:
            continue

        current_entry += line

        if "</entry>" in line:
            current_entry = current_entry.replace('\n', '').replace('\r', '')

            # region Getting the basic characteristics
            kanjis = re.findall(r"<keb>(.+?)</keb>", current_entry, re.U)
            if len(kanjis) > 0:
                kanji = kanjis[0]
                altSpellings = []
                for i in range(1, len(kanjis)):
                    altSpellings.append(kanjis[i])
            else:
                altSpellings = []
                kanji = ''

            kanas = re.findall(r"<reb>(.+?)</reb>", current_entry, re.U)
            hiragana = ''
            romaji = ''
            if len(kanas) > 0:
                hiragana = kanas[0]
                romaji = converter.get_latin_hiragana_katakana(hiragana)[converter.TYPE_LATIN]
                if kanji == '': kanji = hiragana

                for i in range(1, len(kanas)):
                    altSpellingRomaji = converter.get_latin_hiragana_katakana(kanas[i])[converter.TYPE_LATIN]
                    if altSpellingRomaji != romaji:
                        altSpellings.append(altSpellingRomaji)

            # endregion

            # region Getting the common status - if not common, skip this word
            match = re.search(r"<ke_pri>(news1|ichi1)</ke_pri>", current_entry)
            #match = re.search(r"<ke_pri>(news1|news2|ichi1|ichi2|spec1|spec2|gai1|gai2)</ke_pri>", current_entry)
            if match:
                common = True
            else:
                common = False
                current_entry = ''
                continue
            # endregion

            # region Getting the types/meanings and suru verb characteristics
            senses = re.findall(r"<sense>(.+?)</sense>", current_entry, re.DOTALL)
            types = []
            english_meanings = []
            types_for_word = []
            english_meanings_for_word = []
            types_for_suru_verb = []
            english_meanings_for_suru_verb = []
            suru_altSpellings = []
            suru_hiragana = ''
            suru_romaji = ''
            suru_kanji = ''
            types_as_string = '-'
            i = 0
            currentPartOfSpeech = ''
            create_suru_verb = False
            while i < len(senses):

                # region Getting the list of JMtypes
                matches = re.findall(r"<(pos|field|misc)>&(.+?);</(pos|field|misc)>", senses[i])
                JMtypes = [match[1] for match in matches]
                partsOfSpeech = [LEGEND_DICT[JMtype] for JMtype in JMtypes if LEGEND_DICT[JMtype] != '']
                if len(partsOfSpeech) == 0: partsOfSpeech.append(currentPartOfSpeech)
                # endregion

                # region Getting the TRANSITIVE status
                trans = 'I'
                if "vt" in JMtypes and "vi" in JMtypes:
                    senses.append(senses[i].replace("<pos>&vt;</pos>", ""))
                    senses[i] = senses[i].replace("<pos>&vi;</pos>", "")
                    trans = 'T'
                elif "vt" in JMtypes:
                    trans = 'T'
                # endregione

                # region If the word also includes a suru verb option, create a new sense for it
                if "vs" in JMtypes \
                        and (
                            "n" in JMtypes
                            or "adj-no" in JMtypes
                            or "adj-i" in JMtypes
                            or "adj-ix" in JMtypes
                            or "adv" in JMtypes
                            or "adv-to" in JMtypes
                        ):
                    senses.append(re.sub("<pos>&(n|adj-no|adj-na|adj-i|adj-ix|adv|adv-to);</pos>", "", senses[i]))
                    senses[i] = senses[i].replace("<pos>&vs;</pos>", "")

                    # Rebuilding JMTypes without the suru verb reference
                    matches = re.findall(r"<(pos|field|misc)>&(.+?);</(pos|field|misc)>", senses[i])
                    JMtypes = [match[1] for match in matches]
                    partsOfSpeech = [LEGEND_DICT[JMtype] for JMtype in JMtypes if LEGEND_DICT[JMtype] != '']
                    if len(partsOfSpeech) == 0: partsOfSpeech.append(currentPartOfSpeech)
                # endregion

                # region If the word includes both na-adj and noun forms, split them into two senses
                if "adj-na" in JMtypes and "n" in JMtypes:
                    senses.insert(i+1, senses[i].replace("<pos>&n;</pos>", ""))
                    senses[i] = senses[i].replace("<pos>&adj-na;</pos>", "")

                    # Rebuilding JMTypes without the adj-na reference
                    matches = re.findall(r"<(pos|field|misc)>&(.+?);</(pos|field|misc)>", senses[i])
                    JMtypes = [match[1] for match in matches]
                    partsOfSpeech = [LEGEND_DICT[JMtype] for JMtype in JMtypes if LEGEND_DICT[JMtype] != '']
                    if len(partsOfSpeech) == 0: partsOfSpeech.append(currentPartOfSpeech)
                # endregion

                # region Preparing the type depending on whether the word is a verb or not
                type_is_verb = False
                is_suru_verb = False
                for partOfSpeech in partsOfSpeech:
                    if partOfSpeech == 'Vrui' or \
                            partOfSpeech == 'Vbu' or \
                            partOfSpeech == 'Vgu' or \
                            partOfSpeech == 'Vku' or \
                            partOfSpeech == 'Vmu' or \
                            partOfSpeech == 'Vnu' or \
                            partOfSpeech == 'Vru' or \
                            partOfSpeech == 'Vsu' or \
                            partOfSpeech == 'Vtsu' or \
                            partOfSpeech == 'Vu' or \
                            partOfSpeech == 'Vi' or \
                            partOfSpeech == 'Vkuru' or \
                            partOfSpeech == 'Vsuru':
                        currentPartOfSpeech = partOfSpeech + trans
                        if partOfSpeech == 'Vsuru': is_suru_verb = True
                        type_is_verb = True
                        break

                    elif partOfSpeech != '':
                        currentPartOfSpeech = partOfSpeech
                        types.append(currentPartOfSpeech)

                if not type_is_verb:
                    currentPartOfSpeech = ";".join(types)
                # endregion

                # region Removing type duplicates
                currentPartOfSpeech = ";".join(list(set(currentPartOfSpeech.split(";"))))
                # endregion

                # region Getting the meaning
                matches = re.findall(r"<(gloss|gloss g_type=\"expl\")?>(.+?)</gloss>", senses[i], re.U)
                english_meanings = [match[1] for match in matches]
                english_meanings_as_string = ", ".join(english_meanings)
                # endregion

                # region Setting the word characteristics
                if is_suru_verb:
                    types_for_suru_verb.append(currentPartOfSpeech)
                    english_meanings_for_suru_verb.append(english_meanings_as_string)
                    suru_altSpellings = []
                    for altSpelling in altSpellings:
                        match = re.search(r"[a-zA-Z]", altSpelling)
                        if match: suru_altSpellings.append(altSpelling + "suru")
                        else: suru_altSpellings.append(altSpelling + "する")
                    suru_hiragana = hiragana + "する"
                    suru_romaji = romaji + " suru"
                    suru_kanji = kanji + "する"
                    create_suru_verb = True
                else:
                    types_for_word.append(currentPartOfSpeech)
                    english_meanings_for_word.append(english_meanings_as_string)
                # endregion

                i += 1

            # endregion

            # region Cleaning the types after sense repetition
            for i in range(len(english_meanings_for_word)):
                if i > 0 and english_meanings_for_word[i] == english_meanings_for_word[i - 1]:
                    lastTypes = types_for_word[i - 1].split(";")
                    currentTypes = types_for_word[i].split(";")
                    newCurrentTypes = []
                    for currentType in currentTypes:
                        if currentType not in lastTypes: newCurrentTypes.append(currentType)
                    types_for_word[i] = ";".join(newCurrentTypes)
            # endregion

            # region Duplicating leftover meanings if the type must be split (e.g. N;Nan)
            i = 0
            while i < len(english_meanings_for_word):
                if i > 1 and english_meanings_for_word[i-2] == english_meanings_for_word[i - 1]:
                    currentTypes = types_for_word[i].split(";")
                    if "N" in currentTypes and "NAn" in currentTypes:
                        english_meanings_for_word.insert(i+1, english_meanings_for_word[i])
                        types_for_word[i] = ";".join([currentType for currentType in currentTypes if currentType != "NAn"])
                        types_for_word.insert(i+1, ";".join([currentType for currentType in currentTypes if currentType != "N"]))
            # endregion

            # region Creating the words
            if not kanji == '' and not hiragana == '' and not (len(english_meanings_for_word) == 0):

                word = Word(kanji,
                            altSpellings,
                            hiragana,
                            romaji,
                            english_meanings_for_word,
                            types_for_word,
                            common)
                if create_suru_verb: word.hasSuruTwin = True

                if (not ((word.romaji == "ha" or word.romaji == "wa") and word.kanji == "は")) \
                        and (not ((word.romaji == "he" or word.romaji == "e") and word.kanji == "へ")) \
                        and (not ((word.romaji == "deha" or word.romaji == "dewa") and word.kanji == "では")) \
                        and (not ((word.romaji == "niha" or word.romaji == "niwa") and word.kanji == "には")) \
                        and (not (word.romaji == "kana" and word.kanji == "かな")) \
                        and (not (word.romaji == "to" and word.kanji == "と")) \
                        and (not (word.romaji == "ya" and word.kanji == "や")) \
                        and (not (word.romaji == "mo" and word.kanji == "も")) \
                        and (not (word.romaji == "no" and word.kanji == "の")) \
                        and (not (word.romaji == "n" and word.kanji == "ん")) \
                        and (not (word.romaji == "wo" and word.kanji == "を")) \
                        and (not (word.romaji == "wa" and word.kanji == "わ")) \
                        and (not (word.romaji == "yo" and word.kanji == "よ")) \
                        and (not (word.romaji == "na" and word.kanji == "な")) \
                        and (not (word.romaji == "ka" and word.kanji == "か")) \
                        and (not (word.romaji == "ga" and word.kanji == "が")) \
                        and (not (word.romaji == "ni" and word.kanji == "に")) \
                        and (not (word.kanji == "ケ" and word.kanji == "ヶ")):
                    words.append(word)

                    if create_suru_verb:
                        word = Word(suru_kanji,
                                    suru_altSpellings,
                                    suru_hiragana,
                                    suru_romaji,
                                    english_meanings_for_suru_verb,
                                    types_for_suru_verb,
                                    common)
                        suruVerbs.append(word)
                        num_suru_verbs += 1

                if len(words) % 100 == 0:
                    print("built word number " + str(len(words)) + ": " + word.kanji + "\t\tTotal suru verbs:" + str(num_suru_verbs))
            # endregion

            current_entry = ''


# endregion

# region Filtering the words list
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


workingWordsList = list(words)
workingWordsList.sort(key=lambda x: x.uniqueID)
workingSuruVerbsList = list(suruVerbs)
workingSuruVerbsList.sort(key=lambda x: x.uniqueID)

print("total number of words: " + str(len(workingWordsList)))
print("total number of suru verbs: " + str(len(workingSuruVerbsList)))

typesIndex = 1
while True:
    romaji = wsLocalTypes.cell(row=typesIndex, column=3).value
    kanji = wsLocalTypes.cell(row=typesIndex, column=4).value

    if romaji == "" or not romaji:
        break

    uniqueID = romaji + UNIQUE_DELIMITER + kanji
    #print(uniqueID + "\n")

    index_of_first_hit = binary_search(workingWordsList, uniqueID)
    if index_of_first_hit != -1:
        del workingWordsList[index_of_first_hit]

    typesIndex += 1

verbsIndex = 1

print("total number of words after words filter: " + str(len(workingWordsList)))
# print("last words:")
# for i in range(len(workingWordsList)-10, len(workingWordsList)):
#     print(workingWordsList[i])

while True:
    romaji = wsLocalVerbsForGrammar.cell(row=verbsIndex, column=3).value
    kanji = wsLocalVerbsForGrammar.cell(row=verbsIndex, column=4).value

    if romaji == "" or not romaji:
        break

    uniqueID = romaji + UNIQUE_DELIMITER + kanji
    #print(uniqueID + "\n")

    index_of_first_hit = binary_search(workingWordsList, uniqueID)
    if index_of_first_hit != -1:
        del workingWordsList[index_of_first_hit]

    index_of_first_hit = binary_search(workingSuruVerbsList, uniqueID)
    if index_of_first_hit != -1:
        del workingSuruVerbsList[index_of_first_hit]

    verbsIndex += 1

print("total number of words after verbs filter: " + str(len(workingWordsList)))
# print("last suru verbs:")
# for i in range(len(workingSuruVerbsList)-10, len(workingSuruVerbsList)):
#     print(workingSuruVerbsList[i])

print("total number of suru verbs after filter: " + str(len(workingSuruVerbsList)))
# endregion

# region Adding all the remaining words from JMDict to the end of the types sheet

# Getting the first available row index of the Local Types list
availableTypesIndex = 1
while True:
    value = wsLocalTypes.cell(row=availableTypesIndex, column=3).value
    if not value:
        break
    availableTypesIndex += 1

# Getting the first available row index of the Local Meanings list
availableMeaningsIndex = 1
while True:
    value = wsLocalMeanings.cell(row=availableMeaningsIndex, column=1).value
    if not value:
        break
    availableMeaningsIndex += 1

# Adding the words
for word in workingWordsList:

    if (word.romaji + " suru" == workingSuruVerbsList[MAX_NUM_SURU_VERBS_TO_ADD+1].romaji) \
            and (word.kanji + "する" == workingSuruVerbsList[MAX_NUM_SURU_VERBS_TO_ADD+1].kanji):
        break

    if word.types[0] == '':
        pass

    if not (word.common or word.types[0][0] == 'V'): continue

    wsLocalTypes.cell(row=availableTypesIndex, column=3).value = word.romaji
    wsLocalTypes.cell(row=availableTypesIndex, column=4).value = word.kanji
    wsLocalTypes.cell(row=availableTypesIndex, column=6).value = ", ".join(word.altSpellings)

    meaningIndexes = []
    for i in range(len(word.types)):
        currentPartOfSpeech = word.types[i]
        meaning = word.english_meanings[i]

        if len(currentPartOfSpeech) == 0:
            print("word with missing type: " + str(word))

        elif currentPartOfSpeech[0] == 'V':
            meaningAsList = [element.strip() for element in meaning.split(",")]
            meaningAsList = [element[3:] for element in meaningAsList if element[:3] == "to "]
            meaning = ", ".join(meaningAsList)

        wsLocalMeanings.cell(row=availableMeaningsIndex, column=1).value = availableMeaningsIndex
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=2).value = meaning
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=3).value = currentPartOfSpeech
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=9).value = 'JM'

        meaningIndexes.append(str(availableMeaningsIndex))
        availableMeaningsIndex += 1

    wsLocalTypes.cell(row=availableTypesIndex, column=5).value = ";".join(meaningIndexes)

    availableTypesIndex += 1

# Adding the suru verbs
word_addition_index = 0
for word in workingSuruVerbsList:

    if word_addition_index == MAX_NUM_SURU_VERBS_TO_ADD: break
    word_addition_index += 1

    if word.types[0] == '':
        pass

    if not (word.common or word.types[0][0] == 'V'): continue

    wsLocalTypes.cell(row=availableTypesIndex, column=3).value = word.romaji
    wsLocalTypes.cell(row=availableTypesIndex, column=4).value = word.kanji
    wsLocalTypes.cell(row=availableTypesIndex, column=6).value = ", ".join(word.altSpellings)

    meaningIndexes = []
    for i in range(len(word.types)):
        currentPartOfSpeech = word.types[i]
        meaning = word.english_meanings[i]

        if len(currentPartOfSpeech) == 0:
            print("word with missing type: " + str(word))

        wsLocalMeanings.cell(row=availableMeaningsIndex, column=1).value = availableMeaningsIndex
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=2).value = meaning
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=3).value = currentPartOfSpeech
        wsLocalMeanings.cell(row=availableMeaningsIndex, column=9).value = 'JM'

        meaningIndexes.append(str(availableMeaningsIndex))
        availableMeaningsIndex += 1

    wsLocalTypes.cell(row=availableTypesIndex, column=5).value = ";".join(meaningIndexes)

    availableTypesIndex += 1


# endregion

# Saving the results
localWordsWorkbook.save(
    filename='C:/Users/Bar/Dropbox/Japanese/Grammar - 3000 kanji - updated with JMDict_english.xlsx')
