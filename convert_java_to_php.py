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
        content = get_file_contents(f'{PATH_UTILITIES_CROSS_PLATFORM}/{java_name}')

        # Class flattening
        content = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', content)
        content = re.sub(r'UtilitiesGeneral\.', '', content)
        content = re.sub(r'Globals\.', '', content)

        # Line deletions
        content = re.sub(r'package.+\n', '', content)
        content = re.sub(r'import.+\n', '', content)
        content = re.sub(r'\w+ class .+\n', '', content)
        content = re.sub(r'.+@Contract.+\n', '', content)
        content = re.sub(r'@NotNull\s+', '', content)
        content = re.sub(r'.+= new ArrayList.+\n', '', content)

        # Function replacements
        content = re.sub(r'(public|private) static \S+ ', 'function ', content)
        content = re.sub(r'\.get\((\d+)\)', '[\g<1>]', content)
        content = re.sub(r'\.get(\w+)\(\)', lambda match: f'->{match.group(1).lower()}', content)
        content = re.sub(r'([\w$]+)\.(size\(\)|length\b)', 'sizeof(\g<1>)', content)
        content = re.sub(r'([^(\s]+).length\(\)', 'mb_strlen(\g<1>)', content)
        content = re.sub(r'Arrays.asList\(([^)]+)\)', '\g<1>', content)

        # Variable replacements
        content = re.sub(r'\s+\w+.+\w+;\s*\n', '', content)
        content = re.sub(r'for\s*\([\w.]+\s+(\w+)\s*:\s*(\w+)\s*\)', 'foreach ($\g<2> AS $\g<1>)', content)
        content = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|boolean|[A-Z][a-z]+)\[*\]*\[*\]*\s+', '', content)
        content = re.sub(r'else if', 'elseif', content)
        content = re.sub(r'if\s*\(\s*(\w)', 'if ($\g<1>', content)
        content = re.sub(r'else\s+(\w)', 'else $\g<1>', content)
        content = re.sub(r'\)(\s+)([a-z])', ')\g<1>$\g<2>', content)
        content = re.sub(r'(\|\||&&|return|,|\s+<=*|\s+>=*|\s+=)\s+([a-z])', '\g<1> $\g<2>', content)
        content = re.sub(r'(\(\s*)([a-z])', '\g<1>$\g<2>', content)
        content = re.sub(r'(\s*)([a-z]\w*\s*=)', '\g<1>$\g<2>', content)
        content = re.sub(r'(\(\s*| )\$(\w+)\(', '\g<1>\g<2>(', content)
        content = re.sub(r'\$\$', '$', content)

        php_name = java_name + '.php'
        write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + content + '\n?>')


main()
