import unittest
from data_ingestion.label_phrases_with_spoken_slugs import remove_punctuation_and_trim

class RemovePunctuationAndTrimTest(unittest.TestCase):
    def test_that_it_replaces_commas(self):
        input = 'a,b,c,d,e'

        result = remove_punctuation_and_trim(input)

        self.assertEquals('abcde',result)