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

    is_two_dim_array = False
    is_one_dim_array = False
    for java_name in java_files:
        if 'UtilitiesVerbSearch' not in java_name: continue
        content = get_file_contents(f'{PATH_UTILITIES_CROSS_PLATFORM}/{java_name}')

        content_new = []
        last_line = ''
        for line_pre in content.split('\n'):

            line = line_pre

            # line skips
            match_java_only = re.search(r'^(package.+|import.+|.+\w+ class .+|.+@Contract.+|.+@NotNull\s*|.+firebase.+;\s*)$', line)
            if match_java_only:
                continue

            match_instantiation_no_val = re.search(r'^\s*(public |private |)(final |)(static |)(final |)'
                                                   r'(int|boolean|float|double|[A-Z][\w.]+<*\S*>*)'
                                                   r'\[*\]*\[*\]*\[*\]*'
                                                   r'\s+\w+\s*;\s*$', line)
            if match_instantiation_no_val:
                continue

            # line absolute replacements
            match_comment = re.search(r'^\s*//', line)
            if match_comment:
                content_new.append(line)
                continue

            match_log = re.search(r'OverridableUtilitiesGeneral.printLog', line)
            if match_log:
                content_new.append(re.sub(r'^(\s*)OverridableUtilitiesGeneral.printLog(.+)', r'\g<1>//Log\g<2>', line))
                continue

            # java keywords cleaning
            line = re.sub(r' @NotNull \[\]', '[]', line)
            line = re.sub(r'@NotNull\s+', '', line)
            line = re.sub(r'@SuppressWarnings\(.+?\)', '', line)

            # application-specific keywords
            line = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', line)
            line = re.sub(r'OverridableUtilities\w+\.', '', line)
            line = re.sub(r'Utilities\w+\.', '', line)
            line = re.sub(r'Globals\.', '', line)

            # function instantiations
            line = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                          r'(int|boolean|float|double|[A-Z][\w.]+<*\S*>*)'
                          r'\[*\]*\[*\]*\[*\]*'
                          r'\s*(\w+\s*\(.*\))'
                          r'\s*{\s*$',
                          r'\g<1>function \g<7> {', line)
            line = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                          r'(int|boolean|float|double|[A-Z][\w.]+<*\S*>*)'
                          r'\[*\]*\[*\]*\[*\]*'
                          r'\s*(\w+\s*\(.+,)\s*$',
                          r'\g<1>function \g<7>', line)
            line = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                          r'(int|boolean|float|double|[A-Z][\w.]+<*\S*>*)'
                          r'\[*\]*\[*\]*\[*\]*'
                          r'\s*(\w+\s*\()\s*$',
                          r'\g<1>function \g<7>', line)
            line = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                          r'HashMap<.+>'
                          r'\s*(\w+\s*\(.*\))'
                          r'\s*{\s*$',
                          r'\g<1>function \g<6> {', line)

            # variable instantiations
            line = re.sub(r'^(\s+)(public |private |)(final |)(static |)(final |)'
                          r'(int|boolean|float|double|[A-Z][\w.]+<*\S*>*|HashMap<[\w.\[\]]+\s*,\s*[\w.\[\]]+>*)'
                          r'\[*\]*\[*\]*\[*\]*\s+(\w+)\s*=\s*(.+)$',
                          r'\g<1>\g<7> = \g<8>', line)

            # array instantiations
            if re.search(r'new [A-Z][\w.]+\[\]\[\]\s*{\s*$', line):
                line = re.sub(r'new [A-Z][\w.]+\[\]\[*\]*\[*\]*\s*{\s*$', r'array(', line)
            line = re.sub(r'new [A-Z][\w.]+\[\]\[\]{(.+?)}', r'array(\g<1>)', line)
            line = re.sub(r'new [A-Z][\w.]+\[\]{\s*$', r'array(', line)
            line = re.sub(r'new [A-Z][\w.]+\[\]{(.+?)}', r'array(\g<1>)', line)
            line = re.sub(r'new [A-Z][\w.]+\[\d+\]\s*;', r'array();', line)
            line = re.sub(r'};', r');', line)
            line = re.sub(r'new ArrayList<>\(([^,)]+?)\)', r'\g<1>', line)
            line = re.sub(r'new (ArrayList<>|HashMap<>|StringBuilder)', 'array', line)
            line = re.sub(r'([^.\s]+)\.put\(([^,]+),([^,]+)\)', r'\g<1>[\g<2>] = \g<3>', line)
            line = re.sub(r'(\w+)\.toString\(\)', r'implode("", \g<1>)', line)

            match_potential_one_line_array = re.search(r'{.+}', line)
            if match_potential_one_line_array:
                is_escaped = False
                is_string_quote = False
                is_char_quote = False
                new_line = ''
                for char in list(line):
                    if char == '{' and not (is_char_quote or is_string_quote):
                        new_line += 'array('
                    elif char == '}' and not (is_char_quote or is_string_quote):
                        new_line += ')'
                    elif char == '"' and not is_string_quote and not is_escaped:
                        is_string_quote = True
                        new_line += char
                    elif char == '\'' and not is_char_quote:
                        is_char_quote = True
                        new_line += char
                    elif char == '\\' and is_string_quote:
                        is_escaped = True
                        new_line += char
                    elif char == '"' and is_string_quote and not is_escaped:
                        is_string_quote = False
                        new_line += char
                    else:
                        new_line += char
                line = new_line

            if 'Globals.VerbLatinConjDatabase.get(rowIndex)[0].equals("") ' in line_pre:
                a=1
            # java objects & getters/setters/is
            line = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|long|char|boolean|[A-Z][a-z][\w.]+)\[*\]*\[*\]*\s+', '', line)

            line = re.sub(r'\.get\((.+?)\)\)\)', r'[\g<1>]))', line)
            line = re.sub(r'\.get\((.+?)\)\[', r'[\g<1>][', line)
            line = re.sub(r'\.get\((.+?)\)\)', r'[\g<1>])', line)
            line = re.sub(r'\.get\((.+?)\)', r'[\g<1>]', line)
            line = re.sub(r'\.set\((.+?)\s*,\s*(.+?)\)', r'[\g<1>] = \g<2>', line)

            line = re.sub(r'\.get(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line)
            if re.search(r'\.set(\w+)\((.+?)\)', line):
                line = re.sub(r'(\.set\w+)\((.+?)\)', r'\g<1>() = \g<2>', line)
                line = re.sub(r'\.set(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line)

            line = re.sub(r'\.(is\w+)\(\)', r'->\g<1>', line)

            # constructs
            line = re.sub(r'for\s*\([\w.]+\s+(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line)
            line = re.sub(r'for\s*\(\s*(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line)
            line = re.sub(r'else if', 'elseif', line)

            # object manipulations
            line = re.sub(r'([^,;\s]+).length\(\)', r'mb_strlen(\g<1>)', line)
            line = re.sub(r'([^,;\s]+).toLowerCase\(\)', r'strtolower(\g<1>)', line)
            line = re.sub(r'([^,;\s]+).toUpperCase\(\)', r'strtoupper(\g<1>)', line)
            line = re.sub(r'([\w$]+)\.(size\(\)|length\b)', r'sizeof(\g<1>)', line)
            line = re.sub(r'Arrays.asList\(([^)]+)\)', r'\g<1>', line)
            line = re.sub(r'([^,;\s]+).append\((.+?)\)', r'array_push(\g<1>, \g<2>)', line)
            line = re.sub(r'\b[A-Z][\w.]+\.([A-Z]\w+)\b', r'\g<1>', line)

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

            if 'preg_replace' in line:
                line = re.sub(r'\\\\', r'\\', line)
                line = re.sub(r'preg_replace\(\"(.+)\"\s*,\s*\"', r'preg_replace("/\g<1>/", ")', line)

            # ints/longs/floats
            line = re.sub(r'Float.parseFloat\((.+)\)\)', r'(\g<1> + 0))', line)
            line = re.sub(r'Float.parseFloat\((.+)\)', r'(\g<1> + 0)', line)
            line = re.sub(r'Long.parseLong\((.+)\)\)', r'(\g<1> + 0))', line)
            line = re.sub(r'Long.parseLong\((.+)\)', r'(\g<1> + 0)', line)
            line = re.sub(r'Integer.parseInt\((.+)\)\)', r'(\g<1> + 0))', line)
            line = re.sub(r'Integer.parseInt\((.+)\)', r'(\g<1> + 0)', line)

            # removing casting
            line = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*([\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line)
            line = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*\([\w<>.]+?\)\s*(\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line)

            # adding $ to variables
            def add_dollar(text):
                text = re.sub(r'if\s*\(\s*([a-z])', r'if ($\g<1>', text)
                text = re.sub(r'else\s+([a-z])', r'else $\g<1>', text)
                text = re.sub(r'\)(\s+)([a-z])', r')\g<1>$\g<2>', text)
                text = re.sub(r':\s+([a-z])', r': $\g<1>', text)

                if not re.search(r'^\s*(function\s+|if\s+|else\s+|elseif\s+|while\s+|switch\s+|case\s+|return\s+|break\s*;|for\s*\(|foreach\s*\()', text):
                    text = re.sub(r'^(\s*)([a-z])', r'\g<1>$\g<2>', text)

                text = re.sub(r'(\|\||&&|return|,|\s+<=*|\s+>=*|\s+==|\s+=|\s+-|\s+\+)\s+([a-z])', r'\g<1> $\g<2>', text)
                text = re.sub(r'(\(\s*)([a-z])', r'\g<1>$\g<2>', text)
                text = re.sub(r'(\s*)([a-z]\w*\s*=)', r'\g<1>$\g<2>', text)
                text = re.sub(r'(\(\s*| )\$(\w+)\(', r'\g<1>\g<2>(', text)
                text = re.sub(r'\$\$', '$', text)
                text = re.sub(r'!([a-z]\w*)', r'!$\g<1>', text)
                text = re.sub(r'\[([a-z]\w*)', r'[$\g<1>', text)
                text = re.sub(r';\s*([a-z]\w*)', r'; $\g<1>', text)
                return text

            if '"' not in line:
                line = add_dollar(line)
            else:
                line_parts = line.split('"')
                is_in_quotes = False
                new_line_parts = []
                for line_part in line_parts:
                    if not is_in_quotes:
                        new_line_parts.append(add_dollar(line_part))
                    else:
                        new_line_parts.append(line_part)
                    if len(line_part) > 0 and line_part[-1] != '\\':
                        is_in_quotes = not is_in_quotes
                line = '"'.join(new_line_parts)

            line = re.sub(r'\$(null|return|contains|true|false|array|default|new)\b', r'\g<1>', line)

            # removing extra empty lines
            if line or last_line: content_new.append(line)
            last_line = line

        php_name = java_name + '.php'
        write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + '\n'.join(content_new) + '\n?>')


main()
