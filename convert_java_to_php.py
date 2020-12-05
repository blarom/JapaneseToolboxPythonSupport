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

            if re.search(r'^(package.+|import.+|\w+ class .+|.+@Contract.+|.+@NotNull\s*|.+= new ArrayList.+)$', line) \
                    or re.search(r'^\s+(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|boolean|[A-Z][a-z]+)\[*\]*\[*\]*\s+\w+\s*;\s*$', line) \
                    or re.search(r'^\s+[A-Z]\w+\s+\w+;\s*$', line):
                continue

            if re.search(r'^\s*//', line_pre):
                content_new.append(line)
                continue


            # Class flattening
            line = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', line)
            line = re.sub(r'OverridableUtilitiesDb.', '', line)
            line = re.sub(r'UtilitiesGeneral\.', '', line)
            line = re.sub(r'Globals\.', '', line)

            # Function replacements
            line = re.sub(r'(public|private) static \S+ ', 'function ', line)
            line = re.sub(r'\.get\((\d+)\)', '[\g<1>]', line)
            line = re.sub(r'\.get(\w+)\(\)', lambda match: f'->{match.group(1).lower()}', line)
            line = re.sub(r'\.(is\w+)\(\)', f'->\g<1>', line)
            line = re.sub(r'([^,;\s]+).length\(\)', 'mb_strlen(\g<1>)', line)
            line = re.sub(r'([\w$]+)\.(size\(\)|length\b)', 'sizeof(\g<1>)', line)
            line = re.sub(r'Arrays.asList\(([^)]+)\)', '\g<1>', line)
            line = re.sub(r'\(([^,;\s]+)\.(addAll|add)\((.+)\)', '(array_push(\g<1>, \g<3>)', line)
            line = re.sub(r'\(([^,;\s]+)\.subList\(([^,;]+),([^,;]+)\)', '(array_slice(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(([^,;\s]+)\.substring\(([^,;]+),([^,;]+)\)', '(mb_substr(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'\(([^,;\s]+).equals\(([^,;\s]+)\)\)', '(\g<1> == \g<2>', line)
            line = re.sub(r'\(([^,;\s]+).contains\(([^,;\s]+)\)', '(contains(\g<1>, \g<2>)', line)
            line = re.sub(r'\(([^,;\s]+).trim\(\)', '(trim(\g<1>)', line)
            line = re.sub(r'([^,;\s]+)\.(addAll|add)\((.+)\)', 'array_push(\g<1>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+)\.subList\(([^,;]+),([^,;]+)\)', 'array_slice(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+)\.substring\(([^,;]+),([^,;]+)\)', 'mb_substr(\g<1>, \g<2>, \g<3>)', line)
            line = re.sub(r'([^,;\s]+).equals\(([^,;\s]+)\)', '\g<1> == \g<2>', line)
            line = re.sub(r'([^,;\s]+).contains\(([^,;\s]+)\)', 'contains(\g<1>, \g<2>)', line)
            line = re.sub(r'([^,;\s]+).trim\(\)', 'trim(\g<1>)', line)

            # Variable replacements
            line = re.sub(r'@NotNull\s+', '', line)
            line = re.sub(r'for\s*\([\w.]+\s+(\w+)\s*:\s*(\w+)\s*\)', 'foreach ($\g<2> AS $\g<1>)', line)
            line = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|boolean|[A-Z][a-z]\w+)\[*\]*\[*\]*\s+', '', line)
            line = re.sub(r'else if', 'elseif', line)
            line = re.sub(r'if\s*\(\s*(\w)', 'if ($\g<1>', line)
            line = re.sub(r'else\s+(\w)', 'else $\g<1>', line)
            line = re.sub(r'\)(\s+)([a-z])', ')\g<1>$\g<2>', line)

            if not re.search(r'^\s*(function\s+|if\s+|else\s+|elseif\s+|return\s+|break\s*;|for\s*\(|foreach\s*\()', line):
                line = re.sub(r'^(\s*)([a-z])', '\g<1>$\g<2>', line)

            line = re.sub(r'(\|\||&&|return|,|\s+<=*|\s+>=*|\s+==|\s+=)\s+([a-z])', '\g<1> $\g<2>', line)
            line = re.sub(r'(\(\s*)([a-z])', '\g<1>$\g<2>', line)
            line = re.sub(r'(\s*)([a-z]\w*\s*=)', '\g<1>$\g<2>', line)
            line = re.sub(r'(\(\s*| )\$(\w+)\(', '\g<1>\g<2>(', line)
            line = re.sub(r'\$\$', '$', line)
            line = re.sub(r'!(\w)', '!$\g<1>', line)
            line = re.sub(r'\$null\b', 'null', line)

            if line or last_line: content_new.append(line)
            last_line = line

        php_name = java_name + '.php'
        write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + '\n'.join(content_new) + '\n?>')


main()
