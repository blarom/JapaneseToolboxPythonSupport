#!/usr/bin/python -tt
import re

import Globals

content = Globals.get_file_contents(f'{Globals.JAPAGRAM_ASSETS_DIR}/LineRomanizations.csv')
ROMANIZATIONS = {
    Globals.ROMANIZATIONS_HIRA: [],
    Globals.ROMANIZATIONS_KATA: [],
    Globals.ROMANIZATIONS_WAPU: [],
    Globals.ROMANIZATIONS_HEPB: [],
    Globals.ROMANIZATIONS_NISH: [],
    Globals.ROMANIZATIONS_KUSH: []
}
for line in content.split('\n'):
    elements = line.split('|')
    if len(elements) < 6: continue
    ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA] += [elements[Globals.ROMANIZATIONS_HIRA]]
    ROMANIZATIONS[Globals.ROMANIZATIONS_KATA] += [elements[Globals.ROMANIZATIONS_KATA]]
    ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU] += [elements[Globals.ROMANIZATIONS_WAPU]]
    ROMANIZATIONS[Globals.ROMANIZATIONS_HEPB] += [elements[Globals.ROMANIZATIONS_HEPB]]
    ROMANIZATIONS[Globals.ROMANIZATIONS_NISH] += [elements[Globals.ROMANIZATIONS_NISH]]
    ROMANIZATIONS[Globals.ROMANIZATIONS_KUSH] += [elements[Globals.ROMANIZATIONS_KUSH]]


def getOfficialKana(inputText):
    if ROMANIZATIONS is None:
        return ["", "", "", ""]
    # Transliterations performed according to https:en.wikipedia.org/wiki/Romanization_of_Japanese
    transliteratedToHiragana = inputText
    transliteratedToKatakana = inputText
    romajiTypes = [
        Globals.ROMANIZATIONS_WAPU,
        Globals.ROMANIZATIONS_HEPB,
        Globals.ROMANIZATIONS_NISH,
        Globals.ROMANIZATIONS_KUSH
    ]
    romanizationsLength = len(ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA])

    # Translating from Katakana to Hiragana
    for i in range(romanizationsLength):
        currentChar = ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i]
        if currentChar == "": continue
        transliteratedToHiragana = transliteratedToHiragana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i])

    # Translating from from Hiragana to Katakana
    for i in range(romanizationsLength):
        currentChar = ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i]
        if currentChar == "": continue
        transliteratedToKatakana = transliteratedToKatakana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i])

    # Translating from Romaji to Kana
    for romajiType in romajiTypes:
        for i in range(romanizationsLength):
            currentChar = ROMANIZATIONS[romajiType][i]
            if ((currentChar == "")
                    or (currentChar == "aa")
                    or (currentChar == "ii")
                    or (currentChar == "uu")
                    or (currentChar == "ee")
                    or (currentChar == "oo")):
                continue
            transliteratedToHiragana = transliteratedToHiragana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i])
            transliteratedToKatakana = transliteratedToKatakana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i])

        # If there are leftover double-vowels, only then should they be replaced
        for i in range(romanizationsLength):
            currentChar = ROMANIZATIONS[romajiType][i]
            if ((currentChar == "")
                    or not ((currentChar == "aa")
                            or (currentChar == "ii")
                            or (currentChar == "uu")
                            or (currentChar == "ee")
                            or (currentChar == "oo"))):
                continue
            transliteratedToHiragana = transliteratedToHiragana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i])
            transliteratedToKatakana = transliteratedToKatakana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i])

    # If there are leftover consonants, replace them by a japanized version
    oldTransliteration = transliteratedToHiragana
    transliteratedToHiragana = re.sub("([bdfghjkmnprstvz])", "\1u", transliteratedToHiragana)
    transliteratedToKatakana = re.sub("([bdfghjkmnprstvz])", "\1u", transliteratedToKatakana)

    if not (oldTransliteration == transliteratedToHiragana):
        for i in range(romanizationsLength):
            currentChar = ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU][i]
            if ((currentChar == "")
                    or (currentChar == "aa")
                    or (currentChar == "ii")
                    or (currentChar == "uu")
                    or (currentChar == "ee")
                    or (currentChar == "oo")):
                continue
            transliteratedToHiragana = transliteratedToHiragana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i])
            transliteratedToKatakana = transliteratedToKatakana.replace(currentChar, ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i])

    # Cleaning the leftovers
    transliteratedToHiragana = re.sub("[a-z]", "*", transliteratedToHiragana)
    transliteratedToKatakana = re.sub("[a-z]", "*", transliteratedToKatakana)
    transliteratedToHiragana = transliteratedToHiragana.replace('#', '')
    transliteratedToKatakana = transliteratedToKatakana.replace('#', '')

    return [transliteratedToHiragana, transliteratedToKatakana]


def getWaapuroHiraganaKatakana(text):
    conversionsFirstElement = []
    if text == '':
        conversionsFirstElement.append("")
        conversionsFirstElement.append("")
        conversionsFirstElement.append("")
    else:
        conversions = getTransliterationsAsLists(text)
        conversionsFirstElement.append(conversions[Globals.ROMANIZATIONS_WAPU][0])
        conversionsFirstElement.append(conversions[Globals.ROMANIZATIONS_HIRA][0])
        conversionsFirstElement.append(conversions[Globals.ROMANIZATIONS_KATA][0])

    return conversionsFirstElement


def getTransliterationsAsLists(inputQuery):
    waapuroRomanizations = getWaapuroRomanizationsFromLatinText(inputQuery)
    hiraganaConversions = []
    katakanaConversions = []
    waapuroConversions = []
    conversionsMH = []
    conversionsNS = []
    conversionsKS = []
    for conversion in waapuroRomanizations:
        hiraKata = getOfficialKana(conversion)
        hiragana = hiraKata[Globals.ROMANIZATIONS_HIRA]
        katakana = hiraKata[Globals.ROMANIZATIONS_KATA]
        romanizations = getOfficialRomanizations(hiragana)
        hiraganaConversions.append(hiragana)
        katakanaConversions.append(katakana)
        waapuroConversions.append(romanizations[0])
        conversionsMH.append(romanizations[1])
        conversionsNS.append(romanizations[2])
        conversionsKS.append(romanizations[3])

    return [
        hiraganaConversions,
        katakanaConversions,
        waapuroConversions,
        conversionsMH,
        conversionsNS,
        conversionsKS
    ]


def getWaapuroRomanizationsFromLatinText(text):
    text = text.lower()
    finalStrings = []

    text = text.replace("sy", "sh")
    text = text.replace("ty", "ch")

    text = text.replace("j", "A")
    text = text.replace("zy", "B")
    text = text.replace("ts", "C")
    text = text.replace("zu", "D")
    text = text.replace("du", "O")
    text = text.replace("wê", "E")
    text = text.replace("dû", "F")
    text = text.replace("si", "G")
    text = re.sub(r"([^sc])hu", "$1I", text)
    text = re.sub(r"([^sc])hû", "$1J", text)
    text = text.replace("tû", "K")
    text = text.replace("zû", "M")
    text = text.replace("n'", "N")
    text = re.sub(r"t$", "to", text)
    text = re.sub(r"c([aeiou])", "k$1", text)
    text = re.sub(r"l([aeiou])", "r$1", text)
    text = re.sub(r"q([aeiou])", "k$1", text)

    possibleInterpretations = []
    for character in list(text):
        if character == "ō" or character == "ô":
            newPhonemes = ["ou", "oo"]
        elif character == "A" or character == "B":
            newPhonemes = ["j", "dy"]
        elif character == "C":
            newPhonemes = ["ts"]
        elif character == "D" or character == "O":
            newPhonemes = ["zu", "du"]
        elif character == "E" or character == "ē" or character == "ê":
            newPhonemes = ["ee"]
        elif character == "F":
            newPhonemes = ["zuu"]
        elif character == "G":
            newPhonemes = ["shi"]
        elif character == "I":
            newPhonemes = ["hu", "fu"]
        elif character == "J":
            newPhonemes = ["fuu"]
        elif character == "K":
            newPhonemes = ["tsuu"]
        elif character == "M":
            newPhonemes = ["duu", "zuu"]
        elif character == "N":
            newPhonemes = ["n'"]
        elif character == "ā" or character == "â":
            newPhonemes = ["aa"]
        elif character == "ū" or character == "û":
            newPhonemes = ["uu"]
        else:
            newPhonemes = [character]
        possibleInterpretations = addPhonemesToInterpretations(possibleInterpretations, newPhonemes)
    for i in range(len(possibleInterpretations)):
        finalStrings.append("".join(possibleInterpretations[i]))
    return finalStrings


def addPhonemesToInterpretations(possibleInterpretations, phonemes):
    if len(phonemes) == 2:
        if not possibleInterpretations:
            newCharacterList = [phonemes[0]]
            possibleInterpretations.append(newCharacterList)
            newCharacterList = [phonemes[1]]
            possibleInterpretations.append(newCharacterList)
        else:
            initialSize = len(possibleInterpretations)
            for i in range(initialSize):
                newCharacterList = list.copy(possibleInterpretations[i])
                newCharacterList.append(phonemes[0])
                possibleInterpretations[i].append(phonemes[1])
                possibleInterpretations.append(newCharacterList)
    elif len(phonemes) == 1:
        if not possibleInterpretations:
            newCharacterList = [phonemes[0]]
            possibleInterpretations.append(newCharacterList)
        else:
            for i in range(len(possibleInterpretations)):
                possibleInterpretations[i].append(phonemes[0])
    else:
        return []

    return possibleInterpretations


def getOfficialRomanizations(kana):
    if not ROMANIZATIONS:
        return ["", "", "", ""]
    romanizedKanaWaapuro = kana
    romanizedKanaModHepburn = kana
    romanizedKanaNihonShiki = kana
    romanizedKanaKunreiShiki = kana
    romanizationsLength = len(ROMANIZATIONS[0])
    for i in range(romanizationsLength):
        currentKana = ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i]
        if currentKana:
            romanizedKanaWaapuro = romanizedKanaWaapuro.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU][i])
            romanizedKanaModHepburn = romanizedKanaModHepburn.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_HEPB][i])
            romanizedKanaNihonShiki = romanizedKanaNihonShiki.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_NISH][i])
            romanizedKanaKunreiShiki = romanizedKanaKunreiShiki.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_KUSH][i])

        currentKana = ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i]
        if currentKana:
            romanizedKanaWaapuro = romanizedKanaWaapuro.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU][i])
            romanizedKanaModHepburn = romanizedKanaModHepburn.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_HEPB][i])
            romanizedKanaNihonShiki = romanizedKanaNihonShiki.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_NISH][i])
            romanizedKanaKunreiShiki = romanizedKanaKunreiShiki.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_KUSH][i])

    return [romanizedKanaWaapuro, romanizedKanaModHepburn, romanizedKanaNihonShiki, romanizedKanaKunreiShiki]


def getOfficialWaapuroOnly(kana):
    if not ROMANIZATIONS:
        return ''
    romanizedKanaWaapuro = kana
    romanizationsLength = len(ROMANIZATIONS[0])
    for i in range(romanizationsLength):
        currentKana = ROMANIZATIONS[Globals.ROMANIZATIONS_HIRA][i]
        if currentKana:
            romanizedKanaWaapuro = romanizedKanaWaapuro.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU][i])

        currentKana = ROMANIZATIONS[Globals.ROMANIZATIONS_KATA][i]
        if currentKana:
            romanizedKanaWaapuro = romanizedKanaWaapuro.replace(currentKana, ROMANIZATIONS[Globals.ROMANIZATIONS_WAPU][i])

    return romanizedKanaWaapuro


def get_frequency_from_dict(kanji):
    freq = '0'
    if kanji == "為る":
        freq = str(Globals.FREQ_DICT["する"])
    elif kanji:
        key = kanji.replace("～", "")
        key = re.sub(r"する$", "", key)
        if key in Globals.FREQ_DICT.keys():
            freq = str(Globals.FREQ_DICT[key])
        else:
            key = getOfficialKana(key)[0]
            if key in Globals.FREQ_DICT.keys():
                freq = str(Globals.FREQ_DICT[key])
    return freq
