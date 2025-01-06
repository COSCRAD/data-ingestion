import unittest

from data_ingestion.audio_label import AudioLabel

class TestAudioLabel(unittest.TestCase):
    def test_building_new_label(self):
        # arrange
        in_point = 1234.5

        out_point = in_point + 1000.3

        text = "here is what was said"

        # act
        label = AudioLabel(in_point=in_point,out_point=out_point,text=text)

        # assert
        self.assertEqual(label.in_point,in_point)

        self.assertEqual(label.out_point,out_point)

        self.assertEqual(label.text,text)

    def test_shifting_of_labels(self):
        # arrange 
        in_point = 1234.5

        out_point = in_point + 1000.3 # 2234.8

        text = "here is what was said"

        label = AudioLabel(in_point=in_point,out_point=out_point,text=text)

        delta = 0.2

        # act
        label.shift(delta)

        # assert
        self.assertAlmostEqual(label.in_point,1234.3)

        self.assertAlmostEqual(label.out_point,2234.6)

    def test_length(self):
        label = AudioLabel(1.23,99.35,"text")

        self.assertAlmostEqual(label.length(),98.12)
        

if __name__ == '__main__':
    unittest.main()
