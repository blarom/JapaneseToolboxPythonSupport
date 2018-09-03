# Japanese Toolbox database creator
import pyrebase
import json
import openpyxl
from keys import apiKey
from keys import serviceAccount
from openpyxl import Workbook
from collections import namedtuple

config = {
    "apiKey": apiKey,
    "authDomain": "japanese-toolbox.firebaseapp.com",
    "databaseURL": "https://japanese-toolbox.firebaseio.com",
    "storageBucket": "japanese-toolbox.appspot.com",
    "serviceAccount": serviceAccount
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

jishoWordsList = db.child("wordsList").get()


# Defining the word class that maps the relevant json input to values in the class
class Word(object):
    romaji = ""
    kanji = ""
    altSpellings = ""

    def __init__(self, json_content):
        data = json.loads(json_content)
        for key, value in data.items():
            self.__dict__[key] = value

    class Meaning(object):
        def __init__(self, json_content):
            data = json.loads(json_content)
            for key, value in data.items():
                self.__dict__[key] = value

        class Explanation(object):
            def __init__(self, json_content):
                data = json.loads(json_content)
                for key, value in data.items():
                    self.__dict__[key] = value


# Preparing the excel sheet for writing
localWordsWorkbook = openpyxl.load_workbook(
    filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/Grammar - 3000 kanji - for pyrebase.xlsx', data_only=True)
localVerbsWorkbook = openpyxl.load_workbook(
    filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/Verbs - 3000 kanji - for pyrebase.xlsx', data_only=True)

# assign_sheet=wb.active
wsLocalMeanings = localWordsWorkbook["Meanings"]
wsLocalTypes = localWordsWorkbook["Types"]
wsLocalGrammar = localWordsWorkbook["Grammar"]
wsLocalVerbsForGrammar = localVerbsWorkbook["VerbsForGrammar"]
wsLocalVerbs = localVerbsWorkbook["Verbs"]


# Getting the size of the Local Types list
lastLocalTypesIndex = 1
while True:
    value = wsLocalTypes.cell(row=lastLocalTypesIndex, column=3).value
    if not value:
        lastLocalTypesIndex -= 1
        break
    lastLocalTypesIndex += 1


# Getting the size of the Local Grammar list
lastLocalGrammarIndex = 1
while True:
    value = wsLocalGrammar.cell(row=lastLocalGrammarIndex, column=3).value
    if not value:
        lastLocalGrammarIndex -= 1
        break
    lastLocalGrammarIndex += 1


# Getting the size of the Local Meanings list
lastLocalMeaningsIndex = 1
while True:
    value = wsLocalMeanings.cell(row=lastLocalMeaningsIndex, column=3).value
    if not value:
        lastLocalMeaningsIndex -= 1
        break
    lastLocalMeaningsIndex += 1


def getJTType(jishoType):
    if jishoType == "Adverb": return "A"
    elif jishoType == "Noun": return "NACF"
    elif jishoType == "Place": return "NPl"
    elif jishoType == "Temporal Noun": return "NT"
    elif jishoType == "Proper Noun": return "NNe"
    elif jishoType == "Numeric": return "NNe"
    elif "Suru verb" in jishoType:
        if "Transitive" in jishoType: return "VsuruT"
        else: return "VsuruI"
    elif "Kuru verb" in jishoType:
        if "Transitive" in jishoType: return "VkuruT"
        else: return "VkuruI"
    elif "Ichidan verb" in jishoType:
        if "Transitive" in jishoType: return "VruiT"
        else: return "VruiI"
    elif "Godan verb with ru" in jishoType:
        if "Transitive" in jishoType: return "VruT"
        else: return "VrugI"
    elif "Godan verb with bu" in jishoType:
        if "Transitive" in jishoType: return "VbuT"
        else: return "VbuI"
    elif "Godan verb with gu" in jishoType:
        if "Transitive" in jishoType: return "VguT"
        else: return "VguI"
    elif "Godan verb with ku" in jishoType:
        if "Transitive" in jishoType: return "VkuT"
        else: return "VkuI"
    elif "Godan verb with mu" in jishoType:
        if "Transitive" in jishoType: return "VmuT"
        else: return "VmuI"
    elif "Godan verb with nu" in jishoType:
        if "Transitive" in jishoType: return "VnuT"
        else: return "VnuI"
    elif "Godan verb with su" in jishoType:
        if "Transitive" in jishoType: return "VsuT"
        else: return "VsuI"
    elif "Godan verb with u" in jishoType:
        if "Transitive" in jishoType: return "VuT"
        else: return "VuI"
    elif ("Suffix" in jishoType) | ("suffix" in jishoType): return "Sx"
    elif ("Prefix" in jishoType) | ("prefix" in jishoType): return "Px"
    elif ("I-adjective" in jishoType) | ("i-adjective" in jishoType): return "Ai"
    elif ("Na-adjective" in jishoType) | ("na-adjective" in jishoType): return "Ana"
    elif "adjective" in jishoType: return "Aj"
    elif "Pre-noun adjectival" in jishoType: return "P"
    elif "Expression" in jishoType: return "CE"
    elif ("Auxiliary verb" in jishoType) | ("Auxiliary adjective" in jishoType): return ""
    elif ("Conjunction" in jishoType) | ("Auxiliary" in jishoType) | ("Particle" in jishoType): return "PP"

    elif jishoType == "A": return jishoType
    elif jishoType == "ADc": return jishoType
    elif jishoType == "ADg": return jishoType
    elif jishoType == "Ai": return jishoType
    elif jishoType == "Aj": return jishoType
    elif jishoType == "AM": return jishoType
    elif jishoType == "Ana": return jishoType
    elif jishoType == "AO": return jishoType
    elif jishoType == "AP": return jishoType
    elif jishoType == "AT": return jishoType
    elif jishoType == "C": return jishoType
    elif jishoType == "CE": return jishoType
    elif jishoType == "iAC": return jishoType
    elif jishoType == "IES": return jishoType
    elif jishoType == "naAC": return jishoType
    elif jishoType == "NAc": return jishoType
    elif jishoType == "NACF": return jishoType
    elif jishoType == "NAn": return jishoType
    elif jishoType == "NAt": return jishoType
    elif jishoType == "NB": return jishoType
    elif jishoType == "NCo": return jishoType
    elif jishoType == "NCu": return jishoType
    elif jishoType == "NDM": return jishoType
    elif jishoType == "NDW": return jishoType
    elif jishoType == "NFa": return jishoType
    elif jishoType == "NFl": return jishoType
    elif jishoType == "NFy": return jishoType
    elif jishoType == "NGO": return jishoType
    elif jishoType == "NJEP": return jishoType
    elif jishoType == "NMAC": return jishoType
    elif jishoType == "NMe": return jishoType
    elif jishoType == "NMo": return jishoType
    elif jishoType == "NMSE": return jishoType
    elif jishoType == "NN": return jishoType
    elif jishoType == "NNe": return jishoType
    elif jishoType == "NNE": return jishoType
    elif jishoType == "NNn": return jishoType
    elif jishoType == "NOI": return jishoType
    elif jishoType == "NPe": return jishoType
    elif jishoType == "NPl": return jishoType
    elif jishoType == "NS": return jishoType
    elif jishoType == "NT": return jishoType
    elif jishoType == "NV": return jishoType
    elif jishoType == "NW": return jishoType
    elif jishoType == "NY": return jishoType
    elif jishoType == "OI": return jishoType
    elif jishoType == "P": return jishoType
    elif jishoType == "PP": return jishoType
    elif jishoType == "Px": return jishoType
    elif jishoType == "Sa": return jishoType
    elif jishoType == "SI": return jishoType
    elif jishoType == "SSC": return jishoType
    elif jishoType == "SSCC": return jishoType
    elif jishoType == "SSD": return jishoType
    elif jishoType == "SSM": return jishoType
    elif jishoType == "SSOF": return jishoType
    elif jishoType == "SSOF": return jishoType
    elif jishoType == "SSP": return jishoType
    elif jishoType == "SSR": return jishoType
    elif jishoType == "SSSi": return jishoType
    elif jishoType == "SSSq": return jishoType
    elif jishoType == "Sx": return jishoType
    elif jishoType == "UNC": return jishoType
    elif jishoType == "VbuI": return jishoType
    elif jishoType == "VbuT": return jishoType
    elif jishoType == "VC": return jishoType
    elif jishoType == "VdaI": return jishoType
    elif jishoType == "VdaT": return jishoType
    elif jishoType == "VguI": return jishoType
    elif jishoType == "VguT": return jishoType
    elif jishoType == "VkuI": return jishoType
    elif jishoType == "VkuruI": return jishoType
    elif jishoType == "VkuruT": return jishoType
    elif jishoType == "VkuT": return jishoType
    elif jishoType == "VmuI": return jishoType
    elif jishoType == "VmuT": return jishoType
    elif jishoType == "VnuI": return jishoType
    elif jishoType == "VnuT": return jishoType
    elif jishoType == "VrugI": return jishoType
    elif jishoType == "VrugT": return jishoType
    elif jishoType == "VruiI": return jishoType
    elif jishoType == "VruiT": return jishoType
    elif jishoType == "VsuI": return jishoType
    elif jishoType == "VsuruI": return jishoType
    elif jishoType == "VsuruT": return jishoType
    elif jishoType == "VsuT": return jishoType
    elif jishoType == "VtsuI": return jishoType
    elif jishoType == "VtsuT": return jishoType
    elif jishoType == "VuI": return jishoType
    elif jishoType == "VuT": return jishoType

    elif jishoType == "Invalid": return ""
    else: return "UNC"

class JishoWord(object):
    romaji = ""
    kanji = ""
    altSpellings = ""
    meanings = []

    def __init__(self, romaji, kanji, altSpellings, meanings):
        self.romaji = romaji
        self.kanji = kanji
        self.altSpellings = altSpellings
        self.meanings = meanings

    class Meaning(object):
        meaning = ""
        grammarType = ""
        grammarTypeForSheets = ""

        def __init__(self, meaning, grammarType, grammarTypeForSheets):
            self.meaning = meaning
            self.grammarType = grammarType
            self.grammarTypeForSheets = grammarTypeForSheets


# Getting the values in the current word and creating the JishoWord list
jishoWords = []
for wordKey in jishoWordsList.val():

    # Getting the Jisho word's characteristics
    word = jishoWordsList.val()[wordKey]
    wordObject = Word(json.dumps(word))

    meanings = []
    for jishoWordMeaningString in wordObject.meanings:

        meaningObject = Word.Meaning(json.dumps(jishoWordMeaningString))
        grammarType = meaningObject.type
        meaning = meaningObject.meaning
        grammarTypeForSheets = "O"

        jishoMeaning = JishoWord.Meaning(meaning, grammarType, grammarTypeForSheets)
        meanings.append(jishoMeaning)

    # Creating the local word object
    jishoWord = JishoWord(wordObject.romaji, wordObject.kanji, wordObject.altSpellings, meanings)
    jishoWords.append(jishoWord)


# Iterating on the JishoWord list
jishoWordIndex = 0
while jishoWordIndex < len(jishoWords):

    jishoWord = jishoWords[jishoWordIndex]


    # Getting the Jisho word's characteristics
    jishoWordRomaji = jishoWord.romaji
    jishoWordKanji = jishoWord.kanji
    jishoWordAltSpellings = jishoWord.altSpellings

    jishoWordMeaningObjects = jishoWord.meanings
    jishoWordMeaningsOriginalList = []
    jishoWordMeaningTypesOriginalList = []
    jishoWordTypesForSheetsOriginalList = []
    for jishoWordMeaningObject in jishoWordMeaningObjects:
        jishoWordMeaningsOriginalList.append(jishoWordMeaningObject.meaning)
        jishoWordMeaningTypesOriginalList.append(jishoWordMeaningObject.grammarType)
        jishoWordTypesForSheetsOriginalList.append(jishoWordMeaningObject.grammarTypeForSheets)

    # Looping through the meanings to create the meanings/types/typesForSheet lists
    jishoWordMeanings = []
    jishoWordMeaningTypes = []
    jishoWordTypesForSheets = []
    for jishoWordMeaningIndex in range(len(jishoWordMeaningsOriginalList)):


        # Getting the object meaning parameters
        jishoWordMeaningString = jishoWordMeaningsOriginalList[jishoWordMeaningIndex]
        jishoTypesString = jishoWordMeaningTypesOriginalList[jishoWordMeaningIndex]
        jishoWordTypeForSheet = jishoWordTypesForSheetsOriginalList[jishoWordMeaningIndex]


        # Checking for critical attributes
        if "Transitive verb" in jishoTypesString: isTransitive = True
        else: isTransitive = False

        if ("Noun" in jishoTypesString) | ("Temporal noun" in jishoTypesString) | ("Proper noun" in jishoTypesString): isDeclaredAsNoun = True
        else: isDeclaredAsNoun = False

        if "Adverb" in jishoTypesString: isDeclaredAsAdverb = True
        else: isDeclaredAsAdverb = False

        # Cycling over the jishoType elements and creating the jisho word's meanings array accordingly
        typeElements = jishoTypesString.split(",")
        for jishoTypeIndex in range(len(typeElements)):

            # Convert the Jisho type to the Japanese Toolbox type
            jishoType = typeElements[jishoTypeIndex].strip()

            if ("verb" in jishoType) & ("ransitive" in jishoType): jishoType = "Invalid"
            elif ("verb" in jishoType) & (not jishoType == "Adverb") & isTransitive: jishoType += "-Transitive"
            elif ("verb" in jishoType) & (not jishoType == "Adverb") & (not isTransitive): jishoType += "-Intransitive"

            if ("No-adjective" in jishoType) & isDeclaredAsNoun: jishoType = "Invalid"
            elif ("No-adjective" in jishoType) & (not isDeclaredAsNoun): jishoType = "Noun"

            if ("prenominally" in jishoType) & isDeclaredAsNoun: jishoType = "Invalid"
            elif ("prenominally" in jishoType) & (not isDeclaredAsNoun): jishoType = "Noun"

            if ("Adverbial noun" in jishoType) & isDeclaredAsNoun: jishoType = "Invalid"
            elif ("Adverbial noun" in jishoType) & (not isDeclaredAsNoun): jishoType = "Noun"

            if ("Adverb taking" in jishoType) & isDeclaredAsAdverb: jishoType = "Invalid"
            elif ("Adverb taking" in jishoType) & (not isDeclaredAsAdverb): jishoType = "Adverb"

            jTType = getJTType(jishoType)

            if jTType == "": continue


            # If the word is a verb, remove the "to "
            if len(jishoType) > 2:
                if ((jTType == "VsuruT") | (jTType == "VsuruI")) & (" suru" not in jishoWordRomaji) & ("ssuru" not in jishoWordRomaji):
                    newMeanings = []
                    newMeanings.append(JishoWord.Meaning(jishoWordMeaningString, jTType, "V"))
                    newJishoWord = JishoWord(jishoWordRomaji + " suru", jishoWordKanji + "する", "", newMeanings)
                    jishoWords.append(newJishoWord)
                elif ( (jTType == "VsuruT") | (jTType == "VsuruI") ) & ("ssuru" not in jishoWordRomaji):
                    jishoWordTypesForSheets.append("V")
                    jishoWordMeaningTypes.append(jTType)
                    jishoWordMeanings.append(jishoWordMeaningString)
                elif (jTType[0] == "V") & ( (jTType[-1] == "I") | (jTType[-1] == "T") ):
                    # If the word is a verb, remove the "to "
                    jishoWordMeaningString = jishoWordMeaningString.replace(", to ", ", ")
                    jishoWordMeaningString = jishoWordMeaningString[3:]
                    jishoWordTypesForSheets.append("V")
                    jishoWordMeaningTypes.append(jTType)
                    jishoWordMeanings.append(jishoWordMeaningString)
                elif (jTType[0:1] == "VC") | (jTType[0:1] == "SS") | (jTType == "PP") | (jTType == "iAC"):
                    jishoWordTypesForSheets.append("G")
                    jishoWordMeaningTypes.append(jTType)
                    jishoWordMeanings.append(jishoWordMeaningString)
                else:
                    jishoWordTypesForSheets.append("O")
                    jishoWordMeaningTypes.append(jTType)
                    jishoWordMeanings.append(jishoWordMeaningString)
            else:
                jishoWordTypesForSheets.append("O")
                jishoWordMeaningTypes.append(jTType)
                jishoWordMeanings.append(jishoWordMeaningString)


    wordAlreadyExists = False


    # Finding the identical local entry in the Grammar sheet
    rowIndexInLocalWordSheet = 2
    while True:
        value = wsLocalGrammar.cell(row=rowIndexInLocalWordSheet, column=3).value
        if not value:
            break

        currentLocalRomaji = str(wsLocalGrammar.cell(row=rowIndexInLocalWordSheet, column=3).value)
        currentLocalKanji = str(wsLocalGrammar.cell(row=rowIndexInLocalWordSheet, column=4).value)
        currentLocalMeaningIndexes = str(wsLocalGrammar.cell(row=rowIndexInLocalWordSheet, column=5).value)

        # Once the identical local entry is found, find the meanings that are unique to the Jisho word, and add them to the database
        if (currentLocalRomaji == jishoWordRomaji) & (currentLocalKanji == jishoWordKanji):

            wordAlreadyExists = True

            localMeaningIndexes = currentLocalMeaningIndexes.split(";")
            localMeaningLoopIndex = 0
            while localMeaningLoopIndex < len(localMeaningIndexes):

                localMeaningIndex = localMeaningIndexes[localMeaningLoopIndex]

                # Getting the current local meaning
                rowIndexInLocalMeanings = int(localMeaningIndex)
                currentMeaning = str(wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value).strip().replace("\u200b", "") # Fixes Zero Width Space bug

                # Checking if the Jisho meaning is already equal to one of the Local word's meanings
                foundMeaning = False
                jishoMeaningLoopIndex = 0
                for jishoWordMeaningString in jishoWordMeanings:

                    if jishoWordTypesForSheets[jishoMeaningLoopIndex] == "G":
                        if jishoWordMeaningString == currentMeaning:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                            break
                        elif jishoWordMeaningString in currentMeaning:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "LOC"
                            break
                        elif currentMeaning in jishoWordMeaningString:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value = jishoWordMeaningString
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                            break
                    jishoMeaningLoopIndex += 1

                if foundMeaning:
                    del jishoWordMeanings[jishoMeaningLoopIndex]
                    del jishoWordTypesForSheets[jishoMeaningLoopIndex]
                    del jishoWordMeaningTypes[jishoMeaningLoopIndex]

                localMeaningLoopIndex += 1

            # The leftover meanings are not present in the local database, so add them to it and update the Local meanings index list
            for i in range(len(jishoWordMeanings)):

                if jishoWordTypesForSheets[i] == "G":
                    jishoWordMeaningString = jishoWordMeanings[i]
                    jishoWordMeaningType = jishoWordMeaningTypes[i]

                    # Adding the results to the meanings excel sheet
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=1).value = lastLocalMeaningsIndex + 1
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=2).value = jishoWordMeaningString
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=3).value = jishoWordMeaningType
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=9).value = "J"

                    # Updating the meaning indexes in the Local Grammar
                    wsLocalGrammar.cell(row=rowIndexInLocalWordSheet, column=5).value = str(wsLocalGrammar.cell(
                        row=rowIndexInLocalWordSheet, column=5).value) + ";" + str(lastLocalMeaningsIndex+1)

                    # Incrementing the meaning index for the next iteration
                    lastLocalMeaningsIndex += 1

            # Once the meanings have been handled, break the while loop in order to process the next Jisho word
            break

        rowIndexInLocalWordSheet += 1


    # Finding the identical local entry in the Verbs sheet
    rowIndexInLocalWordSheet = 4
    while True:
        value = wsLocalVerbs.cell(row=rowIndexInLocalWordSheet, column=7).value
        value2 = wsLocalVerbs.cell(row=rowIndexInLocalWordSheet+1, column=7).value
        value3 = wsLocalVerbs.cell(row=rowIndexInLocalWordSheet+2, column=7).value
        if (not value) & (not value2) & (not value3):
            break

        currentLocalRomaji = str(wsLocalVerbs.cell(row=rowIndexInLocalWordSheet, column=7).value)
        currentLocalKanji = str(wsLocalVerbs.cell(row=rowIndexInLocalWordSheet, column=6).value)
        currentLocalMeaningIndexes = str(wsLocalVerbs.cell(row=rowIndexInLocalWordSheet, column=12).value)

        # Once the identical local entry is found, find the meanings that are unique to the Jisho word, and add them to the database
        if ((currentLocalRomaji == jishoWordRomaji) | (currentLocalRomaji == (jishoWordRomaji + " suru")))\
                & ((currentLocalKanji == jishoWordKanji) | (currentLocalKanji == (jishoWordKanji + "する"))):

            wordAlreadyExists = True

            localMeaningIndexes = currentLocalMeaningIndexes.split(";")
            localMeaningLoopIndex = 0
            while localMeaningLoopIndex < len(localMeaningIndexes):

                localMeaningIndex = localMeaningIndexes[localMeaningLoopIndex]

                # Getting the current local meaning
                rowIndexInLocalMeanings = int(localMeaningIndex)
                currentMeaning = str(wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value).strip().replace("\u200b", "") # Fixes Zero Width Space bug

                # Checking is the Local meaning is already equal to one of the Jisho word's meanings
                foundMeaning = False
                jishoMeaningLoopIndex = 0
                for jishoWordMeaningString in jishoWordMeanings:

                    if jishoWordTypesForSheets[jishoMeaningLoopIndex] == "V":
                        if jishoWordMeaningString == currentMeaning:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                            break
                        elif jishoWordMeaningString in currentMeaning:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "LOC"
                            break
                        elif currentMeaning in jishoWordMeaningString:
                            foundMeaning = True
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value = jishoWordMeaningString
                            wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                            break
                    jishoMeaningLoopIndex += 1

                if foundMeaning:
                    del jishoWordMeanings[jishoMeaningLoopIndex]
                    del jishoWordTypesForSheets[jishoMeaningLoopIndex]
                    del jishoWordMeaningTypes[jishoMeaningLoopIndex]

                localMeaningLoopIndex += 1

            # The leftover meanings are not present in the local database, so add them to it and update the Local meanings index list
            for i in range(len(jishoWordMeanings)):

                # If the verb is a suru verb, the meanings are not added since it is assumed that it already has the correct meanings
                if (jishoWordTypesForSheets[i] == "V") & (not (" suru" in currentLocalRomaji)) & (not ("ssuru" in currentLocalRomaji)):
                    jishoWordMeaningString = jishoWordMeanings[i]
                    jishoWordMeaningType = jishoWordMeaningTypes[i]

                    # Adding the results to the meanings excel sheet
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=1).value = lastLocalMeaningsIndex + 1
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=2).value = jishoWordMeaningString
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=3).value = jishoWordMeaningType
                    wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=9).value = "J"

                    # Updating the meaning indexes in the Local Types
                    wsLocalVerbs.cell(row=rowIndexInLocalWordSheet, column=12).value = str(wsLocalVerbs.cell(
                        row=rowIndexInLocalWordSheet, column=12).value) + ";" + str(lastLocalMeaningsIndex+1)

                    # Incrementing the meaning index for the next iteration
                    lastLocalMeaningsIndex += 1

            # Once the meanings have been handled, break the while loop in order to process the next Jisho word
            break


        rowIndexInLocalWordSheet += 1


    # Finding the identical local entry in the Types sheet
    rowIndexInLocalWordSheet = 2
    while True:
        value = wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=3).value
        if not value:
            break

        currentLocalRomaji = str(wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=3).value)
        currentLocalKanji = str(wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=4).value)
        currentLocalMeaningIndexes = str(wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=5).value)

        # Once the identical local entry is found, find the meanings that are unique to the Jisho word, and add them to the database
        if (currentLocalRomaji == jishoWordRomaji) & (currentLocalKanji == jishoWordKanji):

            wordAlreadyExists = True


            # Removing identical meaning entries from the jisho meanings list: they correspond to different types (e.g. Noun and Ana)
            # but may cause problems with already existing multiple entries.
            # Namely, meaning_Noun = meaning_Ana in Jisho, but meaning_Noun != meaning_Ana in local, so the next loop would create a new
            # version of meaning_Noun or meaning_Ana
            jishoWordMeaningStringIndex = 0
            while jishoWordMeaningStringIndex < len(jishoWordMeanings) - 1:
                duplicateIndex = jishoWordMeaningStringIndex + 1
                while duplicateIndex < len(jishoWordMeanings):
                    if jishoWordMeanings[duplicateIndex] == jishoWordMeanings[jishoWordMeaningStringIndex]:
                        del jishoWordMeanings[duplicateIndex]
                        del jishoWordTypesForSheets[duplicateIndex]
                        del jishoWordMeaningTypes[duplicateIndex]
                    else:
                        duplicateIndex += 1
                jishoWordMeaningStringIndex += 1


            localMeaningIndexes = currentLocalMeaningIndexes.split(";")
            localMeaningLoopIndex = 0
            while localMeaningLoopIndex < len(localMeaningIndexes):

                localMeaningIndex = localMeaningIndexes[localMeaningLoopIndex]

                # Getting the current local meaning
                rowIndexInLocalMeanings = int(localMeaningIndex)
                currentMeaning = str(wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value).strip().replace("\u200b", "") # Fixes Zero Width Space bug

                # Checking is the Local meaning is already equal to one of the Jisho word's meanings
                foundMeaning = False
                jishoMeaningLoopIndex = 0
                for jishoWordMeaningString in jishoWordMeanings:

                    if jishoWordMeaningString == currentMeaning:
                        foundMeaning = True
                        wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                        break
                    elif jishoWordMeaningString in currentMeaning:
                        foundMeaning = True
                        wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "LOC"
                        break
                    elif currentMeaning in jishoWordMeaningString:
                        foundMeaning = True
                        wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2).value = jishoWordMeaningString
                        wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=9).value = "J"
                        break
                    jishoMeaningLoopIndex += 1

                if foundMeaning:
                    del jishoWordMeanings[jishoMeaningLoopIndex]
                    del jishoWordTypesForSheets[jishoMeaningLoopIndex]
                    del jishoWordMeaningTypes[jishoMeaningLoopIndex]

                localMeaningLoopIndex += 1

            # The leftover meanings are not present in the local database, so add them to it and update the Local meanings index list
            for i in range(len(jishoWordMeanings)):
                jishoWordMeaningString = jishoWordMeanings[i]
                jishoWordMeaningType = jishoWordMeaningTypes[i]

                # Adding the results to the meanings excel sheet
                wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=1).value = lastLocalMeaningsIndex + 1
                wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=2).value = jishoWordMeaningString
                wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=3).value = jishoWordMeaningType
                wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=9).value = "J"

                # Updating the meaning indexes in the Local Types
                wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=5).value = str(wsLocalTypes.cell(
                    row=rowIndexInLocalWordSheet, column=5).value) + ";" + str(lastLocalMeaningsIndex+1)

                # Incrementing the meaning index for the next iteration
                lastLocalMeaningsIndex += 1

            # Once the meanings have been handled, break the while loop in order to process the next Jisho word
            break

        rowIndexInLocalWordSheet += 1


    # If there are still meanings left unregistered, create a new entry to the Types sheet
    if not wordAlreadyExists:

        # Adding a new entry in the Local Types list
        wsLocalTypes.cell(row=lastLocalTypesIndex + 1, column=3).value = jishoWordRomaji
        wsLocalTypes.cell(row=lastLocalTypesIndex + 1, column=4).value = jishoWordKanji
        wsLocalTypes.cell(row=lastLocalTypesIndex + 1, column=6).value = jishoWordAltSpellings

        # Adding the meanings to the Local Meanings list and updating the meanings indexes in the Types list
        for i in range(len(jishoWordMeanings)):
            jishoWordMeaningString = jishoWordMeanings[i]
            jishoWordMeaningType = jishoWordMeaningTypes[i]

            # Adding the results to the meanings excel sheet
            wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=1).value = lastLocalMeaningsIndex + 1
            wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=2).value = jishoWordMeaningString
            wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=3).value = jishoWordMeaningType
            wsLocalMeanings.cell(row=lastLocalMeaningsIndex + 1, column=9).value = "J"

            # Updating the meaning indexes in the Local Types
            if i == 0:
                wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=5).value = lastLocalMeaningsIndex+1
            else:
                wsLocalTypes.cell(row=rowIndexInLocalWordSheet, column=5).value = str(wsLocalTypes.cell(
                    row=rowIndexInLocalWordSheet, column=5).value) + ";" + str(lastLocalMeaningsIndex+1)

            # Incrementing the Meaning index for the next iteration
            lastLocalMeaningsIndex += 1

        # Incrementing the Type index for the next Jisho word
        lastLocalTypesIndex += 1


    jishoWordIndex += 1


localWordsWorkbook.save(
    filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/Grammar - 3000 kanji - for pyrebase - updated.xlsx')
localVerbsWorkbook.save(
    filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/Verbs - 3000 kanji - for pyrebase - updated.xlsx')
