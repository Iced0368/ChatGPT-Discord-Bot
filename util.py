import re
from googletrans import Translator

translator = Translator()

def answer_strip(text):
    split = text.split(':', 1)
    if len(split[0]) < 6:
        return split[1]
    else:
        return text


def wrap_block(text, language):
    if not text.strip().startswith('```'):
        text = f'```{language}\n' + text
    if not text.strip().endswith('```'):
        text = text + '```'
    return text

def get_language_name(code_block):
    # Define a regular expression to extract the language name from the code block
    pattern = r"```(\w+)\n"
    match = re.match(pattern, code_block)
    if match:
        return match.group(1)
    else:
        return ''

def split_text(text, is_code_block=False):
    MAX_LENGTH = 1800
    segments = []
    current_segment = ''
    language = get_language_name(text)
    for line in text.split('\n'):
        if len(current_segment + line) > MAX_LENGTH:
            if is_code_block:
                current_segment = wrap_block(current_segment, language)
            segments.append(current_segment.strip())
            current_segment = ''
        current_segment += line + '\n'

    if is_code_block:
        current_segment = wrap_block(current_segment, language)
    segments.append(current_segment.strip())
    return segments


def split_with_code_tags(text):
    code_regex = r"(\`\`\`)"
    parts = re.split(code_regex, text)

    result = []
    in_code_block = False
    for part in parts:
        if part == '```':
            in_code_block = not in_code_block

        elif in_code_block:
            result.append(f'```{part}```')
        else:
            result.append(part)
    return result


def translate_text(text, lang):
    parts = split_with_code_tags(text)
    translated_text = ''
    for part in parts:
        if part.startswith('```') and part.endswith('```'):
            translated_text += part
        else:
            translated_text += translator.translate(part, lang).text
    return translated_text



def text_to_segments(text):
    segments = []
    parts = split_with_code_tags(text)
    for part in parts:
        is_code = part.startswith('```') and part.endswith('```')
        splitted = split_text(part, is_code)
        for split in splitted:
            segments.append(split)
    return segments