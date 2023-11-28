import unittest
import pytest
from src.pyencry.image_handler import ImageHandler

class ImageHandlerTests(unittest.TestCase):
    def test_can_import_image(self):
        expected = {"filename": "./img/TechSmith-Blog-JPGvsPNG-DE.png", "format": "PNG", "mode": "RGB", "size": (1536, 1152)}
        image_handler = ImageHandler("./img/TechSmith-Blog-JPGvsPNG-DE.png")
        result = image_handler.file_info()
        self.assertEqual(result, expected)

    def test_can_import_image_from_base64(self):
        expected = {"filename": None, "format": "PNG", "mode": "RGB", "size": (1536, 1152)}
        with open("./img/TechSmith-Blog-JPGvsPNG-DE.png", "rb") as file:
            image_handler = ImageHandler.from_base64(file.read())
            result = image_handler.file_info()
        self.assertEqual(result, expected)

    def test_error_when_importing_other_than_png(self):
        with self.assertRaises(ValueError):
            ImageHandler("./img/error_file.jpg")

    


