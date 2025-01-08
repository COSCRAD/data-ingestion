import unittest

from data_ingestion.transcript import Transcript
from data_ingestion.audio_label import AudioLabel
from pydub import AudioSegment


class TestTranscript(unittest.TestCase):
    def test_that_build_tsv_rows_raises_exception_for_invalid_tsv(self):
        invalid_tsv = "1.2\t2.4\tgoodone\n1.2\tmissing out point"

        def try_from_tsv():
            Transcript.from_tsv_rows()

        self.assertRaises(Exception, try_from_tsv)

    def test_building_from_tsv(self):
        in_points = [1.2, 2.2, 3.45]
        out_points = [2.0, 2.849, 4]
        text_for_labels = ["this was said", "so was this", "omit_this_one"]
        tsv = [
            f"{in_point}\t{out_point}\t{label}"
            for in_point, out_point, label in zip(
                in_points, out_points, text_for_labels
            )
        ]

        transcript_name = "My Story"

        audacity_transcript = Transcript.fromTsvRows(tsv, transcript_name)

        first_label = audacity_transcript.labels[0]

        self.assertAlmostEqual(first_label.in_point, in_points[0])

        self.assertAlmostEqual(first_label.out_point, out_points[0])

        self.assertEqual(first_label.text, text_for_labels[0])

        self.assertEqual(audacity_transcript.name, transcript_name)

    def test_filter_that_matches_some_labels(self):
        in_points = [1.2, 2.5, 3.4, 4.5, 6.6]
        out_points = [2.0, 2.8, 4, 5.6, 9.0]
        """
        2.5-2.8 omitted
        4.5-5.6 omitted

        shift result should be
        1.2-2.0 # no shift
        3.1-3.7 # shift .3 left
        5.2-7.6 # shift .3 + 1.1 = 1.4 left
        """
        text_for_labels = [
            "I match",
            "this was said",
            "this one matches",
            "omit_this_one",
            "this one matches too",
        ]

        EXPECTED_NUMBER_OF_MATCHES = 3

        tsv = [
            f"{in_point}\t{out_point}\t{label}"
            for in_point, out_point, label in zip(
                in_points, out_points, text_for_labels
            )
        ]

        transcript_name = "My Story"

        test_transcript = Transcript.fromTsvRows(tsv, transcript_name)

        text_has_match = lambda label: "match" in label.text

        filtered_transcript = test_transcript.filter(text_has_match)

        self.assertEqual(len(filtered_transcript.labels), EXPECTED_NUMBER_OF_MATCHES)

        #  1.2-2.0 # no shift
        first_label = filtered_transcript.labels[0]

        self.assertAlmostEqual(first_label.in_point, 1.2)
        self.assertAlmostEqual(first_label.out_point, 2.0)
        self.assertEqual(first_label.text, text_for_labels[0])

        # 3.1-3.7 # shift .3 left
        second_label = filtered_transcript.labels[1]

        self.assertAlmostEqual(second_label.in_point, 3.1)
        self.assertAlmostEqual(second_label.out_point, 3.7)
        # label[1] should be filtered out
        self.assertEqual(second_label.text, text_for_labels[2])

    def test_sort_when_unsorted(self):
        in_points = [1.2, 2.2, 3.45, 4.5, 6.68]
        out_points = [2.0, 2.849, 4, 5.6, 9.09]
        text_for_labels = [
            "",
            "this was said",
            "this one matches",
            "omit_this_one",
            "this one matches too",
        ]

        EXPECTED_NUMBER_OF_MATCHES = 3

        zipped = [l for l in zip(in_points, out_points, text_for_labels)]

        shuffled = [zipped[4], zipped[3], zipped[1], zipped[0], zipped[2]]

        tsv = [
            f"{in_point}\t{out_point}\t{label}"
            for in_point, out_point, label in shuffled
        ]

        transcript_name = "My Story"

        test_transcript = Transcript.fromTsvRows(tsv, transcript_name)

        # note that the transcsript is mutable
        test_transcript.sort()

        self.assertEqual(len(test_transcript.labels), len(shuffled))

        self.assertAlmostEqual(test_transcript.labels[0].in_point, in_points[0])

        self.assertAlmostEqual(test_transcript.labels[4].in_point, in_points[4])

    def test_assigning_audio(self):
        transcript = Transcript("test transcript")

        full_audio_length = 120000  # ms = 120 s

        full_audio = AudioSegment.silent(full_audio_length)

        end_points_and_labels = [
            [0, 500, "keepers"],
            [500, 1000, "omit this one"],
            [1000, 4000, "I am good"],
            [4000, 90000, "what's up"],
            [90000, 119999.5, "omit me please"],
            [119999.5, full_audio_length, "finally done"],
        ]

        for in_point, out_point, text in end_points_and_labels:
            transcript.append(
                AudioLabel(in_point=in_point, out_point=out_point, text=text)
            )

        transcript.apply_audio(full_audio)

        output_audio = transcript.get_audio()

        # Note that our labels cover the entire audio and we haven't filtered
        self.assertAlmostEqual(len(output_audio), full_audio_length)

    def test_assign_audio_then_filter(self):
        transcript = Transcript("test transcript")

        full_audio_length = 120000  # ms = 120 s

        full_audio = AudioSegment.silent(full_audio_length)

        end_points_and_labels = [
            [0, 500, "keepers"],
            # Remove 500 mss
            [500, 1000, "omit this one"],
            [1000, 4000, "I am good"],
            [4000, 90000, "what's up"],
            # Remove 29999.5 ms
            [90000, 119999.5, "omit me please"],
            [119999.5, full_audio_length, "finally done"],
            # removed 30499.5 ms
        ]

        length_of_removed_audio = 30499.5

        for in_point, out_point, text in end_points_and_labels:
            transcript.append(
                AudioLabel(in_point=in_point, out_point=out_point, text=text)
            )

        transcript.apply_audio(full_audio)

        filtered_transcript = transcript.filter(lambda l: "omit" not in l.text)

        output_audio = filtered_transcript.get_audio()

        # note that it's ok to be off by one ms
        tolerance_ms = 1

        # Note that our labels cover the entire audio and we haven't filtered
        self.assertEqual(
            len(output_audio) - (full_audio_length - length_of_removed_audio)
            < tolerance_ms,
            True,
        )


if __name__ == "__main__":
    unittest.main()
