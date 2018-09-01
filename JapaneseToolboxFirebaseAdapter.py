#Japanese Toolbox database creator
import pyrebase
import json
import openpyxl
from openpyxl import Workbook
from collections import namedtuple

#For single key
##config = {
##  "apiKey": "apiKey",
##  "authDomain": "projectId.firebaseapp.com",
##  "databaseURL": "https://databaseName.firebaseio.com",
##  "storageBucket": "projectId.appspot.com"
##}
##firebase = pyrebase.initialize_app(config)

#For admin control
config = {
  "apiKey": "AIzaSyAzcvVsGJvGZ01TQyUuC4avMhOIBPlXUoM",
  "authDomain": "japanese-toolbox.firebaseapp.com",
  "databaseURL": "https://japanese-toolbox.firebaseio.com",
  "storageBucket": "japanese-toolbox.appspot.com",
  "serviceAccount": "C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/japanese-toolbox-firebase-adminsdk-40rl8-3bce188246.json"
}
#from pyrebase import credentials

#cred = credentials.Certificate("C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/japanese-toolbox-firebase-adminsdk-40rl8-3bce188246.json")
firebase = pyrebase.initialize_app(config)

db = firebase.database()

wordsList = db.child("wordsList").get()

#Defining the word class that maps the relevant json input to values in the class
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

#Preparing the excel sheet for writing
wb = openpyxl.load_workbook(filename = 'C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/FirebaseWords.xlsx')

#assign_sheet=wb.active
wsMeanings = wb["Meanings"]
wsTypes = wb["Types"]
typesRowIndex = 2
meaningsRowIndex = 2
meaningIndex = 6863

#Getting the values in the current word
for wordKey in wordsList.val():
    word = wordsList.val()[wordKey]
    wordObject = Word(json.dumps(word))

    #Writing the results to the excel sheet
    wsTypes.cell(row=typesRowIndex, column=3).value = wordObject.kanaIds
    wsTypes.cell(row=typesRowIndex, column=4).value = wordObject.kanji
    wsTypes.cell(row=typesRowIndex, column=6).value = wordObject.altSpellings

    #Update the meanings for the word
    for meaning in wordObject.meanings:
        
        #meaningObject = Word.Meaning(json.dumps(wordObject.meanings[0]))
        meaningObject = Word.Meaning(json.dumps(meaning))

        #Writing the results to the excel sheet
        wsMeanings.cell(row=meaningsRowIndex, column=1).value = meaningIndex
        wsMeanings.cell(row=meaningsRowIndex, column=2).value = meaningObject.meaning
        wsMeanings.cell(row=meaningsRowIndex, column=3).value = meaningObject.type
            
        #print(word)
        print(wordKey, meaningObject.meaning)
        
        explanationObject = Word.Meaning.Explanation(json.dumps(meaningObject.explanations[0]))
        
        meaningIndex += 1
        meaningsRowIndex += 1

    typesRowIndex += 1
            
wb.save(filename = 'C:/Users/Bar/Dropbox/Japanese/JapaneseToolbox/FirebaseWords.xlsx')
