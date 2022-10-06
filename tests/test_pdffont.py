from typing import Set, Tuple
import unittest
from tools.pdffonts import get_fontnames


class TestPDFFont(unittest.TestCase):

    def _test(self, test_pdf_filename, expected: Set[Tuple[str, str]]):
        result = get_fontnames([test_pdf_filename])
        self.assertEqual(result, expected)

    def test_arial(self):
        self._test(
            "./tests/test_files/pdffonts/test_pdffont_arial.pdf",
            {('AAAAAA+ArialMT', 'CID')})

    def test_timesnewroman_arial(self):
        self._test(
            "./tests/test_files/pdffonts/test_pdffont_timesnewroman_arial.pdf",
            {('BAAAAA+ArialMT', 'CID'), ('AAAAAA+TimesNewRomanPSMT', 'CID')})

    def test_timesnewroman_arial_verdana(self):
        self._test(
            "./tests/test_files/pdffonts/test_pdffont_timesnewroman_arial_verdana.pdf",
            {
                ('AAAAAA+TimesNewRomanPSMT', 'CID'),
                ('CAAAAA+Verdana', 'CID'),
                ('BAAAAA+ArialMT', 'CID')
            })


if __name__ == "__main__":
    unittest.main()
