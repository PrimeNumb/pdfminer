import unittest
from tools import latin2ascii


class TestLatin2Ascii(unittest.TestCase):

    def test_latin2ascii(self):
        text = 'tüst'
        returned_text = latin2ascii.latin2ascii(text)
        self.assertEqual(returned_text, 'tu:st')

    def test_main_error(self):
        self.assertRaises(IndexError, latin2ascii.main, '')


if __name__ == '__main__':
    unittest.main()
