#!/usr/bin/python
import re
from os import listdir
from os.path import isfile, join

PATH_UTILITIES_CROSS_PLATFORM = 'C:/Projects/Workspace/Japagram/app/src/main/java/com/japagram/utilitiesCrossPlatform'
PATH_PHP = 'C:/Projects/Workspace/Web/JavaFiles'

REPLACEMENT_FUNCTIONS = {
    'addAll': ['array_push(', 'caller', ', ', 'arguments', ')'],
    'add': ['array_push(', 'caller', ', ', 'arguments', ')'],
    'append': ['array_push(', 'caller', ', ', 'arguments', ')'],
    'replaceAll': ['preg_replace(', 'arguments', ', ', 'caller', ')'],
    'replace': ['preg_replace(', 'arguments', ', ', 'caller', ')'],
    'subList': ['array_slice(', 'caller', ', ', 'arguments', ')'],
    'contains': ['contains(', 'caller', ', ', 'arguments', ')'],
    'containsKey': ['array_key_exists(', 'arguments', ', ', 'caller', ')'],
    'substring': ['mb_substr(', 'caller', ', ', 'arguments', ')'],
    'charAt': ['mb_substr(', 'caller', ', ', 'arguments', ' + 1)'],
    'equals': ['(', 'caller', ' == ', 'arguments', ')'],
    'split': ['explode(', 'arguments', ', ', 'caller', ')'],
    'trim': ['trim(', 'caller', ')'],
    'keySet': ['array_keys(', 'caller', ')'],
    'length': ['mb_strlen(', 'caller', ')'],
    'toLowerCase': ['strtolower(', 'caller', ')'],
    'toUpperCase': ['strtoupper(', 'caller', ')'],
    'toString': ['implode("", ', 'caller', ')'],
    'size': ['sizeof(', 'caller', ')'],
    'get': ['caller', '[', 'arguments', ']'],
}
REPLACEMENT_FUNCTIONS_NO_PARENTHESES = {
    'length': ['sizeof(', 'caller', ')'],
}


def get_file_contents(filename):
    with open(filename, encoding="utf8") as fh:
        return fh.read()


def write_to_file(rwa, filename, content):
    fh = open(filename, rwa, encoding="utf8")
    fh.write(content)
    fh.close()


def get_caller_start_position(end_index, text):
    index = end_index
    is_open_double_quote = False
    is_open_single_quote = False
    num_open_parentheses = 0
    while index > 0:
        char_is_escaped = index > 1 and text[index - 1] == '\\'
        if not char_is_escaped:
            if text[index] == '"' and not is_open_single_quote:
                is_open_double_quote = not is_open_double_quote
            if text[index] == '\'' and not is_open_double_quote:
                is_open_single_quote = not is_open_single_quote
            if text[index] == '(' and not is_open_single_quote and not is_open_double_quote:
                num_open_parentheses -= 1
            if text[index] == ')' and not is_open_single_quote and not is_open_double_quote:
                num_open_parentheses += 1
        is_field_call = index > 1 and text[index - 1:index + 1] == '->'
        if is_field_call: index -= 1
        if num_open_parentheses == -1 or \
                num_open_parentheses == 0 and \
                re.search(r'[\s!?\-+=*&|/%#@^~;,<>]', text[index]) \
                and not is_open_single_quote \
                and not is_open_double_quote \
                and not is_field_call:
            break
        else:
            index -= 1
    return index + 1


def get_closing_parenthesis_position(start_index, text):
    index = start_index
    is_open_double_quote = False
    is_open_single_quote = False
    num_open_parentheses = 1
    while index < len(text) - 1:
        char_is_escaped = index > 1 and text[index - 1] == '\\'
        if not char_is_escaped:
            if text[index] == '"' and not is_open_single_quote:
                is_open_double_quote = not is_open_double_quote
            if text[index] == '\'' and not is_open_double_quote:
                is_open_single_quote = not is_open_single_quote
            if text[index] == '(' and not is_open_single_quote and not is_open_double_quote:
                num_open_parentheses += 1
            if text[index] == ')' and not is_open_single_quote and not is_open_double_quote:
                num_open_parentheses -= 1
        is_field_call = index < len(text) - 2 and text[index:index + 2] == '->'
        if is_field_call: index += 1
        if num_open_parentheses == 0:
            break
        index += 1
    return index


def convert_caller_and_arguments(text, last_line_caller):
    text_converted = text
    is_no_match = 1000000

    for replacement_functions in [REPLACEMENT_FUNCTIONS, REPLACEMENT_FUNCTIONS_NO_PARENTHESES]:
        len_text_converted_last = 0
        while len(text_converted) != len_text_converted_last:
            no_parentheses = replacement_functions == REPLACEMENT_FUNCTIONS_NO_PARENTHESES
            match_positions = {key: is_no_match for key in replacement_functions.keys()}
            len_text_converted_last = len(text_converted)
            for java_function in replacement_functions:
                match_position = text_converted.find('.' + java_function + ('' if no_parentheses else '('))
                match_positions[java_function] = match_position if match_position > -1 else is_no_match

            ordered_java_functions = [[k, v] for k, v in sorted(match_positions.items(), key=lambda x: x[1])]
            java_function = ordered_java_functions[0][0]
            match_position = ordered_java_functions[0][1]

            if match_position == is_no_match:
                return text_converted

            if last_line_caller and re.search(r'^\s*\.\w+', text_converted):
                caller_start_position = match_position
                caller = last_line_caller
            else:
                caller_end_position = match_position
                caller_start_position = get_caller_start_position(caller_end_position - 1, text_converted)
                caller = text_converted[caller_start_position:caller_end_position]

            if no_parentheses:
                arguments_start_position = match_position + len(java_function)
                arguments_end_position = match_position + len(java_function)
                arguments = ''
                arguments_converted = ''
            else:
                arguments_start_position = match_position + len(java_function) + 2
                arguments_end_position = get_closing_parenthesis_position(arguments_start_position, text_converted)
                arguments = text_converted[arguments_start_position:arguments_end_position]
                arguments_converted = convert_caller_and_arguments(arguments, '')

            chosen_preg_replace_key = '/'
            if java_function == 'replace' or java_function == 'replaceAll':
                preg_replace_keys = ['/', '#', '@', '%', '~', '*', '=', '`']
                preg_replace_keys_not_in_arguments_converted = [item for item in preg_replace_keys if item not in arguments_converted]
                if len(preg_replace_keys_not_in_arguments_converted) > 0:
                    chosen_preg_replace_key = preg_replace_keys_not_in_arguments_converted[0]

            function_converted = ''
            for item in replacement_functions[java_function]:
                if item == 'caller':
                    function_converted += caller
                elif item == 'arguments':
                    if java_function == 'replace' or java_function == 'replaceAll':
                        arguments_converted = f'"{chosen_preg_replace_key}"+' + arguments_converted
                        arguments_separator_comma_index = 0
                        is_in_double_quotes = False
                        is_in_single_quotes = False
                        num_open_parentheses = 0
                        for index in range(len(arguments_converted)):
                            is_escaped = index > 1 and arguments_converted[index - 1] == '\\'
                            if not is_escaped and arguments_converted[index] == '"':
                                is_in_double_quotes = not is_in_double_quotes
                            if not is_escaped and arguments_converted[index] == '\'':
                                is_in_single_quotes = not is_in_single_quotes
                            if not is_in_double_quotes and not is_in_single_quotes and arguments_converted[index] == '(':
                                num_open_parentheses += 1
                            if not is_in_double_quotes and not is_in_single_quotes and arguments_converted[index] == ')':
                                num_open_parentheses -= 1
                            if arguments_converted[index] == ',' and not is_in_double_quotes and not is_in_single_quotes and num_open_parentheses == 0:
                                arguments_separator_comma_index = index
                        arguments_converted_pre = arguments_converted[:arguments_separator_comma_index]
                        arguments_converted_mid = f'+"{chosen_preg_replace_key}"'
                        arguments_converted_post = arguments_converted[arguments_separator_comma_index:]
                        arguments_converted = arguments_converted_pre + arguments_converted_mid + arguments_converted_post
                    arguments_converted = arguments_converted.replace('"+"', '')
                    arguments_converted = arguments_converted.replace('\\\\', '\\')
                    function_converted += arguments_converted
                else:
                    function_converted += item

            text_converted = text_converted[:caller_start_position] + function_converted + text_converted[arguments_end_position + 1:]

    return text_converted


def main():
    java_files = [f for f in listdir(PATH_UTILITIES_CROSS_PLATFORM) if isfile(join(PATH_UTILITIES_CROSS_PLATFORM, f))]

    last_line_caller = ''
    for java_name in java_files:
        if 'UtilitiesVerbSearch' not in java_name: continue
        content = get_file_contents(f'{PATH_UTILITIES_CROSS_PLATFORM}/{java_name}')

        content_new = []
        last_line = ''
        content_old = content.split('\n')
        for line_num in range(len(content_old)):

            line_old = content_old[line_num]

            # line skips
            match_java_only = re.search(r'^(package.+|import.+|.+\w+ class .+|.+@Contract.+|.+@NotNull\s*|.+firebase.+;\s*)$', line_old)
            if match_java_only:
                continue

            match_instantiation_no_val = re.search(r'^\s*(public |private |)(final |)(static |)(final |)'
                                                   r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                                                   r'\[*\]*\[*\]*\[*\]*'
                                                   r'\s+\w+\s*;\s*$', line_old)
            if match_instantiation_no_val:
                continue

            # line absolute replacements
            match_comment = re.search(r'^\s*//', line_old)
            if match_comment:
                line_new = line_old
                content_new.append(line_new)
                continue

            match_log = re.search(r'OverridableUtilitiesGeneral.printLog', line_old)
            if match_log:
                line_new = line_old
                content_new.append(re.sub(r'^(\s*)OverridableUtilitiesGeneral.printLog(.+)', r'\g<1>//Log\g<2>', line_new))
                continue

            line_new = line_old

            # java keywords cleaning
            line_new = re.sub(r' @NotNull \[\]', '[]', line_new)
            line_new = re.sub(r'@NotNull\s+', '', line_new)
            line_new = re.sub(r'@SuppressWarnings\(.+?\)', '', line_new)

            # application-specific keywords
            line_new = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', line_new)
            line_new = re.sub(r'OverridableUtilities\w+\.', '', line_new)
            line_new = re.sub(r'Utilities\w+\.', '', line_new)
            line_new = re.sub(r'Globals\.', '', line_new)

            if 'context, String language) {' in line_old:
                a = 1
            # function instantiations
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*\]*\[*\]*\[*\]*'
                              r'\s*(\w+\s*\(.*\))'
                              r'\s*{\s*$',
                              r'\g<1>function \g<7> {', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*\]*\[*\]*\[*\]*'
                              r'\s*(\w+\s*\(.+,)\s*$',
                              r'\g<1>function \g<7>', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*\]*\[*\]*\[*\]*'
                              r'\s*(\w+\s*\()\s*$',
                              r'\g<1>function \g<7>', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'HashMap<.+>'
                              r'\s*(\w+\s*\(.*\))'
                              r'\s*{\s*$',
                              r'\g<1>function \g<6> {', line_new)

            # variable instantiations
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|char|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*\]*\[*\]*\[*\]*\s+(\w+)(\s*=\s*)(.+)$',
                              r'\g<1>\g<7>\g<8>\g<9>', line_new)
            line_new = re.sub(r'^(\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*\]*\[*\]*\[*\]*\s+(\w+)\s*[),]',
                              r'\g<1>\g<3>,', line_new)
            line_new = re.sub(r'^(\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*\]*\[*\]*\[*\]*\s+(\w+)\s*;',
                              r'', line_new)

            # array instantiations
            if re.search(r'new [A-Z][\w.]+\[\]\[\]\s*{\s*$', line_new):
                line_new = re.sub(r'new [\w.]+\[\]\[*\]*\[*\]*\s*{\s*$', r'array(', line_new)
            line_new = re.sub(r'new [\w.]+\[\]\[\]{(.+?)}', r'array(\g<1>)', line_new)
            line_new = re.sub(r'new [\w.]+\[\]{\s*$', r'array(', line_new)
            line_new = re.sub(r'new [\w.]+\[\]{(.+?)}', r'array(\g<1>)', line_new)
            line_new = re.sub(r'new [\w.]+\[\d+\]\s*;', r'array();', line_new)
            line_new = re.sub(r'};', r');', line_new)
            line_new = re.sub(r'new ArrayList<>\(([^,)]+?)\)', r'\g<1>', line_new)
            line_new = re.sub(r'new (ArrayList<>|HashMap<>|StringBuilder)', 'array', line_new)
            line_new = re.sub(r'([^.\s]+)\.put\(([^,]+),([^,]+)\)', r'\g<1>[\g<2>] = \g<3>', line_new)

            match_potential_one_line_array = re.search(r'{.+}', line_new)
            if match_potential_one_line_array:
                is_escaped = False
                is_string_quote = False
                is_char_quote = False
                new_line = ''
                for char in list(line_new):
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
                line_new = new_line

            # java objects & getters/setters/is
            # line_new = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|long|char|boolean|long|[A-Z][a-z][\w.]+)\[*\]*\[*\]*\s+', '', line_new)

            line_new = re.sub(r'\.set\((.+?)\s*,\s*(.+?)\)', r'[\g<1>] = \g<2>', line_new)

            line_new = re.sub(r'\.get([A-Z]\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line_new)
            if re.search(r'\.set([A-Z]\w+)\((.+?)\)', line_new):
                line_new = re.sub(r'(\.set\w+)\((.+?)\)', r'\g<1>() = \g<2>', line_new)
                line_new = re.sub(r'\.set(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line_new)

            line_new = re.sub(r'\.(is\w+)\(\)', r'->\g<1>', line_new)

            # constructs
            line_new = re.sub(r'for\s*\(\s*\S+\s+(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line_new)
            line_new = re.sub(r'for\s*\(\s*(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line_new)
            line_new = re.sub(r'else if', 'elseif', line_new)

            # object manipulations
            # line_new = re.sub(r'([\w$]+)\.length\b[^(]', r'sizeof(\g<1>)', line_new)
            line_new = re.sub(r'Arrays.asList\(([^)]+)\)', r'\g<1>', line_new)
            line_new = re.sub(r'\b[A-Z][\w.]+\.([A-Z]\w+)\b', r'\g<1>', line_new)

            if re.search(r'\w+\(.*\)', line_new) and not re.search(r'function', line_new):
                local_line_num = line_num - 1
                while not last_line_caller:
                    local_content_old_line = content_old[local_line_num]
                    caller_start_position = get_caller_start_position(len(local_content_old_line) - 1, local_content_old_line)
                    last_line_caller = local_content_old_line[caller_start_position:len(local_content_old_line)]
                    local_line_num -= 1
                line_new = convert_caller_and_arguments(line_new, last_line_caller)
                if last_line_caller and re.search(r'^(\s*)\.', line_new):
                    # content_new[local_line_num] = content_new[local_line_num][:-len(last_line_caller)]
                    match_indent = re.search(r'^(\s*)', content_old[line_num])
                    match_indent = match_indent.group(1) if match_indent else ''
                    line_new = f'{match_indent}{last_line_caller} = {line_new}'

            # ints/longs/floats
            line_new = re.sub(r'Float.parseFloat\((.+)\)\)', r'(\g<1> + 0))', line_new)
            line_new = re.sub(r'Float.parseFloat\((.+)\)', r'(\g<1> + 0)', line_new)
            line_new = re.sub(r'Long.parseLong\((.+)\)\)', r'(\g<1> + 0))', line_new)
            line_new = re.sub(r'Long.parseLong\((.+)\)', r'(\g<1> + 0)', line_new)
            line_new = re.sub(r'Integer.parseInt\((.+)\)\)', r'(\g<1> + 0))', line_new)
            line_new = re.sub(r'Integer.parseInt\((.+)\)', r'(\g<1> + 0)', line_new)

            # removing casting
            line_new = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*([\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line_new)
            line_new = re.sub(r'([^<>=\s]+)\s*=\s*\([\w<>.]+?\)\s*\([\w<>.]+?\)\s*(\w<>.]+)\s*\w+', r'\g<1> = \g<2>', line_new)

            # adding $ to variables
            def add_dollar(text):
                text = re.sub(r'if\s*\(\s*([a-z])', r'if ($\g<1>', text)
                text = re.sub(r'else\s+([a-z])', r'else $\g<1>', text)
                text = re.sub(r'\)(\s+)([a-z])', r')\g<1>$\g<2>', text)

                if not re.search(r'^\s*(function\s+|if\s+|else\s+|elseif\s+|while\s+|switch\s+|case\s+|return\s+|break\s*;|for\s*\(|foreach\s*\()', text):
                    text = re.sub(r'^(\s*)([a-z])', r'\g<1>$\g<2>', text)

                text = re.sub(r'(\|\||&&|return\s+|,|\s+<=*|\s+>=*|=|-|\+)\s*([a-z])', r'\g<1> $\g<2>', text)
                text = re.sub(r'(\(\s*)([a-z])', r'\g<1>$\g<2>', text)
                text = re.sub(r'(\s*)([a-z]\w*\s*=)', r'\g<1>$\g<2>', text)
                text = re.sub(r'(\(\s*| )\$(\w+)\(', r'\g<1>\g<2>(', text)
                text = re.sub(r'\$\$', '$', text)
                text = re.sub(r'([:,;?!\[])(\s*)([a-z])', r'\g<1>\g<2>$\g<3>', text)
                return text

            if '"' not in line_new:
                line_new = add_dollar(line_new)
            else:
                line_parts = line_new.split('"')
                is_in_quotes = False
                new_line_parts = []
                for line_part in line_parts:
                    if not is_in_quotes:
                        new_line_parts.append(add_dollar(line_part))
                    else:
                        new_line_parts.append(line_part)
                    if len(line_part) > 0 and line_part[-1] != '\\':
                        is_in_quotes = not is_in_quotes
                line_new = '"'.join(new_line_parts)

            line_new = re.sub(r'\$(null|return|true|false|default|new|continue'
                              r'|contains|array|array_push|array_slice|array_key_exists'
                              r'|substr|mb_substr|mb_strlen|preg_replace|trim|strtolower|strtoupper|sizeof'
                              r'|explode|implode)\b', r'\g<1>', line_new)

            # removing extra empty lines
            if line_new or last_line: content_new.append(line_new)
            last_line = line_new

        php_name = java_name + '.php'
        write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + '\n'.join(content_new) + '\n?>')


main()
