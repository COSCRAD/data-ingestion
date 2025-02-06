import unittest
from data_ingestion.whisper_trascriber import WhisperTranscriber

class WhisperTranscriberTest(unittest.TestCase):
    def test_that_it_transcribes_a_sample_clip(self):
        test_file = "src/test/test_data/media-files/test-for-asr.wav"

        t = WhisperTranscriber()

        result = t.transcribe(test_file)

        # TODO improve upon this sanity check
        self.assertIsNotNone(result)

        transcript = result[0]

        transcript_full_text = str(transcript).lower().replace('\n',' ')
        
        includes_text = "this is only a test" in transcript_full_text

        self.assertEquals(True,includes_text)