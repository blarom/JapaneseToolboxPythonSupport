# Japanese Toolbox database creator
import pyrebase
import json
import openpyxl
from openpyxl import Workbook
from collections import namedtuple

# For single key
# config = {
#  "apiKey": "apiKey",
#  "authDomain": "projectId.firebaseapp.com",
#  "databaseURL": "https://databaseName.firebaseio.com",
#  "storageBucket": "projectId.appspot.com"
# }
# firebase = pyrebase.initialize_app(config)

# For admin control
config = {
    "apiKey": "AIzaSyAzcvVsGJvGZ01TQyUuC4avMhOIBPlXUoM",
    "authDomain": "japanese-toolbox.firebaseapp.com",
    "databaseURL": "https://japanese-toolbox.firebaseio.com",
    "storageBucket": "japanese-toolbox.appspot.com",
    "serviceAccount": "C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/japanese-toolbox-firebase-adminsdk-40rl8-3bce188246.json"
}
# from pyrebase import credentials

# cred = credentials.Certificate("C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/japanese-toolbox-firebase-adminsdk-40rl8-3bce188246.json")
firebase = pyrebase.initialize_app(config)

db = firebase.database()

jishoWordsList = db.child("wordsList").get()


# Defining the word class that maps the relevant json input to values in the class
class Word(object):
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
localWordsWorkbook = openpyxl.load_workbook(filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/Grammar - 3000 kanji - for pyrebase.xlsx')
jishoWordsWorkbook = openpyxl.load_workbook(filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/FirebaseWords.xlsx')

# assign_sheet=wb.active
wsJishoMeanings = jishoWordsWorkbook["Meanings"]
wsJishoTypes = jishoWordsWorkbook["Types"]
wsLocalMeanings = localWordsWorkbook["Meanings"]
wsLocalTypes = localWordsWorkbook["Types"]
typesRowIndex = 2
meaningsRowIndex = 2
meaningIndex = 6863

# Getting the values in the current word
for wordKey in jishoWordsList.val():


    # Getting the Jisho word's characteristics
    word = jishoWordsList.val()[wordKey]
    wordObject = Word(json.dumps(word))

    jishoWordRomaji = wordObject.romaji
    jishoWordKanji = wordObject.kanji
    jishoWordAltSpellings = wordObject.altSpellings

    jishoWordMeanings = []
    jishoWordMeaningTypes = []
    for meaning in wordObject.meanings:
        meaningObject = Word.Meaning(json.dumps(meaning))
        jishoWordMeanings.append(meaningObject.meaning)
        jishoWordMeaningTypes.append(meaningObject.type)


    # Finding the identical local entry
    rowIndexInLocalTypes = 2
    foundMatchingLocalWord = False
    while wsLocalTypes.cell(row=rowIndexInLocalTypes, column=3) != "":
        currentLocalRomaji = wsLocalTypes.cell(row=rowIndexInLocalTypes, column=3)
        currentLocalKanji = wsLocalTypes.cell(row=rowIndexInLocalTypes, column=4)
        currentLocalMeaningIndex = wsLocalTypes.cell(row=rowIndexInLocalTypes, column=5)

        # Once the identical local entry is found, find the meanings that are unique to the Jisho word, and add them to the database
        if currentLocalRomaji == jishoWordRomaji & currentLocalKanji == jishoWordKanji:

            foundMatchingLocalWord = True

            localMeaningIndexes = currentLocalMeaningIndex.split(";")
            for localMeaningIndex in localMeaningIndexes:

                # Getting the current local meaning
                meaningAsNumber = int(localMeaningIndex)
                rowIndexInLocalMeanings = 2
                while rowIndexInLocalMeanings != meaningAsNumber:
                    rowIndexInLocalMeanings += 1
                currentMeaning = wsLocalMeanings.cell(row=rowIndexInLocalMeanings, column=2)

                # Checking is the Local meaning is already equal to one of the Jisho word's meanings
                foundMeaning = False
                index = 0
                for meaning in jishoWordMeanings:
                    if meaning == currentMeaning:
                        foundMeaning = True
                        break
                    index += 1

                if foundMeaning:
                    jishoWordMeanings.remove(index)

            # The leftover meanings are not present in the local database, so add them to it and update the Local meanings index list
            for meaning in jishoWordMeanings:

                #TODO: setup the correct meaningIndex
                # Writing the results to the excel sheet
                wsJishoMeanings.cell(row=meaningsRowIndex, column=1).value = meaningIndex
                wsJishoMeanings.cell(row=meaningsRowIndex, column=2).value = meaningObject.meaning
                wsJishoMeanings.cell(row=meaningsRowIndex, column=3).value = meaningObject.type

            # Once the meanings have been handled, break the while loop
            break

    if not foundMatchingLocalWord:

        # Adding the whole Jisho word and its meanings to the database

        #TODO: correct the following code, and add the "J" to indicate this is a Jisho word

        # Writing the results to the excel sheet
        wsJishoTypes.cell(row=typesRowIndex, column=3).value = wordObject.kanaIds
        wsJishoTypes.cell(row=typesRowIndex, column=4).value = wordObject.kanji
        wsJishoTypes.cell(row=typesRowIndex, column=6).value = wordObject.altSpellings

        # Update the meanings for the word
        for meaning in wordObject.meanings:
            # meaningObject = Word.Meaning(json.dumps(wordObject.meanings[0]))
            meaningObject = Word.Meaning(json.dumps(meaning))

            # Writing the results to the excel sheet
            wsJishoMeanings.cell(row=meaningsRowIndex, column=1).value = meaningIndex
            wsJishoMeanings.cell(row=meaningsRowIndex, column=2).value = meaningObject.meaning
            wsJishoMeanings.cell(row=meaningsRowIndex, column=3).value = meaningObject.type

            # print(word)
            print(wordKey, meaningObject.meaning)

            explanationObject = Word.Meaning.Explanation(json.dumps(meaningObject.explanations[0]))

            meaningIndex += 1
            meaningsRowIndex += 1

        typesRowIndex += 1

jishoWordsWorkbook.save(filename='C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/FirebaseWords.xlsx')
