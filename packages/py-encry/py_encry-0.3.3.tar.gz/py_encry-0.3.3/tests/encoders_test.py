import unittest
import pytest
from src.pyencry.utils import encode_data_to_pixel, decode_data_from_pixel
from src.pyencry.encoders import encode_rail_fence_cipher

class PixelDataEncodeTests(unittest.TestCase):
    def test_can_encode_pixel(self):

        result = encode_data_to_pixel((38,120,255,0), 0b01011101)

        expected = (37, 121, 255, 1)

        self.assertEqual(result, expected)

class RailFenceEncodeTests(unittest.TestCase):
    def test_can_encode_sentence_rail_fence(self):
        result = encode_rail_fence_cipher("WEAREDISCOVEREDFLEEATONCE", 3)
        expected = "WECRLTEERDSOEEFEAOCAIVDEN"
        self.assertEqual(result, expected)

    def test_can_encode_4_rails_rail_fence(self):
        result = encode_rail_fence_cipher("EXERCISES", 4)
        expected = "ESXIEECSR"
        self.assertEqual(result, expected)

    def test_can_encode_5_rails_rail_fence(self):
        result = encode_rail_fence_cipher("EXERCISMISAWESOME", 5)
        expected = "EIEXMSMESAORIWSCE"
        self.assertEqual(result, expected)

    def test_can_encode_6_rails_rail_fence(self):
        result = encode_rail_fence_cipher("112358132134558914423337761098715972584418167651094617711286", 6)
        expected = "133714114238148966225439541018335470986172518171757571896261"
        self.assertEqual(result, expected)  