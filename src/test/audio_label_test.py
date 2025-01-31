import unittest
from pydub import AudioSegment

from data_ingestion.audio_label import AudioLabel


class TestAudioLabel(unittest.TestCase):
    def test_building_new_label(self):
        # arrange
        in_point = 1234.5

        out_point = in_point + 1000.3

        text = "here is what was said"

        initials = "AP"

        # act
        label = AudioLabel(
            in_point=in_point, out_point=out_point, text=text, speaker_initials=initials
        )

        # assert
        self.assertEqual(label.in_point, in_point)

        self.assertEqual(label.out_point, out_point)

        self.assertEqual(label.text, text)

        self.assertEqual(label.speaker_initials, initials)

        self.assertEqual(label.has_audio(), False)

    def test_shifting_of_labels(self):
        # arrange
        in_point = 1234.5

        out_point = in_point + 1000.3  # 2234.8

        text = "here is what was said"

        label = AudioLabel(in_point=in_point, out_point=out_point, text=text)

        delta = 0.2

        # act
        label.shift(delta)

        # assert
        self.assertAlmostEqual(label.in_point, 1234.3)

        self.assertAlmostEqual(label.out_point, 2234.6)

    def test_length(self):
        label = AudioLabel(1.23, 99.35, "text")

        self.assertAlmostEqual(label.length(), 98.12)

        self.assertAlmostEqual(label.length(), 98.12)

    def test_assign_audio(self):
        in_point = 1.345
        out_point = 2.345
        text = "here is the text"

        label = AudioLabel(
            in_point=in_point,
            out_point=out_point,
            text=text,
        )
        chunk_length = 1200
        chunk_to_add = AudioSegment.silent(chunk_length)

        label.assign_audio(chunk_to_add)

        self.assertEqual(label.has_audio(), True)

        self.assertAlmostEqual(len(chunk_to_add), len(label.audio))


if __name__ == "__main__":
    unittest.main()
