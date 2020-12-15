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
    # Transliterations performed according to https://en.wikipedia.org/wiki/Romanization_of_Japanese
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
    transliteratedToHiragana_last = ''
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
            if transliteratedToHiragana_last != transliteratedToHiragana:
                a = 1
            transliteratedToHiragana_last = transliteratedToHiragana

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


# a = getOfficialKana('shibireru')
# b = 1


class Converter:
    def __init__(self):
        self.TYPE_LATIN = 0
        self.TYPE_HIRAGANA = 1
        self.TYPE_KATAKANA = 2

    def get_latin_hiragana_katakana(self, input_word):

        latin_transliteration = ''
        hiragana_transliteration = ''
        katakana_transliteration = ''

        transliterations = [latin_transliteration, hiragana_transliteration, katakana_transliteration]

        character = ''
        added_string_last = ''
        if not input_word == '':
            character = input_word[0]
        else:
            return transliterations

        final_index = 0
        if not input_word == '':
            final_index = len(input_word) - 1

        i = 0
        while i <= final_index:

            character_next = ""
            character_next2 = ""
            character_last = ""

            character = input_word[i]
            if i <= final_index - 1:
                character_next = input_word[i + 1]
            if i <= final_index - 2:
                character_next2 = input_word[i + 2]
            if i > 0:
                character_last = input_word[i - 1]

            # Detecting what the current character represents
            script_detector_output = self.get_phoneme_based_on_letter(i, character, character_next, character_next2, character_last)

            i = int(script_detector_output[0])
            added_string = script_detector_output[1]

            # Getting the current string addition
            char_finder_output = self.get_char_based_on_phoneme(i, added_string, character, character_next, added_string_last)
            added_string_last = added_string

            i = int(char_finder_output[0])
            added_string_latin = char_finder_output[1]
            added_string_hiragana = char_finder_output[2]
            added_string_katakana = char_finder_output[3]

            # Add the string to the translation
            latin_transliteration = latin_transliteration + added_string_latin
            hiragana_transliteration = hiragana_transliteration + added_string_hiragana
            katakana_transliteration = katakana_transliteration + added_string_katakana

            i += 1

        transliterations[self.TYPE_LATIN] = latin_transliteration
        transliterations[self.TYPE_HIRAGANA] = hiragana_transliteration
        transliterations[self.TYPE_KATAKANA] = katakana_transliteration

        return transliterations

    def get_phoneme_based_on_letter(self, i, character, character_next, character_next2, character_last):

        character = str(character).lower()
        character_next = str(character_next).lower()
        character_next2 = str(character_next2).lower()
        character_last = str(character_last).lower()

        added_string = ""
        if character == "あ":
            if character == character_last:
                added_string = "a_double_vowel"
            else:
                if character_next == "ぁ":
                    added_string = "aa"
                    i += 1
                else:
                    added_string = "a"

        elif character == "い":
            if character == character_last:
                added_string = "i_double_vowel"
            else:
                if character_next == "ぃ":
                    added_string = "ii"
                    i += 1
                elif character_next == "ぇ":
                    added_string = "ye"
                    i += 1
                else:
                    added_string = "i"

        elif character == "え":
            if character == character_last:
                added_string = "e_double_vowel"
            else:
                if character_next == "ぇ":
                    added_string = "ee"
                    i += 1
                else:
                    added_string = "e"

        elif character == "お":
            if character == character_last:
                added_string = "o_double_vowel"
            else:
                if character_next == "ぉ":
                    added_string = "oo"
                    i += 1
                else:
                    added_string = "o"

        elif character == "か":
            added_string = "ka"
        elif character == "き":

            if character_next == "ゃ":
                added_string = "kya"
                i += 1
            elif character_next == "ゅ":
                added_string = "kyu"
                i += 1
            elif character_next == "ょ":
                added_string = "kyo"
                i += 1
            else:
                added_string = "ki"

        elif character == "く":
            if character_next == "ゃ":
                added_string = "kwa"
                i += 1
            elif character_next == "ゅ":
                added_string = "*"
                i += 1
            elif character_next == "ょ":
                added_string = "*"
                i += 1
            else:
                added_string = "ku"

        elif character == "け":
            added_string = "ke"
        elif character == "こ":
            added_string = "ko"
        elif character == "が":
            added_string = "ga"
        elif character == "ぎ":

            if character_next == "ゃ":
                added_string = "gya"
                i += 1
            elif character_next == "ゅ":
                added_string = "gyu"
                i += 1
            elif character_next == "ょ":
                added_string = "gyo"
                i += 1
            else:
                added_string = "gi"

        elif character == "ぐ":
            if character_next == "ゃ":
                added_string = "gwa"
                i += 1
            elif character_next == "ゅ":
                added_string = "*"
                i += 1
            elif character_next == "ょ":
                added_string = "*"
                i += 1
            else:
                added_string = "gu"

        elif character == "げ":
            added_string = "ge"
        elif character == "ご":
            added_string = "go"
        elif character == "さ":
            added_string = "sa"
        elif character == "す":
            added_string = "su"
        elif character == "せ":
            added_string = "se"
        elif character == "そ":
            added_string = "so"
        elif character == "ざ":
            added_string = "za"
        elif character == "ず":
            added_string = "zu"
        elif character == "ぜ":
            added_string = "ze"
        elif character == "ぞ":
            added_string = "zo"
        elif character == "し":
            if character_next == "ゃ":
                added_string = "sha"
                i += 1
            elif character_next == "ゅ":
                added_string = "shu"
                i += 1
            elif character_next == "ぇ":
                added_string = "she"
                i += 1
            elif character_next == "ょ":
                added_string = "sho"
                i += 1
            else:
                added_string = "shi"

        elif character == "じ":
            if character_next == "ゃ":
                added_string = "ja"
                i += 1
            elif character_next == "ゅ":
                added_string = "ju"
                i += 1
            elif character_next == "ぇ":
                added_string = "je"
                i += 1
            elif character_next == "ょ":
                added_string = "jo"
                i += 1
            else:
                added_string = "ji"

        elif character == "た":
            added_string = "ta"
        elif character == "て":
            added_string = "te"
        elif character == "と":
            added_string = "to"
        elif character == "だ":
            added_string = "da"
        elif character == "で":
            added_string = "de"
        elif character == "ど":
            added_string = "do"
        elif character == "ち":
            if character_next == "ゃ":
                added_string = "cha"
                i += 1
            elif character_next == "ゅ":
                added_string = "chu"
                i += 1
            elif character_next == "ぇ":
                added_string = "che"
                i += 1
            elif character_next == "ょ":
                added_string = "cho"
                i += 1
            else:
                added_string = "chi"

        elif character == "ぢ":
            if character_next == "ゃ":
                added_string = "dya"
                i += 1
            elif character_next == "ゅ":
                added_string = "dyu"
                i += 1
            elif character_next == "ぇ":
                added_string = "*"
                i += 1
            elif character_next == "ょ":
                added_string = "dyo"
                i += 1
            else:
                added_string = "di"

        elif character == "つ":
            if character_next == "ぁ":
                added_string = "tsa"
                i += 1
            elif character_next == "ぃ":
                added_string = "tsi"
                i += 1
            elif character_next == "ぇ":
                added_string = "tse"
                i += 1
            elif character_next == "ぉ":
                added_string = "tso"
                i += 1
            else:
                added_string = "tsu"

        elif character == "づ":
            if character_next == "ぁ":
                added_string = "*"
                i += 1
            elif character_next == "ゅ":
                added_string = "*"
                i += 1
            elif character_next == "ぃ":
                added_string = "*"
                i += 1
            elif character_next == "ぇ":
                added_string = "*"
                i += 1
            elif character_next == "ぉ":
                added_string = "*"
                i += 1
            else:
                added_string = "du"

        elif character == "な":
            added_string = "na"
        elif character == "ぬ":
            added_string = "nu"
        elif character == "ね":
            added_string = "ne"
        elif character == "の":
            added_string = "no"
        elif character == "ん":
            if character_next == "あ":
                added_string = "n'"
            elif character_next == "え":
                added_string = "n'"
            elif character_next == "い":
                added_string = "n'"
            elif character_next == "お":
                added_string = "n'"
            elif character_next == "う":
                added_string = "n'"
            elif character_next == "や":
                added_string = "n'"
            elif character_next == "よ":
                added_string = "n'"
            elif character_next == "ゆ":
                added_string = "n'"
            else:
                added_string = "n"

        elif character == "に":
            if character_next == "ゃ":
                added_string = "nya"
                i += 1
            elif character_next == "ゅ":
                added_string = "nyu"
                i += 1
            elif character_next == "ぇ":
                added_string = "nye"
                i += 1
            elif character_next == "ょ":
                added_string = "nyo"
                i += 1
            else:
                added_string = "ni"

        elif character == "は":
            added_string = "ha"

        elif character == "ひ":
            if character_next == "ゃ":
                added_string = "hya"
                i += 1
            elif character_next == "ゅ":
                added_string = "hyu"
                i += 1
            elif character_next == "ぇ":
                added_string = "hye"
                i += 1
            elif character_next == "ょ":
                added_string = "hyo"
                i += 1
            else:
                added_string = "hi"

        elif character == "へ":
            added_string = "he"
        elif character == "ほ":
            added_string = "ho"
        elif character == "ば":
            added_string = "ba"
        elif character == "び":
            if character_next == "ゃ":
                added_string = "bya"
                i += 1
            elif character_next == "ゅ":
                added_string = "byu"
                i += 1
            elif character_next == "ぇ":
                added_string = "bye"
                i += 1
            elif character_next == "ょ":
                added_string = "byo"
                i += 1
            else:
                added_string = "bi"

        elif character == "べ":
            added_string = "be"
        elif character == "ぼ":
            added_string = "bo"
        elif character == "ぶ":
            added_string = "bu"
        elif character == "ぱ":
            added_string = "pa"
        elif character == "ぴ":
            if character_next == "ゃ":
                added_string = "pya"
                i += 1
            elif character_next == "ゅ":
                added_string = "pyu"
                i += 1
            elif character_next == "ぇ":
                added_string = "pye"
                i += 1
            elif character_next == "ょ":
                added_string = "pyo"
                i += 1
            else:
                added_string = "pi"

        elif character == "ぺ":
            added_string = "pe"
        elif character == "ぽ":
            added_string = "po"
        elif character == "ぷ":
            added_string = "pu"
        elif character == "ふ":
            if character_next == "ぁ":
                added_string = "fa"
                i += 1
            elif character_next == "ぃ":
                added_string = "fi"
                i += 1
            elif character_next == "ぇ":
                added_string = "fe"
                i += 1
            elif character_next == "ぉ":
                added_string = "fo"
                i += 1
            elif character_next == "ゃ":
                added_string = "fya"
                i += 1
            elif character_next == "ゅ":
                added_string = "fyu"
                i += 1
            elif character_next == "ょ":
                added_string = "fyo"
                i += 1
            else:
                added_string = "fu"

        elif character == "ま":
            added_string = "ma"

        elif character == "み":
            if character_next == "ゃ":
                added_string = "mya"
                i += 1
            elif character_next == "ゅ":
                added_string = "myu"
                i += 1
            elif character_next == "ぇ":
                added_string = "mye"
                i += 1
            elif character_next == "ょ":
                added_string = "myo"
                i += 1
            else:
                added_string = "mi"

        elif character == "む":
            added_string = "mu"
        elif character == "め":
            added_string = "me"
        elif character == "も":
            added_string = "mo"
        elif character == "や":
            added_string = "ya"
        elif character == "ゆ":
            added_string = "yu"
        elif character == "よ":
            added_string = "yo"
        elif character == "ら":
            added_string = "ra"
        elif character == "り":
            if character_next == "ゃ":
                added_string = "rya"
                i += 1
            elif character_next == "ゅ":
                added_string = "ryu"
                i += 1
            elif character_next == "ぇ":
                added_string = "rye"
                i += 1
            elif character_next == "ょ":
                added_string = "ryo"
                i += 1
            else:
                added_string = "ri"

        elif character == "る":
            added_string = "ru"
        elif character == "れ":
            added_string = "re"
        elif character == "ろ":
            added_string = "ro"
        elif character == "わ":
            added_string = "wa"
        elif character == "う":
            if character == character_last:
                added_string = "u_double_vowel"
            else:
                if character_next == "ぃ":
                    added_string = "wi"
                    i += 1
                elif character_next == "ぇ":
                    added_string = "we"
                    i += 1
                else:
                    added_string = "u"

        elif character == "を":
            added_string = "wo"
        elif character == "ゔ":
            if character_next == "ぁ":
                added_string = "va"
                i += 1
            elif character_next == "ぃ":
                added_string = "vi"
                i += 1
            elif character_next == "ぇ":
                added_string = "ve"
                i += 1
            elif character_next == "ぉ":
                added_string = "vo"
                i += 1
            else:
                added_string = "vu"

        elif character == "ゐ":
            added_string = "xwi"
        elif character == "ゑ":
            added_string = "xwe"
        elif character == "っ":
            added_string = "small_tsu"

        elif character == "ア":
            if character == character_last:
                added_string = "a_double_vowel"
            else:
                added_string = "a"

        elif character == "イ":
            if character == character_last:
                added_string = "i_double_vowel"
            elif character_next == "ェ":
                added_string = "ye"
                i += 1
            else:
                added_string = "i"

        elif character == "エ":
            if character == character_last:
                added_string = "e_double_vowel"
            else:
                added_string = "e"

        elif character == "オ":
            if character == character_last:
                added_string = "o_double_vowel"
            else:
                added_string = "o"

        elif character == "カ":
            added_string = "ka"
        elif character == "キ":
            if character_next == "ャ":
                added_string = "kya"
                i += 1
            elif character_next == "ュ":
                added_string = "kyu"
                i += 1
            elif character_next == "ェ":
                added_string = "kye"
                i += 1
            elif character_next == "ョ":
                added_string = "kyo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "kyi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "ki"

        elif character == "ク":
            if character_next == "ァ":
                added_string = "kwa"
                i += 1
            elif character_next == "ュ":
                added_string = "*"
                i += 1
            elif character_next == "ョ":
                added_string = "*"
                i += 1
            else:
                added_string = "ku"

        elif character == "ケ":
            added_string = "ke"
        elif character == "コ":
            added_string = "ko"
        elif character == "ガ":
            added_string = "ga"
        elif character == "ギ":
            if character_next == "ャ":
                added_string = "gya"
                i += 1
            elif character_next == "ュ":
                added_string = "gyu"
                i += 1
            elif character_next == "ェ":
                added_string = "gye"
                i += 1
            elif character_next == "ョ":
                added_string = "gyo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "gyi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "gi"

        elif character == "グ":
            if character_next == "ァ":
                added_string = "gwa"
                i += 1
            elif character_next == "ュ":
                added_string = "*"
                i += 1
            elif character_next == "ョ":
                added_string = "*"
                i += 1
            else:
                added_string = "gu"
        elif character == "ゲ":
            added_string = "ge"
        elif character == "ゴ":
            added_string = "go"
        elif character == "サ":
            added_string = "sa"

        elif character == "ス":
            if character_next == "ゥ":
                added_string = "su"
                i += 1
            else:
                added_string = "su"

        elif character == "セ":
            added_string = "se"
        elif character == "ソ":
            added_string = "so"
        elif character == "ザ":
            added_string = "za"
        elif character == "ズ":
            added_string = "zu"
        elif character == "ゼ":
            added_string = "ze"
        elif character == "ゾ":
            added_string = "zo"
        elif character == "シ":
            if character_next == "ャ":
                added_string = "sha"
                i += 1
            elif character_next == "ュ":
                added_string = "shu"
                i += 1
            elif character_next == "ェ":
                added_string = "she"
                i += 1
            elif character_next == "ョ":
                added_string = "sho"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "shi"

        elif character == "ジ":
            if character_next == "ャ":
                added_string = "ja"
                i += 1
            elif character_next == "ュ":
                added_string = "ju"
                i += 1
            elif character_next == "ェ":
                added_string = "je"
                i += 1
            elif character_next == "ョ":
                added_string = "jo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "ji"

        elif character == "タ":
            added_string = "ta"
        elif character == "テ":
            if character_next == "ィ":
                added_string = "ti"
                i += 1
            elif character_next == "ュ":
                added_string = "tu"
                i += 1
            else:
                added_string = "te"

        elif character == "ト":
            if character_next == "ャ":
                added_string = "ta"
                i += 1
            elif character_next == "ゥ":
                added_string = "tu"
                i += 1
            elif character_next == "ェ":
                added_string = "te"
                i += 1
            elif character_next == "ィ":
                added_string = "ti"
                i += 1
            elif character_next == "ョ":
                added_string = "to"
                i += 1
            else:
                added_string = "to"

        elif character == "ダ":
            added_string = "da"
        elif character == "デ":
            if character_next == "ャ":
                added_string = "*"
                i += 1
            elif character_next == "ュ":
                added_string = "du"
                i += 1
            elif character_next == "ェ":
                added_string = "*"
                i += 1
            elif character_next == "ョ":
                added_string = "*"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "di"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "de"

        elif character == "ド":
            added_string = "do"
        elif character == "チ":
            if character_next == "ャ":
                added_string = "cha"
                i += 1
            elif character_next == "ュ":
                added_string = "chu"
                i += 1
            elif character_next == "ェ":
                added_string = "che"
                i += 1
            elif character_next == "ョ":
                added_string = "cho"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "chi"

        elif character == "ヂ":
            if character_next == "ャ":
                added_string = "dja"
                i += 1
            elif character_next == "ュ":
                added_string = "dju"
                i += 1
            elif character_next == "ェ":
                added_string = "dje"
                i += 1
            elif character_next == "ョ":
                added_string = "djo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "dji"

        elif character == "ツ":
            if character_next == "ャ":
                added_string = "*"
                i += 1
            elif character_next == "ュ":
                added_string = "*"
                i += 1
            elif character_next == "ェ":
                added_string = "tse"
                i += 1
            elif character_next == "ョ":
                added_string = "*"
                i += 1
            elif character_next == "ァ":
                added_string = "tsa"
                i += 1
            elif character_next == "ィ":
                added_string = "tsi"
                i += 1
            elif character_next == "ォ":
                added_string = "tso"
                i += 1
            else:
                added_string = "tsu"

        elif character == "ヅ":
            if character_next == "ャ":
                added_string = "*"
                i += 1
            elif character_next == "ュ":
                added_string = "*"
                i += 1
            elif character_next == "ェ":
                added_string = "dze"
                i += 1
            elif character_next == "ョ":
                added_string = "*"
                i += 1
            elif character_next == "ァ":
                added_string = "dza"
                i += 1
            elif character_next == "ィ":
                added_string = "dzi"
                i += 1
            elif character_next == "ォ":
                added_string = "dzo"
                i += 1
            else:
                added_string = "dzu"

        elif character == "ナ":
            added_string = "na"
        elif character == "ヌ":
            added_string = "nu"
        elif character == "ネ":
            added_string = "ne"
        elif character == "ノ":
            added_string = "no"
        elif character == "ン":
            if character_next == "ア":
                added_string = "n'"
            elif character_next == "エ":
                added_string = "n'"
            elif character_next == "イ":
                added_string = "n'"
            elif character_next == "オ":
                added_string = "n'"
            elif character_next == "ウ":
                added_string = "n'"
            elif character_next == "ヤ":
                added_string = "n'"
            elif character_next == "ヨ":
                added_string = "n'"
            elif character_next == "ュ":
                added_string = "n'"
            else:
                added_string = "n"

        elif character == "ニ":

            if character_next == "ャ":
                added_string = "nya"
                i += 1
            elif character_next == "ュ":
                added_string = "nyu"
                i += 1
            elif character_next == "ェ":
                added_string = "nye"
                i += 1
            elif character_next == "ョ":
                added_string = "nyo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "nyi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "ni"

        elif character == "ハ":
            added_string = "ha"
        elif character == "ヒ":

            if character_next == "ャ":
                added_string = "hya"
                i += 1
            elif character_next == "ュ":
                added_string = "hyu"
                i += 1
            elif character_next == "ェ":
                added_string = "hye"
                i += 1
            elif character_next == "ョ":
                added_string = "hyo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "hyi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "hi"

        elif character == "ヘ":
            added_string = "he"
        elif character == "ホ":
            added_string = "ho"
        elif character == "バ":
            added_string = "ba"
        elif character == "ビ":
            if character_next == "ャ":
                added_string = "bya"
                i += 1
            elif character_next == "ュ":
                added_string = "byu"
                i += 1
            elif character_next == "ェ":
                added_string = "bye"
                i += 1
            elif character_next == "ョ":
                added_string = "byo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "byi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "bi"

        elif character == "ベ":
            added_string = "be"
        elif character == "ボ":
            added_string = "bo"
        elif character == "ブ":
            added_string = "bu"
        elif character == "パ":
            added_string = "pa"
        elif character == "ピ":
            if character_next == "ャ":
                added_string = "pya"
                i += 1
            elif character_next == "ュ":
                added_string = "pyu"
                i += 1
            elif character_next == "ェ":
                added_string = "pye"
                i += 1
            elif character_next == "ョ":
                added_string = "pyo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "pyi"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "pi"

        elif character == "ペ":
            added_string = "pe"
        elif character == "ポ":
            added_string = "po"
        elif character == "プ":
            added_string = "pu"
        elif character == "フ":

            if character_next == "ャ":
                added_string = "fya"
                i += 1
            elif character_next == "ュ":
                added_string = "fyu"
                i += 1
            elif character_next == "ェ":
                added_string = "fe"
                i += 1
            elif character_next == "ョ":
                added_string = "fyo"
                i += 1
            elif character_next == "ァ":
                added_string = "fa"
                i += 1
            elif character_next == "ィ":
                added_string = "fi"
                i += 1
            elif character_next == "ォ":
                added_string = "fo"
                i += 1
            else:
                added_string = "fu"

        elif character == "マ":
            added_string = "ma"
        elif character == "ミ":
            if character_next == "ャ":
                added_string = "mya"
                i += 1
            elif character_next == "ュ":
                added_string = "myu"
                i += 1
            elif character_next == "ェ":
                added_string = "mye"
                i += 1
            elif character_next == "ョ":
                added_string = "myo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "mi"

        elif character == "ム":
            added_string = "mu"
        elif character == "メ":
            added_string = "me"
        elif character == "モ":
            added_string = "mo"
        elif character == "ヤ":
            added_string = "ya"
        elif character == "ユ":
            added_string = "yu"
        elif character == "ヨ":
            added_string = "yo"
        elif character == "ラ":
            added_string = "ra"
        elif character == "リ":
            if character_next == "ャ":
                added_string = "rya"
                i += 1
            elif character_next == "ュ":
                added_string = "ryu"
                i += 1
            elif character_next == "ェ":
                added_string = "rye"
                i += 1
            elif character_next == "ョ":
                added_string = "ryo"
                i += 1
            elif character_next == "ァ":
                added_string = "*"
                i += 1
            elif character_next == "ィ":
                added_string = "*"
                i += 1
            elif character_next == "ォ":
                added_string = "*"
                i += 1
            else:
                added_string = "ri"

        elif character == "ル":
            added_string = "ru"
        elif character == "レ":
            added_string = "re"
        elif character == "ロ":
            added_string = "ro"
        elif character == "ワ":
            added_string = "wa"
        elif character == "ウ":
            if character == character_last:
                added_string = "u_double_vowel"
            else:
                if character_next == "ャ":
                    added_string = "*"
                    i += 1
                elif character_next == "ュ":
                    added_string = "*"
                    i += 1
                elif character_next == "ェ":
                    added_string = "we"
                    i += 1
                elif character_next == "ョ":
                    added_string = "*"
                    i += 1
                elif character_next == "ァ":
                    added_string = "*"
                    i += 1
                elif character_next == "ィ":
                    added_string = "wi"
                    i += 1
                elif character_next == "ォ":
                    added_string = "vo"
                    i += 1
                else:
                    added_string = "u"

        elif character == "ヲ":
            added_string = "wo"
        elif character == "ヴ":
            if character_next == "ァ":
                added_string = "va"
                i += 1
            elif character_next == "ィ":
                added_string = "vi"
                i += 1
            elif character_next == "ェ":
                added_string = "ve"
                i += 1
            elif character_next == "ォ":
                added_string = "vo"
                i += 1
            else:
                added_string = "vu"

        elif character == "ヷ":
            added_string = "va"
        elif character == "ヸ":
            added_string = "vi"
        elif character == "ヹ":
            added_string = "ve"
        elif character == "ヺ":
            added_string = "vo"
        elif character == "ヰ":
            added_string = "xwi"
        elif character == "ヱ":
            added_string = "xwe"
        elif character == "ッ":
            added_string = "small_tsu"

        elif character == "ー":
            added_string = "katakana_repeat_bar"

        elif character == "a":
            if character == character_last:
                added_string = "a_double_vowel"
            else:
                added_string = "a"

        elif character == "b":
            if character_next == "a":
                added_string = "ba"
                i += 1
            elif character_next == "e":
                added_string = "be"
                i += 1
            elif character_next == "i":
                added_string = "bi"
                i += 1
            elif character_next == "o":
                added_string = "bo"
                i += 1
            elif character_next == "u":
                added_string = "bu"
                i += 1
            elif character_next == "y":
                if character_next2 == "a":
                    added_string = "bya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "bye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "byi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "byo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "byu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "b":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "c":
            if character_next == "h":
                if character_next2 == "a":
                    added_string = "cha"
                    i += 2
                elif character_next2 == "e":
                    added_string = "che"
                    i += 2
                elif character_next2 == "i":
                    added_string = "chi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "cho"
                    i += 2
                elif character_next2 == "u":
                    added_string = "chu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "c":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "d":

            if character_next == "a":
                added_string = "da"
                i += 1
            elif character_next == "e":
                added_string = "de"
                i += 1
            elif character_next == "i":
                added_string = "di"
                i += 1
            elif character_next == "o":
                added_string = "do"
                i += 1
            elif character_next == "u":
                added_string = "du"
                i += 1
            elif character_next == "d":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "e":
            if character == character_last:
                added_string = "e_double_vowel"
            else:
                added_string = "e"

        elif character == "f":
            if character_next == "a":
                added_string = "fa"
                i += 1
            elif character_next == "e":
                added_string = "fe"
                i += 1
            elif character_next == "i":
                added_string = "fi"
                i += 1
            elif character_next == "o":
                added_string = "fo"
                i += 1
            elif character_next == "u":
                added_string = "fu"
                i += 1
            elif character_next == "y":
                if character_next2 == "a":
                    added_string = "fya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "fye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "fyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "fyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "fyu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "f":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "g":

            if character_next == "a":
                added_string = "ga"
                i += 1
            elif character_next == "e":
                added_string = "ge"
                i += 1
            elif character_next == "i":
                added_string = "gi"
                i += 1
            elif character_next == "o":
                added_string = "go"
                i += 1
            elif character_next == "u":
                added_string = "gu"
                i += 1
            elif character_next == "y":
                if character_next2 == "a":
                    added_string = "gya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "gye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "gyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "gyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "gyu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "g":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "h":
            if character_next == "a":
                added_string = "ha"
                i += 1
            elif character_next == "e":
                added_string = "he"
                i += 1
            elif character_next == "i":
                added_string = "hi"
                i += 1
            elif character_next == "o":
                added_string = "ho"
                i += 1
            elif character_next == "u":
                added_string = "hu"
                i += 1
            elif character_next == "y":
                if character_next2 == "a":
                    added_string = "hya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "hye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "hyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "hyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "hyu"
                    i += 2
                else:
                    added_string = "*"

            else:
                added_string = "*"

        elif character == "i":
            if character == character_last:
                added_string = "i_double_vowel"
            else:
                added_string = "i"

        elif character == "j":
            if character_next == "a":
                added_string = "ja"
                i += 1
            elif character_next == "e":
                added_string = "je"
                i += 1
            elif character_next == "i":
                added_string = "ji"
                i += 1
            elif character_next == "o":
                added_string = "jo"
                i += 1
            elif character_next == "u":
                added_string = "ju"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "jya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "jye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "jyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "jyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "jyu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "j":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "k":

            if character_next == "a":
                added_string = "ka"
                i += 1
            elif character_next == "e":
                added_string = "ke"
                i += 1
            elif character_next == "i":
                added_string = "ki"
                i += 1
            elif character_next == "o":
                added_string = "ko"
                i += 1
            elif character_next == "u":
                added_string = "ku"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "kya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "kye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "kyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "kyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "kyu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "k":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "l":
            added_string = "*"
        elif character == "m":

            if character_next == "a":
                added_string = "ma"
                i += 1
            elif character_next == "e":
                added_string = "me"
                i += 1
            elif character_next == "i":
                added_string = "mi"
                i += 1
            elif character_next == "o":
                added_string = "mo"
                i += 1
            elif character_next == "u":
                added_string = "mu"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "mya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "mye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "myi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "myo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "myu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "m":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "n":

            if character_next == "'":
                added_string = "n'"
                i += 1
            elif character_next == "a":
                added_string = "na"
                i += 1
            elif character_next == "e":
                added_string = "ne"
                i += 1
            elif character_next == "i":
                added_string = "ni"
                i += 1
            elif character_next == "o":
                added_string = "no"
                i += 1
            elif character_next == "u":
                added_string = "nu"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "nya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "nye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "nyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "nyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "nyu"
                    i += 2
                else:
                    added_string = "*"
                    i += 1

            else:
                added_string = "n"

        elif character == "o":
            if character == character_last:
                added_string = "o_double_vowel"
            else:
                added_string = "o"

        elif character == "p":

            if character_next == "a":
                added_string = "pa"
                i += 1
            elif character_next == "e":
                added_string = "pe"
                i += 1
            elif character_next == "i":
                added_string = "pi"
                i += 1
            elif character_next == "o":
                added_string = "po"
                i += 1
            elif character_next == "u":
                added_string = "pu"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "pya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "pye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "pyi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "pyo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "pyu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "p":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "q":
            added_string = "*"
        elif character == "r":

            if character_next == "a":
                added_string = "ra"
                i += 1
            elif character_next == "e":
                added_string = "re"
                i += 1
            elif character_next == "i":
                added_string = "ri"
                i += 1
            elif character_next == "o":
                added_string = "ro"
                i += 1
            elif character_next == "u":
                added_string = "ru"
                i += 1
            elif character_next == "y":

                if character_next2 == "a":
                    added_string = "rya"
                    i += 2
                elif character_next2 == "e":
                    added_string = "rye"
                    i += 2
                elif character_next2 == "i":
                    added_string = "ryi"
                    i += 2
                elif character_next2 == "o":
                    added_string = "ryo"
                    i += 2
                elif character_next2 == "u":
                    added_string = "ryu"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "r":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "s":

            if character_next == "a":
                added_string = "sa"
                i += 1
            elif character_next == "e":
                added_string = "se"
                i += 1
            elif character_next == "o":
                added_string = "so"
                i += 1
            elif character_next == "u":
                added_string = "su"
                i += 1
            elif character_next == "h":

                if character_next2 == "i":
                    added_string = "shi"
                    i += 2
                elif character_next2 == "a":
                    added_string = "sha"
                    i += 2
                elif character_next2 == "o":
                    added_string = "sho"
                    i += 2
                elif character_next2 == "u":
                    added_string = "shu"
                    i += 2
                elif character_next2 == "e":
                    added_string = "she"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "s":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "t":

            if character_next == "a":
                added_string = "ta"
                i += 1
            elif character_next == "e":
                added_string = "te"
                i += 1
            elif character_next == "i":
                added_string = "ti"
                i += 1
            elif character_next == "o":
                added_string = "to"
                i += 1
            elif character_next == "u":
                added_string = "tu"
                i += 1
            elif character_next == "s":

                if character_next2 == "a":
                    added_string = "tsa"
                    i += 2
                elif character_next2 == "i":
                    added_string = "tsi"
                    i += 2
                elif character_next2 == "u":
                    added_string = "tsu"
                    i += 2
                elif character_next2 == "e":
                    added_string = "tse"
                    i += 2
                elif character_next2 == "o":
                    added_string = "tso"
                    i += 2
                else:
                    added_string = "*"

            elif character_next == "t":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "u":
            if character == character_last:
                added_string = "u_double_vowel"
            else:
                added_string = "u"

        elif character == "v":

            if character_next == "a":
                added_string = "va"
                i += 1
            elif character_next == "e":
                added_string = "ve"
                i += 1
            elif character_next == "i":
                added_string = "vi"
                i += 1
            elif character_next == "o":
                added_string = "vo"
                i += 1
            elif character_next == "u":
                added_string = "vu"
                i += 1
            elif character_next == "v":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "w":

            if character_next == "a":
                added_string = "wa"
                i += 1
            elif character_next == "e":
                added_string = "we"
                i += 1
            elif character_next == "i":
                added_string = "wi"
                i += 1
            elif character_next == "o":
                added_string = "wo"
                i += 1
            elif character_next == "u":
                added_string = "wu"
                i += 1
            elif character_next == "w":
                added_string = "small_tsu"
            else:
                added_string = "*"

        elif character == "x":
            added_string = "*"
        elif character == "y":

            if character_next == "a":
                added_string = "ya"
                i += 1
            elif character_next == "e":
                added_string = "ye"
                i += 1
            elif character_next == "o":
                added_string = "yo"
                i += 1
            elif character_next == "u":
                added_string = "yu"
                i += 1
            else:
                added_string = "*"

        elif character == "z":

            if character_next == "a":
                added_string = "za"
                i += 1
            elif character_next == "e":
                added_string = "ze"
                i += 1
            elif character_next == "o":
                added_string = "zo"
                i += 1
            elif character_next == "u":
                added_string = "zu"
                i += 1
            elif character_next == "z":
                added_string = "small_tsu"
            else:
                added_string = "*"

        else:
            added_string = "original"

        output = [str(i), added_string]

        return output

    def get_char_based_on_phoneme(self, i, added_string, character, character_next, added_string_last):

        added_string_latin = ""
        added_string_hiragana = ""
        added_string_katakana = ""

        if added_string == "a":
            added_string_latin = "a"
            added_string_hiragana = "あ"
            added_string_katakana = "ア"
        elif added_string == "ba":
            added_string_latin = "ba"
            added_string_hiragana = "ば"
            added_string_katakana = "バ"
        elif added_string == "bi":
            added_string_latin = "bi"
            added_string_hiragana = "び"
            added_string_katakana = "ビ"
        elif added_string == "bu":
            added_string_latin = "bu"
            added_string_hiragana = "ぶ"
            added_string_katakana = "ブ"
        elif added_string == "be":
            added_string_latin = "be"
            added_string_hiragana = "べ"
            added_string_katakana = "ベ"
        elif added_string == "bo":
            added_string_latin = "bo"
            added_string_hiragana = "ぼ"
            added_string_katakana = "ボ"
        elif added_string == "bya":
            added_string_latin = "bya"
            added_string_hiragana = "びゃ"
            added_string_katakana = "ビャ"
        elif added_string == "byu":
            added_string_latin = "byu"
            added_string_hiragana = "びゅ"
            added_string_katakana = "ビュ"
        elif added_string == "byi":
            added_string_latin = "byi"
            added_string_hiragana = "びぃ"
            added_string_katakana = "ビィ"
        elif added_string == "bye":
            added_string_latin = "bye"
            added_string_hiragana = "びぇ"
            added_string_katakana = "ビェ"
        elif added_string == "byo":
            added_string_latin = "byo"
            added_string_hiragana = "びょ"
            added_string_katakana = "ビョ"
        elif added_string == "cha":
            added_string_latin = "cha"
            added_string_hiragana = "ちゃ"
            added_string_katakana = "チャ"
        elif added_string == "chi":
            added_string_latin = "chi"
            added_string_hiragana = "ち"
            added_string_katakana = "チ"
        elif added_string == "chu":
            added_string_latin = "chu"
            added_string_hiragana = "ちゅ"
            added_string_katakana = "チュ"
        elif added_string == "che":
            added_string_latin = "che"
            added_string_hiragana = "ちぇ"
            added_string_katakana = "チェ"
        elif added_string == "cho":
            added_string_latin = "cho"
            added_string_hiragana = "ちょ"
            added_string_katakana = "チョ"
        elif added_string == "da":
            added_string_latin = "da"
            added_string_hiragana = "だ"
            added_string_katakana = "ダ"
        elif added_string == "di":
            added_string_latin = "di"
            added_string_hiragana = "ぢ"
            added_string_katakana = "ヂ"
        elif added_string == "du":
            added_string_latin = "du"
            added_string_hiragana = "づ"
            added_string_katakana = "ヅ"
        elif added_string == "de":
            added_string_latin = "de"
            added_string_hiragana = "で"
            added_string_katakana = "デ"
        elif added_string == "do":
            added_string_latin = "do"
            added_string_hiragana = "ど"
            added_string_katakana = "ド"
        elif added_string == "dja":
            added_string_latin = "dja"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂャ"
        elif added_string == "dji":
            added_string_latin = "dji"
            added_string_hiragana = "ぢ"
            added_string_katakana = "ヂ"
        elif added_string == "dju":
            added_string_latin = "dju"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂュ"
        elif added_string == "dje":
            added_string_latin = "dje"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂェ"
        elif added_string == "djo":
            added_string_latin = "djo"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂョ"
        elif added_string == "dya":
            added_string_latin = "dya"
            added_string_hiragana = "ぢゃ"
            added_string_katakana = "ヂァ"
        elif added_string == "dyi":
            added_string_latin = "dyi"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂィ"
        elif added_string == "dyu":
            added_string_latin = "dyu"
            added_string_hiragana = "ぢゅ"
            added_string_katakana = "ヂュ"
        elif added_string == "dye":
            added_string_latin = "dye"
            added_string_hiragana = "＊"
            added_string_katakana = "ヂェ"
        elif added_string == "dyo":
            added_string_latin = "dyo"
            added_string_hiragana = "ぢょ"
            added_string_katakana = "ヂォ"
        elif added_string == "dza":
            added_string_latin = "dza"
            added_string_hiragana = "＊"
            added_string_katakana = "ヅァ"
        elif added_string == "dzi":
            added_string_latin = "dzi"
            added_string_hiragana = "＊"
            added_string_katakana = "ヅィ"
        elif added_string == "dzu":
            added_string_latin = "dzu"
            added_string_hiragana = "＊"
            added_string_katakana = "ヅ"
        elif added_string == "dze":
            added_string_latin = "dze"
            added_string_hiragana = "＊"
            added_string_katakana = "ヅェ"
        elif added_string == "dzo":
            added_string_latin = "dzo"
            added_string_hiragana = "＊"
            added_string_katakana = "ヅォ"
        elif added_string == "e":
            added_string_latin = "e"
            added_string_hiragana = "え"
            added_string_katakana = "エ"
        elif added_string == "fa":
            added_string_latin = "fa"
            added_string_hiragana = "ふぁ"
            added_string_katakana = "ファ"
        elif added_string == "fi":
            added_string_latin = "fi"
            added_string_hiragana = "ふぃ"
            added_string_katakana = "フィ"
        elif added_string == "fu":
            added_string_latin = "fu"
            added_string_hiragana = "ふ"
            added_string_katakana = "フ"
        elif added_string == "fe":
            added_string_latin = "fe"
            added_string_hiragana = "ふぇ"
            added_string_katakana = "フェ"
        elif added_string == "fo":
            added_string_latin = "fo"
            added_string_hiragana = "ふぉ"
            added_string_katakana = "フォ"
        elif added_string == "fya":
            added_string_latin = "fya"
            added_string_hiragana = "ふゃ"
            added_string_katakana = "フャ"
        elif added_string == "fye":
            added_string_latin = "fye"
            added_string_hiragana = "ふぇ"
            added_string_katakana = "フェ"
        elif added_string == "fyi":
            added_string_latin = "fyi"
            added_string_hiragana = "ふぃ"
            added_string_katakana = "フィ"
        elif added_string == "fyu":
            added_string_latin = "fyu"
            added_string_hiragana = "ふゅ"
            added_string_katakana = "フュ"
        elif added_string == "fyo":
            added_string_latin = "fyo"
            added_string_hiragana = "ふょ"
            added_string_katakana = "フョ"
        elif added_string == "ga":
            added_string_latin = "ga"
            added_string_hiragana = "が"
            added_string_katakana = "ガ"
        elif added_string == "gi":
            added_string_latin = "gi"
            added_string_hiragana = "ぎ"
            added_string_katakana = "ギ"
        elif added_string == "gu":
            added_string_latin = "gu"
            added_string_hiragana = "ぐ"
            added_string_katakana = "グ"
        elif added_string == "ge":
            added_string_latin = "ge"
            added_string_hiragana = "げ"
            added_string_katakana = "ゲ"
        elif added_string == "go":
            added_string_latin = "go"
            added_string_hiragana = "ご"
            added_string_katakana = "ゴ"
        elif added_string == "gwa":
            added_string_latin = "gwa"
            added_string_hiragana = "ぐゎ"
            added_string_katakana = "グァ"
        elif added_string == "gya":
            added_string_latin = "gya"
            added_string_hiragana = "ぎゃ"
            added_string_katakana = "ギャ"
        elif added_string == "gye":
            added_string_latin = "gye"
            added_string_hiragana = "ぎぇ"
            added_string_katakana = "ギェ"
        elif added_string == "gyi":
            added_string_latin = "gyi"
            added_string_hiragana = "ぎぃ"
            added_string_katakana = "ギィ"
        elif added_string == "gyu":
            added_string_latin = "gyu"
            added_string_hiragana = "ぎゅ"
            added_string_katakana = "ギュ"
        elif added_string == "gyo":
            added_string_latin = "gyo"
            added_string_hiragana = "ぎょ"
            added_string_katakana = "ギョ"
        elif added_string == "ha":
            added_string_latin = "ha"
            added_string_hiragana = "は"
            added_string_katakana = "ハ"
        elif added_string == "hi":
            added_string_latin = "hi"
            added_string_hiragana = "ひ"
            added_string_katakana = "ヒ"
        elif added_string == "hu":
            added_string_latin = "hu"
            added_string_hiragana = "ふ"
            added_string_katakana = "フ"
        elif added_string == "he":
            added_string_latin = "he"
            added_string_hiragana = "へ"
            added_string_katakana = "ヘ"
        elif added_string == "ho":
            added_string_latin = "ho"
            added_string_hiragana = "ほ"
            added_string_katakana = "ホ"
        elif added_string == "hya":
            added_string_latin = "hya"
            added_string_hiragana = "ひゃ"
            added_string_katakana = "ヒャ"
        elif added_string == "hyi":
            added_string_latin = "hyi"
            added_string_hiragana = "ひぃ"
            added_string_katakana = "ヒィ"
        elif added_string == "hyu":
            added_string_latin = "hyu"
            added_string_hiragana = "ひゅ"
            added_string_katakana = "ヒュ"
        elif added_string == "hye":
            added_string_latin = "hye"
            added_string_hiragana = "ひぇ"
            added_string_katakana = "ヒェ"
        elif added_string == "hyo":
            added_string_latin = "hyo"
            added_string_hiragana = "ひょ"
            added_string_katakana = "ヒョ"
        elif added_string == "i":
            added_string_latin = "i"
            added_string_hiragana = "い"
            added_string_katakana = "イ"
        elif added_string == "ja":
            added_string_latin = "ja"
            added_string_hiragana = "じゃ"
            added_string_katakana = "ジャ"
        elif added_string == "ji":
            added_string_latin = "ji"
            added_string_hiragana = "じ"
            added_string_katakana = "ジ"
        elif added_string == "ju":
            added_string_latin = "ju"
            added_string_hiragana = "じゅ"
            added_string_katakana = "ジュ"
        elif added_string == "je":
            added_string_latin = "je"
            added_string_hiragana = "じぇ"
            added_string_katakana = "ジェ"
        elif added_string == "jo":
            added_string_latin = "jo"
            added_string_hiragana = "じょ"
            added_string_katakana = "ジョ"
        elif added_string == "jya":
            added_string_latin = "jya"
            added_string_hiragana = "じゃ"
            added_string_katakana = "ジャ"
        elif added_string == "jye":
            added_string_latin = "jye"
            added_string_hiragana = "じぇ"
            added_string_katakana = "ジェ"
        elif added_string == "jyi":
            added_string_latin = "jyi"
            added_string_hiragana = "じぃ"
            added_string_katakana = "ジィ"
        elif added_string == "jyu":
            added_string_latin = "jyu"
            added_string_hiragana = "じゅ"
            added_string_katakana = "ジュ"
        elif added_string == "jyo":
            added_string_latin = "jyo"
            added_string_hiragana = "じょ"
            added_string_katakana = "ジョ"
        elif added_string == "ka":
            added_string_latin = "ka"
            added_string_hiragana = "か"
            added_string_katakana = "カ"
        elif added_string == "ki":
            added_string_latin = "ki"
            added_string_hiragana = "き"
            added_string_katakana = "キ"
        elif added_string == "ku":
            added_string_latin = "ku"
            added_string_hiragana = "く"
            added_string_katakana = "ク"
        elif added_string == "ke":
            added_string_latin = "ke"
            added_string_hiragana = "け"
            added_string_katakana = "ケ"
        elif added_string == "ko":
            added_string_latin = "ko"
            added_string_hiragana = "こ"
            added_string_katakana = "コ"
        elif added_string == "kwa":
            added_string_latin = "kwa"
            added_string_hiragana = "くゎ"
            added_string_katakana = "クァ"
        elif added_string == "kya":
            added_string_latin = "kya"
            added_string_hiragana = "きゃ"
            added_string_katakana = "キャ"
        elif added_string == "kye":
            added_string_latin = "kye"
            added_string_hiragana = "きぇ"
            added_string_katakana = "キェ"
        elif added_string == "kyi":
            added_string_latin = "kyi"
            added_string_hiragana = "きぃ"
            added_string_katakana = "キィ"
        elif added_string == "kyu":
            added_string_latin = "kyu"
            added_string_hiragana = "きゅ"
            added_string_katakana = "キュ"
        elif added_string == "kyo":
            added_string_latin = "kyo"
            added_string_hiragana = "きょ"
            added_string_katakana = "キョ"
        elif added_string == "ma":
            added_string_latin = "ma"
            added_string_hiragana = "ま"
            added_string_katakana = "マ"
        elif added_string == "mi":
            added_string_latin = "mi"
            added_string_hiragana = "み"
            added_string_katakana = "ミ"
        elif added_string == "mu":
            added_string_latin = "mu"
            added_string_hiragana = "む"
            added_string_katakana = "ム"
        elif added_string == "me":
            added_string_latin = "me"
            added_string_hiragana = "め"
            added_string_katakana = "メ"
        elif added_string == "mo":
            added_string_latin = "mo"
            added_string_hiragana = "も"
            added_string_katakana = "モ"
        elif added_string == "mya":
            added_string_latin = "mya"
            added_string_hiragana = "みゃ"
            added_string_katakana = "ミャ"
        elif added_string == "myu":
            added_string_latin = "myu"
            added_string_hiragana = "みゅ"
            added_string_katakana = "ミュ"
        elif added_string == "myi":
            added_string_latin = "myi"
            added_string_hiragana = "みぃ"
            added_string_katakana = "ミィ"
        elif added_string == "mye":
            added_string_latin = "mye"
            added_string_hiragana = "みぇ"
            added_string_katakana = "ミェ"
        elif added_string == "myo":
            added_string_latin = "myo"
            added_string_hiragana = "みょ"
            added_string_katakana = "ミョ"
        elif added_string == "n":
            added_string_latin = "n"
            added_string_hiragana = "ん"
            added_string_katakana = "ン"
        elif added_string == "n'":
            added_string_latin = "n'"
            added_string_hiragana = "ん"
            added_string_katakana = "ン"
        elif added_string == "na":
            added_string_latin = "na"
            added_string_hiragana = "な"
            added_string_katakana = "ナ"
        elif added_string == "ni":
            added_string_latin = "ni"
            added_string_hiragana = "に"
            added_string_katakana = "ニ"
        elif added_string == "nu":
            added_string_latin = "nu"
            added_string_hiragana = "ぬ"
            added_string_katakana = "ヌ"
        elif added_string == "ne":
            added_string_latin = "ne"
            added_string_hiragana = "ね"
            added_string_katakana = "ネ"
        elif added_string == "no":
            added_string_latin = "no"
            added_string_hiragana = "の"
            added_string_katakana = "ノ"
        elif added_string == "nya":
            added_string_latin = "nya"
            added_string_hiragana = "にゃ"
            added_string_katakana = "ニャ"
        elif added_string == "nyu":
            added_string_latin = "nyu"
            added_string_hiragana = "にゅ"
            added_string_katakana = "ニュ"
        elif added_string == "nye":
            added_string_latin = "nye"
            added_string_hiragana = "にぇ"
            added_string_katakana = "ニェ"
        elif added_string == "nyi":
            added_string_latin = "nyi"
            added_string_hiragana = "にぃ"
            added_string_katakana = "ニィ"
        elif added_string == "nyo":
            added_string_latin = "nyo"
            added_string_hiragana = "にょ"
            added_string_katakana = "ニョ"
        elif added_string == "o":
            added_string_latin = "o"
            added_string_hiragana = "お"
            added_string_katakana = "オ"
        elif added_string == "pa":
            added_string_latin = "pa"
            added_string_hiragana = "ぱ"
            added_string_katakana = "パ"
        elif added_string == "pi":
            added_string_latin = "pi"
            added_string_hiragana = "ぴ"
            added_string_katakana = "ビ"
        elif added_string == "pu":
            added_string_latin = "pu"
            added_string_hiragana = "ぷ"
            added_string_katakana = "プ"
        elif added_string == "pe":
            added_string_latin = "pe"
            added_string_hiragana = "ぺ"
            added_string_katakana = "ペ"
        elif added_string == "po":
            added_string_latin = "po"
            added_string_hiragana = "ぽ"
            added_string_katakana = "ポ"
        elif added_string == "pya":
            added_string_latin = "pya"
            added_string_hiragana = "ぴゃ"
            added_string_katakana = "ピャ"
        elif added_string == "pyu":
            added_string_latin = "pyu"
            added_string_hiragana = "ぴゅ"
            added_string_katakana = "ピュ"
        elif added_string == "pyi":
            added_string_latin = "pyi"
            added_string_hiragana = "ぴぃ"
            added_string_katakana = "ピィ"
        elif added_string == "pye":
            added_string_latin = "pye"
            added_string_hiragana = "ぴぇ"
            added_string_katakana = "ピェ"
        elif added_string == "pyo":
            added_string_latin = "pyo"
            added_string_hiragana = "ぴょ"
            added_string_katakana = "ピョ"
        elif added_string == "ra":
            added_string_latin = "ra"
            added_string_hiragana = "ら"
            added_string_katakana = "ラ"
        elif added_string == "ri":
            added_string_latin = "ri"
            added_string_hiragana = "り"
            added_string_katakana = "リ"
        elif added_string == "ru":
            added_string_latin = "ru"
            added_string_hiragana = "る"
            added_string_katakana = "ル"
        elif added_string == "re":
            added_string_latin = "re"
            added_string_hiragana = "れ"
            added_string_katakana = "レ"
        elif added_string == "ro":
            added_string_latin = "ro"
            added_string_hiragana = "ろ"
            added_string_katakana = "ロ"
        elif added_string == "rya":
            added_string_latin = "rya"
            added_string_hiragana = "りゃ"
            added_string_katakana = "リャ"
        elif added_string == "ryu":
            added_string_latin = "ryu"
            added_string_hiragana = "りゅ"
            added_string_katakana = "リュ"
        elif added_string == "ryi":
            added_string_latin = "ryi"
            added_string_hiragana = "りぃ"
            added_string_katakana = "リィ"
        elif added_string == "rye":
            added_string_latin = "rye"
            added_string_hiragana = "りぇ"
            added_string_katakana = "リェ"
        elif added_string == "ryo":
            added_string_latin = "ryo"
            added_string_hiragana = "りょ"
            added_string_katakana = "リョ"
        elif added_string == "sa":
            added_string_latin = "sa"
            added_string_hiragana = "さ"
            added_string_katakana = "サ"
        elif added_string == "si":
            added_string_latin = "si"
            added_string_hiragana = "＊"
            added_string_katakana = "＊"
        elif added_string == "su":
            added_string_latin = "su"
            added_string_hiragana = "す"
            added_string_katakana = "ス"
        elif added_string == "se":
            added_string_latin = "se"
            added_string_hiragana = "せ"
            added_string_katakana = "セ"
        elif added_string == "so":
            added_string_latin = "so"
            added_string_hiragana = "そ"
            added_string_katakana = "ソ"
        elif added_string == "sha":
            added_string_latin = "sha"
            added_string_hiragana = "しゃ"
            added_string_katakana = "シャ"
        elif added_string == "shi":
            added_string_latin = "shi"
            added_string_hiragana = "し"
            added_string_katakana = "シ"
        elif added_string == "shu":
            added_string_latin = "shu"
            added_string_hiragana = "しゅ"
            added_string_katakana = "シュ"
        elif added_string == "she":
            added_string_latin = "she"
            added_string_hiragana = "しぇ"
            added_string_katakana = "シェ"
        elif added_string == "sho":
            added_string_latin = "sho"
            added_string_hiragana = "しょ"
            added_string_katakana = "ショ"
        elif added_string == "sya":
            added_string_latin = "sya"
            added_string_hiragana = "＊"
            added_string_katakana = "＊"
        elif added_string == "syu":
            added_string_latin = "syu"
            added_string_hiragana = "＊"
            added_string_katakana = "＊"
        elif added_string == "syo":
            added_string_latin = "syo"
            added_string_hiragana = "＊"
            added_string_katakana = "＊"
        elif added_string == "ta":
            added_string_latin = "ta"
            added_string_hiragana = "た"
            added_string_katakana = "タ"
        elif added_string == "ti":
            added_string_latin = "ti"
            added_string_hiragana = "＊"
            added_string_katakana = "ティ"
        elif added_string == "tu":
            added_string_latin = "tu"
            added_string_hiragana = "＊"
            added_string_katakana = "テュ"
        elif added_string == "te":
            added_string_latin = "te"
            added_string_hiragana = "て"
            added_string_katakana = "テ"
        elif added_string == "to":
            added_string_latin = "to"
            added_string_hiragana = "と"
            added_string_katakana = "ト"
        elif added_string == "tsu":
            added_string_latin = "tsu"
            added_string_hiragana = "つ"
            added_string_katakana = "ツ"
        elif added_string == "u":
            added_string_latin = "u"
            added_string_hiragana = "う"
            added_string_katakana = "ウ"
        elif added_string == "va":
            added_string_latin = "va"
            added_string_hiragana = "ヴぁ"
            added_string_katakana = "ヴァ"
        elif added_string == "vi":
            added_string_latin = "vi"
            added_string_hiragana = "ヴぃ"
            added_string_katakana = "ヴィ"
        elif added_string == "vu":
            added_string_latin = "vu"
            added_string_hiragana = "ヴ"
            added_string_katakana = "ヴ"
        elif added_string == "ve":
            added_string_latin = "ve"
            added_string_hiragana = "ヴぇ"
            added_string_katakana = "ヴェ"
        elif added_string == "vo":
            added_string_latin = "vo"
            added_string_hiragana = "ヴぉ"
            added_string_katakana = "ヴォ"
        elif added_string == "wa":
            added_string_latin = "wa"
            added_string_hiragana = "わ"
            added_string_katakana = "ワ"
        elif added_string == "wi":
            added_string_latin = "wi"
            added_string_hiragana = "うぃ"
            added_string_katakana = "ウィ"
        elif added_string == "wu":
            added_string_latin = "wu"
            added_string_hiragana = "う"
            added_string_katakana = "ウ"
        elif added_string == "we":
            added_string_latin = "we"
            added_string_hiragana = "うぇ"
            added_string_katakana = "ウェ"
        elif added_string == "wo":
            added_string_latin = "wo"
            added_string_hiragana = "を"
            added_string_katakana = "ヲ"
        elif added_string == "ya":
            added_string_latin = "ya"
            added_string_hiragana = "や"
            added_string_katakana = "ヤ"
        elif added_string == "yu":
            added_string_latin = "yu"
            added_string_hiragana = "ゆ"
            added_string_katakana = "ユ"
        elif added_string == "ye":
            added_string_latin = "ye"
            added_string_hiragana = "いぇ"
            added_string_katakana = "イェ"
        elif added_string == "yo":
            added_string_latin = "yo"
            added_string_hiragana = "よ"
            added_string_katakana = "ヨ"
        elif added_string == "za":
            added_string_latin = "za"
            added_string_hiragana = "ざ"
            added_string_katakana = "ザ"
        elif added_string == "zu":
            added_string_latin = "zu"
            added_string_hiragana = "ず"
            added_string_katakana = "ズ"
        elif added_string == "ze":
            added_string_latin = "ze"
            added_string_hiragana = "ぜ"
            added_string_katakana = "ゼ"
        elif added_string == "zo":
            added_string_latin = "zo"
            added_string_hiragana = "ぞ"
            added_string_katakana = "ゾ"
        elif added_string == "xwi":
            added_string_latin = "wi"
            added_string_hiragana = "ゐ"
            added_string_katakana = "ヰ"
        elif added_string == "xwe":
            added_string_latin = "we"
            added_string_hiragana = "ゑ"
            added_string_katakana = "ヱ"
        elif added_string == "*":
            added_string_latin = "*"
            added_string_hiragana = "＊"
            added_string_katakana = "＊"
        elif added_string == "a_double_vowel":
            added_string_latin = "a"
            added_string_hiragana = "あ"
            added_string_katakana = "ー"
        elif added_string == "e_double_vowel":
            added_string_latin = "e"
            added_string_hiragana = "え"
            added_string_katakana = "ー"
        elif added_string == "i_double_vowel":
            added_string_latin = "i"
            added_string_hiragana = "い"
            added_string_katakana = "ー"
        elif added_string == "o_double_vowel":
            added_string_latin = "o"
            added_string_hiragana = "お"
            added_string_katakana = "ー"
        elif added_string == "u_double_vowel":
            added_string_latin = "u"
            added_string_hiragana = "う"
            added_string_katakana = "ー"
        elif added_string == "katakana_repeat_bar":

            if added_string_last != "":
                if added_string_last[-1] == "a":
                    added_string_latin = "a"
                    added_string_hiragana = "あ"
                    added_string_katakana = "ー"
                elif added_string_last[-1] == "i":
                    added_string_latin = "i"
                    added_string_hiragana = "い"
                    added_string_katakana = "ー"
                elif added_string_last[-1] == "u":
                    added_string_latin = "u"
                    added_string_hiragana = "う"
                    added_string_katakana = "ー"
                elif added_string_last[-1] == "e":
                    added_string_latin = "e"
                    added_string_hiragana = "え"
                    added_string_katakana = "ー"
                elif added_string_last[-1] == "o":
                    added_string_latin = "o"
                    added_string_hiragana = "お"
                    added_string_katakana = "ー"
                elif added_string_last == "*":
                    added_string_latin = ""
                    added_string_hiragana = ""
                    added_string_katakana = ""


        elif added_string == "small_tsu":
            added_string_latin = ""
            added_string_hiragana = "っ"
            added_string_katakana = "ッ"

        if added_string_latin != "":
            first_char = added_string_latin[0]
        if added_string_last == "small_tsu":
            if added_string_latin == "":
                added_string_latin = "*"  # If the character after small_tsu is invalid (e.g. a kanji), this line prevents the program from crashing
            else:
                first_char = added_string_latin[0]
                if first_char == 'a' or first_char == 'e' or first_char == 'i' or first_char == 'o' or first_char == 'u' or first_char == 'y':
                    added_string_latin = "*" + added_string_latin
                else:
                    added_string_latin = first_char + added_string_latin

        # Delimiters
        elif character == ",":
            added_string_latin = ", "
            added_string_katakana = ", "
            added_string_hiragana = ", "
            if character_next == " ":
                i += 1

        elif added_string == "original":
            added_string_latin = character
            added_string_hiragana = character
            added_string_katakana = character

        output = [str(i), added_string_latin, added_string_hiragana, added_string_katakana]

        return output
