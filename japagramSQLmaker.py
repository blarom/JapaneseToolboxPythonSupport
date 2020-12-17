import os
from os import listdir
# from pyexcel_ods3 import save_data
from collections import OrderedDict
import Globals

SQL_PATH = r'C:\Projects\Workspace\Web\JT database'
MAX_CHUNK_LENGTH = 2500000
lineFiles = [f for f in listdir(Globals.JAPAGRAM_ASSETS_DIR) if os.path.isfile(os.path.join(Globals.JAPAGRAM_ASSETS_DIR, f))]

data = OrderedDict()
for lineFile in lineFiles:
    content = Globals.get_file_contents(os.path.join(Globals.JAPAGRAM_ASSETS_DIR, lineFile))
    lines = content.split('\n')

    if 'Extended' in lineFile: table_name = '`jt_' + lineFile.split('-')[0][4:-1] + lineFile.split('-')[1][1:-4] + '`'
    else:  table_name = '`jt_' + lineFile[4:].split('-')[0][:-1] + '`'

    # Creating the columns
    sql_content = 'DROP TABLE IF EXISTS ' + table_name + ';\n'
    sql_content += 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (\n'
    if 'ExtendedDbWords' in table_name:
        column_names = ["Index", "romaji", "kanji", "POS", "altSpellings", "meaningsEN", "meaningsFR", "meaningsES"]
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Extended' in lineFile and 'Index' in table_name:
        column_names = ["value", "wordIds"]
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'IndexKanji' in table_name:
        column_names = ['value', 'wordIds', 'kanaIds']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Index' in table_name:
        column_names = ['value', 'wordIds']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Decomposition' in table_name:
        column_names = ['value', 'structure', 'components']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Components' in table_name:
        column_names = ['component', 'associated_components']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'KanjiDict' in table_name:
        column_names = ['value', 'readings', 'english', 'french', 'spanish']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'RadicalsOnly' in table_name:
        column_names = ['Radical', 'Index', 'Radical_Num', 'Num_strokes', 'Radical_name_EN', 'Radical_name_FR', 'Radical_name_ES']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Radicals' in table_name:
        column_names = ['Radical', 'Value']
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8,\n'
        start_row = 0
    elif 'Similars' in table_name or 'Length' in table_name or 'Conj' in table_name:
        continue
    else:
        column_names = lines[0].split('|')
        sql_content += '`' + column_names[0].replace(' ', '_').replace('\\', '\\\\') + '` INT,\n'
        start_row = 1

    sheet = [column_names]
    sql_content += ',\n'.join(['`' + column_names[i].replace(' ', '_').replace('\\', '\\\\') + '` TEXT CHARACTER SET utf8'
                               for i in range(1, len(column_names)) if (start_row == 0 or i < len(column_names) - 1)]) + ');\n'

    # Creating the rows
    insert_line = 'INSERT INTO ' + table_name + ' VALUES\n'
    sql_content += insert_line
    cumulative_content = ''
    partition_index = 0
    is_partitioned = False
    ends_in_vert_line = lines[0][-1] == '|'
    for i in range(start_row, len(lines)):
        column_items = lines[i].split('|')
        if len(column_items) == 0 or lines[i] == '' or column_items[0] == '': continue

        adapted_items = []
        for item in (column_items[:-1] if ends_in_vert_line else column_items):
            if item != '':
                adapted_items.append("\"" + item.replace('\"', '\"\"').replace('\\', '\\\\') + "\"")
            else:
                adapted_items.append("\"\"")

        adapted_line = '(' + ','.join(adapted_items) + '),'
        if len(cumulative_content) + len(adapted_line) > MAX_CHUNK_LENGTH:
            is_partitioned = True

            # Closing the sql content
            sql_content = sql_content[:-1] + ';'

            # Writing to a PART file
            fh = open(os.path.join(SQL_PATH, table_name[1:-1] + '-PART' + str(partition_index) + '.txt'), 'w+', encoding='utf-8')
            fh.write(sql_content)
            fh.close()
            partition_index += 1

            # Resetting the sql and cumulative content
            sql_content = insert_line + adapted_line
            cumulative_content = adapted_line

        else:
            sql_content += adapted_line
            cumulative_content += adapted_line

        sheet.append(column_items[:-1])

    sql_content = sql_content[:-1] + ';'
    fh = open(os.path.join(SQL_PATH, table_name[1:-1] + ('-PART' + str(partition_index) if is_partitioned else '') + '.txt'), 'w+', encoding='utf-8')
    fh.write(sql_content)
    fh.close()

    data.update({'db' + table_name[1:-1]: sheet})

    print("Finished " + table_name[1:-1])

# print("Started saving ods")
# save_data(join(SQL_PATH, 'japagram_db.ods'), data)
