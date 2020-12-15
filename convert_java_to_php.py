#!/usr/bin/python
import re
from os import listdir
from os.path import isfile, join

import Globals

PATH_UTILITIES_CROSS_PLATFORM = 'C:/Projects/Workspace/Japagram/app/src/main/java/com/japagram/utilitiesCrossPlatform'
PATH_UTILITIES_OVERRIDABLE = 'C:/Projects/Workspace/Japagram/app/src/main/java/com/japagram/utilitiesPlatformOverridable'
PATH_PHP = 'C:/Projects/Workspace/Web/Java2PhpFiles'

REPLACEMENT_FUNCTIONS = {
    'addAll': ['array_merge(', 'caller', ', ', 'arguments', ')'],
    'add': ['array_push(', 'caller', ', ', 'arguments', ')'],
    'startsWith': ['startsWith(', 'caller', ', ', 'arguments', ')'],
    'endsWith': ['endsWith(', 'caller', ', ', 'arguments', ')'],
    'append': ['array_push(', 'caller', ', ', 'arguments', ')'],
    'replaceAll': ['preg_replace(', 'arguments', ', ', 'caller', ')'],
    'replace': ['str_replace(', 'arguments', ', ', 'caller', ')'],
    'subList': ['array_slice(', 'caller', ', ', 'arguments', ')'],
    'contains': ['contains(', 'caller', ', ', 'arguments', ')'],
    'containsKey': ['array_key_exists(', 'arguments', ', ', 'caller', ')'],
    'substring': ['mb_substr(', 'caller', ', ', 'arguments', ', \'UTF-8\')'],
    'charAt': ['caller', '[', 'arguments', ']'],
    'equals': ['(', 'caller', ' == ', 'arguments', ')'],
    'split': ['explode(', 'arguments', ', ', 'caller', ')'],
    'trim': ['trim(', 'caller', ')'],
    'keySet': ['array_keys(', 'caller', ')'],
    'length': ['mb_strlen(', 'caller', ', \'UTF-8\')'],
    'toLowerCase': ['strtolower(', 'caller', ')'],
    'toUpperCase': ['strtoupper(', 'caller', ')'],
    'toString': ['implode("", ', 'caller', ')'],
    'size': ['sizeof(', 'caller', ')'],
    'get': ['caller', '[', 'arguments', ']'],
    'printStackTrace': ['echo \'Caught exception: \', ', 'caller', '->getMessage(), \'\\n\''],
}
REPLACEMENT_FUNCTIONS_NO_PARENTHESES = {
    'length': ['sizeof(', 'caller', ')'],
}


def find_complementary_char_index(requested_char, start_index, direction, text):
    increment = -1 if direction == 'left' else 1
    is_in_double_quotes = False
    is_in_single_quotes = False
    num_open_parentheses = 0
    num_open_curly = 0
    num_open_square = 0
    for index in range(start_index, len(text)):
        is_escaped = index > 1 and text[index - 1] == '\\'
        if not is_escaped and text[index] == '"' and not is_in_single_quotes:
            is_in_double_quotes = not is_in_double_quotes
        if not is_escaped and text[index] == '\'' and not is_in_double_quotes:
            is_in_single_quotes = not is_in_single_quotes
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == '(':
            num_open_parentheses += increment
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == ')':
            num_open_parentheses -= increment
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == '{':
            num_open_curly += increment
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == '}':
            num_open_curly -= increment
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == '[':
            num_open_square += increment
        if not is_in_double_quotes and not is_in_single_quotes and text[index] == ']':
            num_open_square -= increment
        if text[index] == requested_char and \
                not is_in_double_quotes and \
                not is_in_single_quotes and \
                num_open_parentheses == 0 and \
                num_open_curly == 0 and \
                num_open_square == 0:
            return index
    return -1


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
            index += 1
            break
        else:
            index -= 1
    return index


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
    text = re.sub(r'([:,;?!\[])(\s*)\$([a-z]\w+)\(', r'\g<1>\g<2>\g<3>(', text)
    return text


def add_dollars_in_text_incl_quotes(text):
    if '"' not in text:
        text = add_dollar(text)
    else:
        line_parts = text.split('"')
        is_in_quotes = False
        new_line_parts = []
        for i in range(len(line_parts)):
            if i > 0 and (line_parts[i - 1] == '' or len(line_parts[i - 1]) > 0 and line_parts[i - 1][-1] != '\\'):
                is_in_quotes = not is_in_quotes
            if not is_in_quotes:
                new_line_parts.append(add_dollar(line_parts[i]))
            else:
                new_line_parts.append(line_parts[i])
        text = '"'.join(new_line_parts)

    text = re.sub(r'\$(null|return|true|false|default|new|continue|try|catch|finally|echo'
                  r'|contains|array|array_push|array_slice|array_fill|array_key_exists'
                  r'|substr|mb_substr|mb_strlen|preg_replace|str_replace|trim|strtolower|strtoupper|sizeof'
                  r'|explode|implode)\b', r'\g<1>', text)
    return text


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
                break

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
            if java_function == 'replaceAll':
                preg_replace_keys = ['/', '#', '@', '%', '~', '*', '=', '`']
                preg_replace_keys_not_in_arguments_converted = [item for item in preg_replace_keys if item not in arguments_converted]
                if len(preg_replace_keys_not_in_arguments_converted) > 0:
                    chosen_preg_replace_key = preg_replace_keys_not_in_arguments_converted[0]

            function_converted = ''
            for item in replacement_functions[java_function]:
                if item == 'caller':
                    function_converted += caller
                elif item == 'arguments':
                    if java_function == 'replaceAll':
                        arguments_converted = f'"{chosen_preg_replace_key}"+' + arguments_converted
                        arguments_separator_comma_index = find_complementary_char_index(',', 0, 'right', arguments_converted)
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
    is_open_global = False
    for java_name in java_files:
        # if 'UtilitiesVerbSearch' not in java_name: continue
        content = Globals.get_file_contents(f'{PATH_UTILITIES_CROSS_PLATFORM}/{java_name}')

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
                                                   r'\[*]*\[*]*\[*]*'
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
            line_new = re.sub(r' @NotNull \[]', '[]', line_new)
            line_new = re.sub(r'@NotNull\s+', '', line_new)
            line_new = re.sub(r'@SuppressWarnings\(.+?\)', '', line_new)
            line_new = re.sub(r"\(\s*int\s*\)\s*(\w+.charAt\(\d+\))", r"ord(\g<1>)", line_new)
            line_new = re.sub(r"\(\s*int\s*\)\s*'(\w)'", r"ord('\g<1>')", line_new)
            line_new = re.sub(r'\(\s*(int|String|List)(|<[\w<>]+>)\s*\)\s*', '', line_new)
            line_new = re.sub(r'\b([\d]+)\.f\b', r'\g<1>.0', line_new)
            line_new = re.sub(r'\b([\d.]+)\.f\b', r'\g<1>', line_new)

            # application-specific keywords
            line_new = re.sub(r'OverridableUtilitiesGeneral.joinList', 'implode', line_new)
            line_new = re.sub(r'OverridableUtilities\w+\.', '', line_new)
            line_new = re.sub(r'Utilities\w+\.', '', line_new)

            # function instantiations
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*]*\[*]*\[*]*'
                              r'\s*(\w+\s*\(.*\))'
                              r'\s*{\s*$',
                              r'\g<1>function \g<7> {', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*]*\[*]*\[*]*'
                              r'\s*(\w+\s*\()\s*\S+\s+(\S+\s*,)',
                              r'\g<1>function \g<7>\g<8>', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|float|double|[A-Z][\w.]+<*\S*>*)'
                              r'\[*]*\[*]*\[*]*'
                              r'\s*(\w+\s*\()\s*$',
                              r'\g<1>function \g<7>', line_new)
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'HashMap<.+?>'
                              r'\s*(\w+\s*\(.*\))'
                              r'\s*{\s*$',
                              r'\g<1>function \g<6> {', line_new)
            if 'function ' in line_new:
                line_new = re.sub(r'(function\s*\w+\s*\()\s*\S+\s+(\S+\s*)([,)])',
                                  r'\g<1>\g<2>\g<3>', line_new)
                line_new = re.sub(r',\s*\S+\s+(\S+)\s*([,)])',
                                  r', \g<1>\g<2>', line_new)

            if 'conjugationTitle.setTitle(OverridableUtilitiesResources.getString(titleRef, context, Globals.RESOURCE_MAP_VERB_CONJ_TITLES, language));' in line_old:
                a = 1
            # variable instantiations
            line_new = re.sub(r'^(\s*)(public |private |)(final |)(static |)(final |)'
                              r'(int|boolean|long|char|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)(\s*=\s*)(.+)$',
                              r'\g<1>\g<7>\g<8>\g<9>', line_new)
            line_new = re.sub(r'^(\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)\s*([),])',
                              r'\g<1>\g<3>\g<4>', line_new)
            line_new = re.sub(r'(,\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)\s*,',
                              r'\g<1>\g<3>,', line_new)
            line_new = re.sub(r'(,\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*[^,]+>*)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)\s*\)',
                              r'\g<1>\g<3>)', line_new)
            line_new = re.sub(r'(,\s*)(HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>*)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)\s*\)',
                              r'\g<1>\g<3>)', line_new)
            line_new = re.sub(r'^(\s*)(int|char|boolean|long|float|double|[A-Z][\w.]+<*\S*>*|HashMap<\s*[\w.\[\]]+\s*,\s*[\w.\[\]]+\s*>)'
                              r'\[*]*\[*]*\[*]*\s+([\w.]+)\s*;',
                              r'', line_new)
            line_new = re.sub(r'^(\s*)(HashMap<\s*[\w.\[\]<>]+\s*,\s*[\w.\[\]<>]+\s*>)'
                              r'\s+(\w+\s*)',
                              r'\g<1>\g<3>', line_new)
            # globals
            line_new = re.sub(r'^(\s*)([A-Z0-9_]+)\s*=\s*(.+);', r"\g<1>define('\g<2>', \g<3>);", line_new)
            match_global_open = re.search(r'^\s*([A-Z0-9_]+)\s*=\s*(.+)', line_new)
            if match_global_open:
                is_open_global = True
                line_new = re.sub(r'([A-Z0-9_]+)\s*=\s*(.+)', r"define('\g<1>', \g<2>", line_new)
            if is_open_global and re.search(r'}\s*;', line_new):
                line_new = re.sub(r'}\s*;', r"));", line_new)
                is_open_global = False
            line_new = re.sub(r'(\bGLOBAL_[A-Z][A-Z0-9_]+\b)', r"$GLOBALS['\g<1>']", line_new)
            # line_new = re.sub(r"^(\s*define\()'\$GLOBALS\['([A-Z][A-Z0-9_]+)']'", r"\g<1>\g<2>", line_new)
            # line_new = re.sub(r"\"\$GLOBALS\['([A-Z][A-Z0-9_]+)']\"", r'"\g<1>"', line_new)
            # line_new = re.sub(r'Globals\.([A-Z0-9_]+)', r"$GLOBALS['\g<1>']", line_new)
            line_new = re.sub(r'Globals\.', r"", line_new)
            # line_new = re.sub(r"\[\$GLOBALS\['([A-Z][A-Z0-9_]+)']]", r'[\g<1>]', line_new)

            # constructs
            line_new = re.sub(r'for\s*\(\s*\S+\s+(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line_new)
            line_new = re.sub(r'for\s*\(\s*(\w+)\s*:\s*(\S+)\s*\)', r'foreach ($\g<2> AS $\g<1>)', line_new)
            line_new = re.sub(r'for\s*\(\s*int\s*', r'for (', line_new)
            line_new = re.sub(r'else if', 'elseif', line_new)

            # array instantiations
            if re.search(r'\bnew [\w.]+\[[^]]', line_new):
                square_index = 0
                complementary_square_index = 0
                array_sizes = []
                while square_index != -1 and complementary_square_index >= square_index:
                    match_instantiation = re.search(r'\bnew [\w.]+\[', line_new)
                    if not match_instantiation: break
                    instantiation_start_index = match_instantiation.start()
                    array_filler = 0
                    if 'new String' in match_instantiation.group(0): array_filler = '""'
                    if re.search(r'(Array|Linked|Map|List)', match_instantiation.group(0)): array_filler = 'array()'

                    complementary_square_index = match_instantiation.end() - 1
                    while square_index != -1 and complementary_square_index >= square_index:
                        square_index = line_new.find('[', complementary_square_index)
                        if square_index == -1: break
                        complementary_square_index = find_complementary_char_index(']', square_index, 'right', line_new)
                        if complementary_square_index == -1: break
                        array_sizes.append(line_new[square_index + 1:complementary_square_index])

                    if array_sizes and (complementary_square_index == -1 or not re.search(r'^\s*\[', line_new[complementary_square_index + 1:])):
                        replacement = array_filler
                        for i in range(len(array_sizes)):
                            replacement = f'array_fill(0, {array_sizes[i]}, {replacement})'
                        line_new = line_new[:instantiation_start_index] + replacement + line_new[complementary_square_index + 1:]
                        array_sizes = []

            line_new = re.sub(r'Arrays.fill\(\s*([^,]+)\s*,\s*([^,]+)\s*\)', r'\g<1> = array_fill(0, sizeof(\g<1>), \g<2>)', line_new)
            line_new = re.sub(r'Arrays.copyOf\(\s*([^,]+)\s*,\s*([^,]+)\s*\)', r'array_slice(\g<1>, 0, \g<2>)', line_new)

            if 'new' in line_new:
                line_new = re.sub(r'new LinkedHashSet<>', r'removeDuplicatesInArray', line_new)
                if re.search(r'new [A-Z][\w.]+\[]\[]\s*{\s*$', line_new):
                    line_new = re.sub(r'new [\w.]+\[]\[*]*\[*]*\s*{\s*$', r'array(', line_new)
                line_new = re.sub(r'new [\w.]+\[]\[]\s*{(.+?)}', r'array(\g<1>)', line_new)
                line_new = re.sub(r'new [\w.]+\[]\s*{\s*$', r'array(', line_new)
                line_new = re.sub(r'new [\w.]+\[]\s*{(.+?)}', r'array(\g<1>)', line_new)
                line_new = re.sub(r'new [\w.]+\[]\s*{}', r'array()', line_new)
                line_new = re.sub(r'new [\w.]+\[\d+]\s*;', r'array();', line_new)
                line_new = re.sub(r'new (Linked|Array)List<>\(([^,)]+?)\)', r'\g<2>', line_new)
                line_new = re.sub(r'new (LinkedList<>|ArrayList<>|HashMap<>|StringBuilder)', 'array', line_new)

            line_new = re.sub(r'};', r');', line_new)
            line_new = re.sub(r'([^.\s]+)\.put\(([^,]+),([^,]+)\)', r'\g<1>[\g<2>] = \g<3>', line_new)

            if '{' in line_new:
                curly_index = 0
                complementary_square_index = 0
                while curly_index != -1 and complementary_square_index >= curly_index:
                    curly_index = line_new[complementary_square_index:].find('{')
                    if curly_index == -1: break
                    complementary_square_index = find_complementary_char_index('}', curly_index, 'right', line_new)
                    if complementary_square_index == -1: break

                    is_array_size = not re.search(r'\)\s*$', line_new[:curly_index])
                    if is_array_size:
                        line_new = line_new[:curly_index] + 'array(' + line_new[curly_index + 1:complementary_square_index] + ')' + line_new[complementary_square_index + 1:]

            # java objects & getters/setters/is
            # line_new = re.sub(r'\b(List<[^>]+>|List<List<[^>]+>>|List<List<List<[^>]+>>>|int|long|char|boolean|long|[A-Z][a-z][\w.]+)\[*\]*\[*\]*\s+', '', line_new)

            line_new = re.sub(r'\.set\((.+?)\s*,\s*(.+?)\)', r'[\g<1>] = \g<2>', line_new)

            line_new = re.sub(r'\.get([A-Z]\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line_new)
            if re.search(r'\.set([A-Z]\w+)\((.+?)\)', line_new):
                line_new = re.sub(r'(\.set\w+)\((.+?)\)', r'\g<1>() = \g<2>', line_new)
                line_new = re.sub(r'\.set(\w+)\(\)', lambda match: f'->{match.group(1)[0].lower() + match.group(1)[1:]}', line_new)

            line_new = re.sub(r'\.(is\w+)\(\)', r'->\g<1>', line_new)

            # object manipulations
            # line_new = re.sub(r'([\w$]+)\.length\b[^(]', r'sizeof(\g<1>)', line_new)
            line_new = re.sub(r'Arrays.asList\(([^)]+)\)', r'array(\g<1>)', line_new)
            line_new = re.sub(r'\b[A-Z][\w.]+\.([A-Z]\w+)\b', r'\g<1>', line_new)

            if 'if (phonemes.length == 2) {' in line_old:
                a = 1
            if re.search(r'\w+(\(.*\)|\w+)', line_new) and not re.search(r'function', line_new):
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
            line_new = add_dollars_in_text_incl_quotes(line_new)
            line_new = re.sub(r'catch\s*\((\$[a-z])', r'catch (Exception \g<1>', line_new)
            line_new = re.sub(r'catch\s*\(Exception ([a-z])', r'catch (Exception $\g<1>', line_new)
            line_new = re.sub(r'->\$', r'->', line_new)

            # removing class closing bracket
            line_new = re.sub(r'^}', r'', line_new)

            # removing extra empty lines
            if line_new or last_line: content_new.append(line_new)
            last_line = line_new

        php_name = java_name + '.php'
        Globals.write_to_file('w+', f'{PATH_PHP}/{php_name}', '<?php\n' + '\n'.join(content_new) + '\n?>')


main()
