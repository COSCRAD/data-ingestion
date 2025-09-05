def convert_optima_haidatron_to_standard_orthography(optima_haidatron_text):
    replacements = {
        "Ñ": "K̲",
        "ñ": "k̲",
        "Ý": "X̲",
        "ý": "x̲",
        "Ç": "G̲",
        "ç": "ɢ̲",
        "Þ": "X̂",
        "þ": "x̂",
        "Ð": "Ĝ",
        "ð": "ɢ̂"
        }
    
    output_chars = []

    for c in optima_haidatron_text:
        # if the char is not in the replacement list, we append the char without replacement
        output_chars.append(replacements.get(c,c))

    return ''.join(output_chars)