import re

# TODO Unit test these
def remove_punctuation_and_trim(t):
    # Note that we aren't doing general text preprocessing here. We are only looking for spoken slug labels
    # e.g., 1,2,3,4,3,2. -> 123432
    return re.sub(r"(,|!|\.|\?|-)+","",t).replace(" ","")

def is_numeric_slug_identifier(t): 
    # TODO make sure this regexp matches **only** a sequence of numerals (no text allowed)
    return isinstance(t,str) and re.match(r"[0-9]{5,8}",t) is not None

def label_phrases_with_spoken_slugs(transcripts, is_label=is_numeric_slug_identifier, preprocess_text=remove_punctuation_and_trim):
    # eventually we may want to allow several transcripts (created using different approaches) to be combined
    transcript = transcripts[0]

    return transcript.map_label_text(preprocess_text).filter(lambda l: is_label(l.text))


