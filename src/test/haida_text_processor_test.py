import unittest
from data_ingestion.haida_text_processor import convert_optima_haidatron_to_standard_orthography

class HaidaTextProcessorTest(unittest.TestCase):
    def test_that_it_replaces_all_special_symbols(self):
        # TODO include all characters common to both keysets
        input = 'aÑñÝýÇçÞþÐði'

        expected_output = 'aK̲k̲X̲x̲G̲ɢ̲X̂x̂Ĝɢ̂i'

        result = convert_optima_haidatron_to_standard_orthography(input)

        self.assertEqual(result,expected_output)