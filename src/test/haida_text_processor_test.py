import unittest
from data_ingestion.haida_text_processor import convert_optima_haidatron_to_standard_orthography

class HaidaTextProcessorTest(unittest.TestCase):
    def test_that_it_replaces_all_special_symbols(self):
        consonants_with_standard_characters = [
            'b',
            'ch',
            'd',
            'dl',
            'g',
            'h',
            'hl',
            'j',
            'k',
            "k'", # TODO check that ' is the correct char
            "'l", # TODO check that ' is the correct char
            "m",
            "n",
            "ng",
            "p",
            "s",
            "t",
            "t'",
            "tl",
            "tl'", # TODO check that ' is the correct char
            "ts'", # TODO check that ' is the correct char
            ".",
            "w",
            "x",
            "y",
        ]

        # no vowels require special symbols
        vowels = [
            'a',
            'aa',
            'aw',
            'aaw',
            'ay',
            'aay',
            'ey',
            'i',
            'ii',
            'l',
            'll',
            'o',
            'u',
            'uu',
            'yaa'
        ]

        consonants_with_standard_characters_in_sequence = "".join(consonants_with_standard_characters)

        vowels_in_sequence = "".join(vowels)

        # We include all non-replaced alphabet characters here as well
        input = f'{consonants_with_standard_characters_in_sequence}ÑñÝýÇçÞþÐð{vowels_in_sequence}'

        # TODO are there any edge-cases where text is actually English \ bilingual and we get unwanted replacements?

        expected_output = f'{consonants_with_standard_characters_in_sequence}K̲k̲X̲x̲G̲ɢ̲X̂x̂Ĝɢ̂{vowels_in_sequence}'

        result = convert_optima_haidatron_to_standard_orthography(input)

        self.assertEqual(result,expected_output)

    def test_that_it_handles_pinched_consonants(self):
        input = "Ñ'ñ'"

        expected_output = "K̲'k̲'"

        result = convert_optima_haidatron_to_standard_orthography(input)

        self.assertEqual(result,expected_output)