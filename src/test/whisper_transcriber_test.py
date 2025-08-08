import unittest
from data_ingestion.whisper_trascriber import WhisperTranscriber
from data_ingestion.label_phrases_with_spoken_slugs import label_phrases_with_spoken_slugs

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

    def test_slug_labelled_clip_transcription(self):
        test_file = "src/test/test_data/media-files/test-for-asr_slug-labelled-list.wav"

        t = WhisperTranscriber()

        transcript, _raw_transcript = t.transcribe(test_file)

        transcript_for_slugs = label_phrases_with_spoken_slugs([transcript])

        audacity_labels = transcript_for_slugs.to_audacity_labels()

        self.assertIsNotNone(audacity_labels)

        # You can visually inspect this file 
        with open ("src/test/test_data/test_slug_labelled_clip_transcription.txt",'w') as f:
            f.write(audacity_labels)


