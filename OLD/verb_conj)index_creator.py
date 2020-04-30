# region Reading worksheets
VerbsWorkbook = openpyxl.load_workbook(filename='C:/Users/Bar/Dropbox/Japanese/Verbs - 3000 kanji.xlsx', data_only=True)
print("Finished loading Verbs - 3000 kanji.xlsx")
wsVerbsForGrammar = VerbsWorkbook["VerbsForGrammar"]
wsVerbs = VerbsWorkbook["Verbs"]
wsLatinConj = VerbsWorkbook["LatinConj"]
wsKanjiConj = VerbsWorkbook["KanjiConj"]
wsLatinConjIndex = VerbsWorkbook["LatinConjIndex"]
wsKanjiConjIndex = VerbsWorkbook["KanjiConjIndex"]
# endregion

# region Getting the family conjugations
conjugations_latin_per_family = {}
conjugations_kanji_per_family = {}
last_col = 1
while wsLatinConj.cell(row=3, column=last_col).value:
    last_col += 1

row = 2
while not Globals.isLastRow(wsLatinConj, row):
    family = wsLatinConj.cell(row=row, column=idx("A")).value
    if not family:
        row += 1
        continue
    match = re.search(r'(.*(godan|special class|ichidan|suru|kuru|desu).*)', wsLatinConj.cell(row=row, column=idx("A")).value)
    if match and not wsLatinConj.cell(row=row, column=idx("H")).value:
        conjugations_latin_per_family[match.group(0)] = [wsLatinConj.cell(row=row, column=i).value if wsLatinConj.cell(row=row, column=i).value else "" for i in range(1, last_col + 1)]
        conjugations_kanji_per_family[match.group(0)] = [wsKanjiConj.cell(row=row, column=i).value if wsKanjiConj.cell(row=row, column=i).value else "" for i in range(1, last_col + 1)]
    row += 1
# endregion

# region Creating the conjugation dicts and index
latinConjIndex = {}
kanjiConjIndex = {}
row = 2
while not Globals.isLastRow(wsVerbsForGrammar, row):
    conjIndex = int(wsVerbsForGrammar.cell(row=row, column=Globals.TYPES_COL_EXCEPTION_INDEX).value) + 1
    verbIndex = str(wsVerbsForGrammar.cell(row=row, column=Globals.TYPES_COL_INDEX).value)
    conj_family = wsLatinConj.cell(row=conjIndex, column=idx("A")).value
    is_family_conj = not wsLatinConj.cell(row=conjIndex, column=idx("B")).value
    alt_spellings = wsVerbsForGrammar.cell(row=row, column=Globals.TYPES_COL_ALTS).value
    alt_spellings = alt_spellings.replace(' ', '') if alt_spellings else ""
    root = wsVerbsForGrammar.cell(row=row, column=Globals.TYPES_COL_ROMAJI_ROOT).value
    latinRoots = [root if root else ""]
    root = wsVerbsForGrammar.cell(row=row, column=Globals.TYPES_COL_KANJI_ROOT).value
    kanjiRoots = [root if root else ""]
    for item in alt_spellings.split(','):
        if not item: continue
        if Globals.is_latin(item):
            latinRoots.append(Globals.get_root_from_masu_stem_latin(item, conj_family))
        else:
            kanjiRoots.append(Globals.get_root_from_masu_stem_kanji(item, conj_family))

    for latinRoot in latinRoots:
        current_verb_conjugations_latin = [latinRoot + termination for termination in conjugations_latin_per_family[conj_family][10:]]
        if not is_family_conj:
            for col in range(0, last_col - 10):
                current_verb_conjugations_latin[col] = wsLatinConj.cell(row=conjIndex, column=col + 10).value
        for item in current_verb_conjugations_latin:
            if item:
                latinConjIndex[item] = [verbIndex] if item not in latinConjIndex.keys() else latinConjIndex[item] + [verbIndex]
                latinConjIndex[item] = list(set(latinConjIndex[item]))

    for kanjiRoot in kanjiRoots:
        current_verb_conjugations_kanji = [kanjiRoot + termination for termination in conjugations_kanji_per_family[conj_family][10:]]
        if not is_family_conj:
            for col in range(0, last_col - 10):
                current_verb_conjugations_kanji[col] = wsKanjiConj.cell(row=conjIndex, column=col + 10).value
        for item in current_verb_conjugations_kanji:
            if item and item != '*':
                kanjiConjIndex[item] = [verbIndex] if item not in kanjiConjIndex.keys() else kanjiConjIndex[item] + [verbIndex]
                kanjiConjIndex[item] = list(set(kanjiConjIndex[item]))

    if row % 100 == 0: print(f"VerbsForGrammar - finished row {row}")
    row += 1
# endregion

# region Writing to the worksheets
sorted_keys = sorted(latinConjIndex.keys())
for i in range(0, len(sorted_keys)):
    wsLatinConjIndex.cell(row=i + 1, column=1).value = sorted_keys[i]
    wsLatinConjIndex.cell(row=i + 1, column=2).value = ';'.join(latinConjIndex[sorted_keys[i]])
sorted_keys = sorted(kanjiConjIndex.keys())
for i in range(0, len(sorted_keys)):
    wsKanjiConjIndex.cell(row=i + 1, column=1).value = sorted_keys[i]
    wsKanjiConjIndex.cell(row=i + 1, column=2).value = ';'.join(kanjiConjIndex[sorted_keys[i]])
# endregion

# region Saving the results to xlsx & csv
if create_workbooks:
    VerbsWorkbook.save(filename='C:/Users/Bar/Dropbox/Japanese/Verbs - 3000 kanji - ready for Japagram.xlsx')

Globals.create_csv_from_worksheet(wsLatinConjIndex, name("VerbConjLatinSortedIndex"), idx("A"), idx("B"))
Globals.create_csv_from_worksheet(wsKanjiConjIndex, name("VerbConjKanjiSortedIndex"), idx("A"), idx("B"))
# endregion