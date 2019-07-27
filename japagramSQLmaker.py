from os import listdir
from os.path import isfile, join
from pyexcel_ods3 import save_data
from collections import OrderedDict

ASSETS_PATH = r'C:\Projects\Workspace\JapaneseToolbox\app\src\main\assets'
SQL_PATH = r'C:\Projects\Workspace\Web\JT database'
lineFiles = [f for f in listdir(ASSETS_PATH) if isfile(join(ASSETS_PATH, f))]

data = OrderedDict()
for lineFile in lineFiles:
    fh = open(join(ASSETS_PATH, lineFile), 'r+', encoding='utf-8')
    content = fh.read()
    lines = content.split('\n')
    fh.close()

    table_name = '`jt_' + lineFile[4:].split('-')[0][:-1] + '`'

    # Creating the columns
    sql_content = 'DROP TABLE IF EXISTS ' + table_name + ';\n'
    sql_content += 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (\n'

    if 'IndexKanji' in table_name:
        column_names = ['value','word_ids','kana_ids']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Index' in table_name:
        column_names = ['value','word_ids']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Decomposition' in table_name:
        column_names = ['value','structure','components']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Components' in table_name:
        column_names = ['component','associated_components']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'KanjiDict' in table_name:
        column_names = ['value','readings','english','french','spanish']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'RadicalsOnly' in table_name:
        column_names = ['Radical','Index','Radical_Num','Num_strokes','Radical_name_EN','Radical_name_FR','Radical_name_ES']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Radicals' in table_name:
        column_names = ['Radical','Value']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Similars' in table_name or 'Lenght' in table_name or 'Conj' in table_name:
        continue
    else:
        column_names = lines[0].split('|')
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\','\\\\') + '` INT,\n'
        start_row = 1

    sheet = [column_names]
    sql_content += ',\n'.join(['`' + column_names[i].replace(' ', '_').replace('\\','\\\\') + '` TEXT CHARACTER SET utf8'
                               for i in range(1, len(column_names)) if (start_row == 0 or i < len(column_names) - 1)]) + ');\n'

    # Creating the rows
    sql_content += 'INSERT INTO ' + table_name + ' VALUES\n'
    for i in range(start_row, len(lines)):
        column_items = lines[i].split('|')
        if len(column_items) == 0 or lines[i] == '' or column_items[0] == '': continue
        sql_content += '(' + ','.join(["\"" + item.replace('\"', '\"\"').replace('\\','\\\\') + "\"" if item != '' else '\"\"' for item in column_items[:-1]]) + '),'
        sheet.append(column_items[:-1])

    sql_content = sql_content[:-1] + ';'
    data.update({'db'+table_name[1:-1]: sheet})

    fh = open(join(SQL_PATH, table_name[1:-1] + '.txt'), 'w+', encoding='utf-8')
    fh.write(sql_content)
    fh.close()

    print("Finished " + table_name[1:-1])

print("Started saving ods")
save_data(join(SQL_PATH, 'japagram_db.ods'), data)
