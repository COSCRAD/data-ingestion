import re

# TODO Unit test these
def remove_punctuation_and_trim(t):
    # Note that we aren't doing general text preprocessing here. We are only looking for spoken slug labels
    # e.g., 1,2,3,4,3,2. -> 123432
    return re.sub(r"(,|!|\.|\?|-)+","",t).replace(" ","")

written_numerals = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0"

}

def replace_words_with_numerals(t):
    # TODO do this more efficiently
    for w,n in written_numerals.items():
        t = re.sub(w,n,t,flags=re.IGNORECASE)
    
    return t

def default_preprocess_text(t):
    return remove_punctuation_and_trim(replace_words_with_numerals(t))


def is_numeric_slug_identifier(t): 
    # TODO make sure this regexp matches **only** a sequence of numerals (no text allowed)
    return isinstance(t,str) and re.match(r"[0-9]{5,8}",t) is not None

def label_phrases_with_spoken_slugs(transcripts, is_label=is_numeric_slug_identifier, preprocess_text=default_preprocess_text):
    # eventually we may want to allow several transcripts (created using different approaches) to be combined
    transcript = transcripts[0]

    return transcript.map_label_text(preprocess_text).filter(lambda l: is_label(l.text))


