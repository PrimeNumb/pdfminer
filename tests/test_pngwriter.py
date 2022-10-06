from pdfminer.image import (
    PngWriter
)
import unittest
import os
from PIL import Image

class TestPngWriter(unittest.TestCase):

    def setUp(self):
        writer = PngWriter("tests/test_files/testImage.png", 200, 200) 
        writer.write("")
    
    def test_png_write_basic(self):
        self.assertTrue(os.path.exists("tests/test_files/testImage.png"))
    
    def test_png_dimensions(self):
        img = Image.open("tests/test_files/testImage.png")
        self.assertTrue(img.width == 200)
        self.assertTrue(img.height == 200)

    def tearDown(self) -> None:
        os.remove("tests/test_files/testImage.png")
        






