import unittest
import os

from pdfminer.image import BMPWriter


class TestPngWriter(unittest.TestCase):

    def test_write_bmp(self):
        filename = os.path.join(
            os.path.dirname(__file__),
            'test_files/test_bmp.bmp'
            )
        fp = open(filename, 'wb')
        bmp = BMPWriter(fp, 8, 10, 10)
        bmp.write_line(0, b'0')
        fp.close()
        self.assertTrue(os.path.isfile(filename))


if __name__ == '__main__':
    unittest.main()
