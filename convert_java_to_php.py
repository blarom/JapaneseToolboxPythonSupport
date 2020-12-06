#!/usr/bin/python
import re
from os import listdir
from os.path import isfile, join

PATH_UTILITIES_CROSS_PLATFORM = 'C:/Projects/Workspace/Japagram/app/src/main/java/com/japagram/utilitiesCrossPlatform'
PATH_PHP = 'C:/Projects/Workspace/Web/JavaFiles'


def get_file_contents(filename):
    with open(filename, encoding="utf8") as fh:
        return fh.read()


def write_to_file(rwa, filename, content):
    fh = open(filename, rwa, encoding="utf8")
    fh.write(content)
    fh.close()


def main():
    java_files = [f for f in listdir(PATH_UTILITIES_CROSS_PLATFORM) if isfile(join(PATH_UTILITIES_CROSS_PLATFORM, f))]
    for java_name in java_files:
        if 'UtilitiesDb' not in java_name: continue
        content = get_file_contents(f'{PATH_UTILITIES_CROSS_PLATFORM}/{java_name}')

        content_new = []
        last_line = ''
        for line_pre in content.split('\n'):

            line = line_pre

            if re.search(r'^(package.+|import.+|\w+ class .+|.+@Contract.+|.+@NotNull\s*|.+= new [A-Z][\w.]+\(\).+|.+= new StringBuilder.+)$', line) \
                    or re.search(r'^\s+(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|boolean|[A-Z][a-z]+)\[*\]*\[*\]*\s+\w+\s*;\s*$', line) \
                    or re.search(r'^\s+[A-Z][\w.]+\s+\w+;\s*$', line):
                continue

            if re.search(r'^\s*//', line):
                content_new.append(line)
                continue

            if re.search(r'OverridableUtilitiesGeneral.printLog', line):
                content_new.append(re.sub(r'^(\s*)OverridableUtilitiesGeneral.printLog(.+)', r'\g<1>//Log\g<2>', line))
                continue

            # Class flattening
            line = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', line)
            line = re.sub(r'OverridableUtilities\w+\.', '', line)
            line = re.sub(r'Utilities\w+\.', '', line)
            line = re.sub(r'Globals\.', '', line)

            # Function replacements
            line = re.sub(r'(public|private) static \S+ ', 'function ', line)
            line = re.sub(r'\.get\((.+?)\)\)\)', r'[\g<1>]))', line)
            line = re.sub(r'\.get\((.+?)\)\)', r'[\g<1>])', line)
            line = re.sub(r'\.get\((.+?)\)', r'[\g<1>]', line)
            line = re.sub(r'\.set\((.+?)\s*,\s*(.+?)\)', r'[\g<1>] = \g<2>', line)

            line = re.sub(r'\.get(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line)
            if re.search(r'\.set(\w+)\((.+?)\)', line):
                line = re.sub(r'(\.set\w+)\((.+?)\)', r'\g<1>() = \g<2>', line)
                line = re.sub(r'\.set(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line)

            line = re.sub(r'\.(is\w+)\(\)', r'->\g<1>', line)
            line = re.sub(r'([^,;\s]+).length\(\)', r'mb_strlen(\g<1>)', line)
            line = re.sub(r'([^,;\s]+).toLowerCase\(\)', r'strtolower(\g<1>)', line)
            line = re.sub(r'([^,;\s]+).toUpperCase\(\)', r'strtoupper(\g<1>)', line)
            line = re.sub(r'([\w$]+)\.(size\(\)|length\b)', r'sizeof(\g<1>)', line)
            line = re.sub(r'Arrays.asList\(([^)]+)\)', r'\g<1>', line)
            line = re.sub(r'for\s*\([\w.]+\s+(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line)

            # start + end parenthesis + !
            line = re.sub(r'\(!([^,);\s]+)\.(addAll|add)\((.+)\)\)', r'(!array_push(\g<1>, \g<3>))', line)
            line = re.sub(r'\(!([^,);\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)\)\)', r'(!preg_replace("\g<3>", "\g<4>", \g<1>)))', line)
            line = re.sub(r'\(!([^,);\s]+)\.subList\(([^,;]+),([^,;]+)\)\)', r'(!array_slice(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'\(!([^,);\s]+).contains\(([^,;\s]+)\)\)', r'(!contains(\g<1>, \g<2>))', line)
            line = re.sub(r'\(!([^,);\s]+)\.substring\(\s*([^,;]+)\s*,\s*([^,;]+)\s*\)\)', r'(!mb_substr(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'\(!([^,);\s]+)\.substring\(\s*([^,;]+)\s*\)\)', r'(!mb_substr(\g<1>, \g<2>))', line)
            line = re.sub(r'\(!([^,);\s]+)\.charAt\(\s*(.+?)\s*\)\)', r'(!mb_substr(\g<1>, \g<2>, \g<2>+1))', line)
            line = re.sub(r'\(!([^,);\s]+).equals\(([^,;\s]+)\)\)\)', r'(!(\g<1> == \g<2>))', line)
            line = re.sub(r'\(!([^,);\s]+).split\((.+?)\)\)', r'(!explode(\g<2>, \g<1>))', line)
            line = re.sub(r'\(!([^,);\s]+).trim\(\)\)', r'(!trim(\g<1>))', line)

            # start + end parenthesis
            line = re.sub(r'\(([^,);\s]+)\.(addAll|add)\((.+)\)\)', r'(array_push(\g<1>, \g<3>))', line)
            line = re.sub(r'\(([^,);\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)\)\)', r'(preg_replace("\g<3>", "\g<4>", \g<1>)))', line)
            line = re.sub(r'\(([^,);\s]+)\.subList\(([^,;]+),([^,;]+)\)\)', r'(array_slice(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'\(([^,);\s]+).contains\(([^,;\s]+)\)\)', r'(contains(\g<1>, \g<2>))', line)
            line = re.sub(r'\(([^,);\s]+)\.substring\(\s*([^,;]+)\s*,\s*([^,;]+)\s*\)\)', r'(mb_substr(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'\(([^,);\s]+)\.substring\(\s*([^,;]+)\s*\)\)', r'(mb_substr(\g<1>, \g<2>))', line)
            line = re.sub(r'\(([^,);\s]+)\.charAt\(\s*(.+?)\s*\)\)', r'(mb_substr(\g<1>, \g<2>, \g<2>+1))', line)
            line = re.sub(r'\(([^,);\s]+).equals\(([^,;\s]+)\)\)\)', r'((\g<1> == \g<2>))', line)
            line = re.sub(r'\(([^,);\s]+).split\((.+?)\)\)', r'(explode(\g<2>, \g<1>))', line)
            line = re.sub(r'\(([^,);\s]+).trim\(\)\)', r'(trim(\g<1>))', line)

            # start parenthesis + !
            line = re.sub(r'\(!([^,;\s]+)\.(addAll|add)\((.+)\)', r'(!array_push(\g<1>, \g<3>)', line)
            line = re.sub(r'\(!([^,;\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)\)', r'(!preg_replace("\g<3>", "\g<4>", \g<1>))', line)
            line = re.sub(r'\(!([^,;\s]+)\.subList\(([^,;]+),([^,;]+)\)', r'(!array_slice(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(!([^,;\s]+).contains\(([^,;\s]+)\)', r'(!contains(\g<1>, \g<2>)', line)
            line = re.sub(r'\(!([^,;\s]+)\.substring\(\s*([^,;]+)\s*,\s*([^,;]+)\s*\)', r'(!mb_substr(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(!([^,;\s]+)\.substring\(\s*([^,;]+)\s*\)', r'(!mb_substr(\g<1>, \g<2>)', line)
            line = re.sub(r'\(!([^,;\s]+)\.charAt\(\s*(.+?)\s*\)', r'(!mb_substr(\g<1>, \g<2>, \g<2>+1)', line)
            line = re.sub(r'\(!([^,;\s]+).equals\(([^,;\s]+)\)', r'((\g<1> != \g<2>)', line)
            line = re.sub(r'\(!([^,;\s]+).split\((.+?)\)', r'(!explode(\g<2>, \g<1>)', line)
            line = re.sub(r'\(!([^,;\s]+).trim\(\)', r'(trim(\g<1>)', line)

            # start parenthesis
            line = re.sub(r'\(([^,);\s]+)\.(addAll|add)\((.+)\)', r'(array_push(\g<1>, \g<3>)', line)
            line = re.sub(r'\(([^,);\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)\)', r'(preg_replace("\g<3>", "\g<4>", \g<1>))', line)
            line = re.sub(r'\(([^,);\s]+)\.subList\(([^,;]+),([^,;]+)\)', r'(array_slice(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(([^,);\s]+).contains\(([^,;\s]+)\)', r'(contains(\g<1>, \g<2>)', line)
            line = re.sub(r'\(([^,);\s]+)\.substring\(\s*([^,;]+)\s*,\s*([^,;]+)\s*\)', r'(mb_substr(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(([^,);\s]+)\.substring\(\s*([^,;]+)\s*\)', r'(mb_substr(\g<1>, \g<2>)', line)
            line = re.sub(r'\(([^,);\s]+)\.charAt\(\s*(.+?)\s*\)', r'(mb_substr(\g<1>, \g<2>, \g<2>+1)', line)
            line = re.sub(r'\(([^,);\s]+).equals\(([^,;\s]+)\)', r'(\g<1> == \g<2>)', line)
            line = re.sub(r'\(([^,);\s]+).split\((.+?)\)', r'(explode(\g<2>, \g<1>)', line)
            line = re.sub(r'\(([^,);\s]+).trim\(\)', r'(trim(\g<1>)', line)

            # end parenthesis
            line = re.sub(r'([^,;\s]+)\.(addAll|add)\((.+)\)\)', r'array_push(\g<1>, \g<3>))', line)
            line = re.sub(r'([^,;\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)\)', r'preg_replace("\g<3>", "\g<4>", \g<1>))', line)
            line = re.sub(r'([^,;\s]+)\.subList\(([^,;]+),([^,;]+)\)\)', r'array_slice(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'([^,;\s]+).contains\(([^,;\s]+)\)\)', r'contains(\g<1>, \g<2>))', line)
            line = re.sub(r'([^,;\s]+)\.substring\(\s*([^,]+)\s*,\s*(.+?)\s*\)\)', r'mb_substr(\g<1>, \g<2>, \g<3>))', line)
            line = re.sub(r'([^,;\s]+)\.substring\(\s*(.+?)\s*\)\)', r'mb_substr(\g<1>, \g<2>))', line)
            line = re.sub(r'([^,;\s]+)\.charAt\(\s*(.+?)\s*\)\)', r'mb_substr(\g<1>, \g<2>, \g<2>+1))', line)
            line = re.sub(r'([^,;\s]+).equals\(([^,;\s]+)\)\)', r'\g<1> == \g<2>)', line)
            line = re.sub(r'([^,;\s]+).split\((.+?)\)\)', r'explode(\g<2>, \g<1>))', line)
            line = re.sub(r'([^,;\s]+).trim\(\)\)', r'trim(\g<1>))', line)

            # no parenthesis
            line = re.sub(r'([^,;\s]+)\.(addAll|add)\((.+)\)', r'array_push(\g<1>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+)\.replace(|All)\(\s*\"(.+?)\"\s*,\s*\"(.*?)\"\s*\)', r'preg_replace("\g<3>", "\g<4>", \g<1>)', line)
            line = re.sub(r'([^,;\s]+)\.subList\(([^,;]+),([^,;]+)\)', r'array_slice(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+).contains\(([^,;\s]+)\)', r'contains(\g<1>, \g<2>)', line)
            line = re.sub(r'([^,;\s]+)\.substring\(\s*([^,]+)\s*,\s*(.+?)\s*\)', r'mb_substr(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+)\.substring\(\s*(.+?)\s*\)', r'mb_substr(\g<1>, \g<2>)', line)
            line = re.sub(r'([^,;\s]+)\.charAt\(\s*(.+?)\s*\)', r'mb_substr(\g<1>, \g<2>, \g<2>+1)', line)
            line = re.sub(r'!([^,!;\s]+).equals\(([^;\s]+)\)', r'(\g<1> != \g<2>)', line)
            line = re.sub(r'([^,;\s]+).equals\(([^;\s]+)\)', r'(\g<1> == \g<2>)', line)
            line = re.sub(r'([^,;\s]+).split\((.+?)\)', r'explode(\g<2>, \g<1>)', line)
            line = re.sub(r'([^,;\s]+).trim\(\)', r'trim(\g<1>)', line)

            line = re.sub(r'([^,;\s]+).append\((.+?)\)', r'array_push(\g<1>, \g<2>)', line)

            line = re.sub(r'Long.parseLong\((.+)\)\)', r'(\g<1> + 0))', line)
            line = re.sub(r'Integer.parseInt\((.+)\)\)', r'(\g<1> + 0))', line)
            line = re.sub(r'Long.parseLong\((.+)\)', r'(\g<1> + 0)', line)
            line = re.sub(r'Integer.parseInt\((.+)\)', r'(\g<1> + 0)', line)
            line = re.sub(r'new ArrayList<>\((.+?)\)', r'\g<1>', line)
            line = re.sub(r'new ArrayList<>', 'array', line)
            line = re.sub(r'new [A-Z]\w+\[\]{(.+?)}', r'array(\g<1>)', line)

            if 'preg_replace' in line:
                line = re.sub(r'\\\\', r'\\', line)
                line = re.sub(r'preg_replace\(\"(.+)\"\s*,\s*\"', r'preg_replace("/\g<1>/", ")', line)

            if 'col <= Globals.COLUMN_VERB_MASUSTEM' in line_pre:
                a=1
            # Variable replacements
            line = re.sub(r'@NotNull\s+', '', line)
            line = re.sub(r'@SuppressWarnings\(.+?\)', '', line)
            line = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|long|char|boolean|[A-Z][a-z]\w+)\[*\]*\[*\]*\s+', '', line)
            line = re.sub(r'else if', 'elseif', line)
            line = re.sub(r'if\s*\(\s*(\w)', r'if ($\g<1>', line)
            line = re.sub(r'else\s+(\w)', r'else $\g<1>', line)
            line = re.sub(r'\)(\s+)([a-z])', r')\g<1>$\g<2>', line)

            # Removing casting
            line = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*([\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line)
            line = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*\([\w<>.]+?\)\s*(\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line)

            if not re.search(r'^\s*(function\s+|if\s+|else\s+|elseif\s+|while\s+|switch\s+|case\s+|return\s+|break\s*;|for\s*\(|foreach\s*\()', line):
                line = re.sub(r'^(\s*)([a-z])', r'\g<1>$\g<2>', line)

            line = re.sub(r'(\|\||&&|return|,|\s+<=*|\s+>=*|\s+==|\s+=)\s+([a-z])', r'\g<1> $\g<2>', line)
            line = re.sub(r'(\(\s*)([a-z])', r'\g<1>$\g<2>', line)
            line = re.sub(r'(\s*)([a-z]\w*\s*=)', r'\g<1>$\g<2>', line)
            line = re.sub(r'(\(\s*| )\$(\w+)\(', r'\g<1>\g<2>(', line)
            line = re.sub(r'\$\$', '$', line)
            line = re.sub(r'!(\w)', r'!$\g<1>', line)
            line = re.sub(r'\[([a-z]\w*)', r'[$\g<1>', line)
            line = re.sub(r';\s*([a-z]\w*)', r'; $\g<1>', line)
            line = re.sub(r'\$(null|return|contains|true|false|array|default)\b', r'\g<1>', line)

            if line or last_line: content_new.append(line)
            last_line = line

        php_name = java_name + '.php'
        write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + '\n'.join(content_new) + '\n?>')


main()
