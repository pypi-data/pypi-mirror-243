import unittest
import pytest
from src.pyencry.utils import decode_data_from_pixel
from src.pyencry.encoders import encode_rail_fence_cipher
from src.pyencry.decoders import decode_rail_fence_cipher

class PixelDataDecodeTests(unittest.TestCase):
    def test_can_decode_pixel(self):
        result = decode_data_from_pixel((37, 121, 255, 1))
        expected = 0b01011101
        self.assertEqual(result, expected)

class RailFenceDecodeTests(unittest.TestCase):
    def test_can_decode_sentence_rail_fence(self):
        result = decode_rail_fence_cipher("WECRLTEERDSOEEFEAOCAIVDEN", 3)
        expected = "WEAREDISCOVEREDFLEEATONCE"
        self.assertEqual(result, expected)

    def test_can_decode_4_rails_rail_fence(self):
        result = decode_rail_fence_cipher("ESXIEECSR", 4)
        expected = "EXERCISES"
        self.assertEqual(result, expected)

    def test_can_decode_5_rails_rail_fence(self):
        result = decode_rail_fence_cipher("EIEXMSMESAORIWSCE", 5)
        expected = "EXERCISMISAWESOME"
        self.assertEqual(result, expected)

    def test_can_decode_6_rails_rail_fence(self):
        result = decode_rail_fence_cipher("133714114238148966225439541018335470986172518171757571896261", 6)
        expected = "112358132134558914423337761098715972584418167651094617711286"
        self.assertEqual(result, expected)

    def test_can_encode_then_decode(self):
        message = "This is a secret message"
        rails = 4
        encoded = encode_rail_fence_cipher(message, rails)
        decoded = decode_rail_fence_cipher(encoded, rails)
        self.assertEqual(message, decoded)
