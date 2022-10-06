import unittest
import os

from line_profiler import LineProfiler
from memory_profiler import LineProfiler as MemProfiler, show_results

from pdfminer.layout import LAParams
from tools import dumppdf
from tools.pdf2txt import (
    convert_from_pdf,
    ConverterParams,
    OutputType,
    split_by_chapters
    )


# These tests are here specifically so they won't run with the other tests.
# Time and memory tests have very strange effects on coverage reports
# So only run these tests manually.
class TestPDF2Text(unittest.TestCase):

    def setUp(self):
        self.path_simple1_pdf = [os.path.join(os.path.dirname(__file__), '../samples/simple1.pdf')]

        self.course_book_txt_file = os.path.join(
            os.path.dirname(__file__),
            '../samples/samples_for_chapter_retrieval/course_book_full.txt'
        )

    def test_convert_from_pdf_text_time(self):

        lp = LineProfiler()
        lp_wrapper = lp(convert_from_pdf)

        test_filename = os.path.join(
            os.path.dirname(__file__),
            'test_files/test_convert_from_pdf_text_result.txt'
        )

        lp_wrapper(
            self.path_simple1_pdf, ConverterParams(pagenos=set(), laparams=LAParams()),
            OutputType.TEXT, test_filename
        )

        lp.print_stats()

    def test_convert_from_pdf_text_memory(self):

        mp = MemProfiler()
        mp_wrapper = mp(convert_from_pdf)

        test_filename = os.path.join(
            os.path.dirname(__file__),
            'test_files/test_convert_from_pdf_text_result.txt'
        )

        mp_wrapper(
            self.path_simple1_pdf, ConverterParams(pagenos=set(), laparams=LAParams()),
            OutputType.TEXT, test_filename
        )

        show_results(mp)

    def test_split_txt_file_by_chapters_time(self):
        lp = LineProfiler()
        lp_wrapper = lp(split_by_chapters)
        lp_wrapper(self.course_book_txt_file)
        lp.print_stats()

    def test_split_txt_file_by_chapters_memory(self):
        mp = MemProfiler()
        mp_wrapper = mp(split_by_chapters)
        mp_wrapper(self.course_book_txt_file)
        show_results(mp)


class TestDumpPdf(unittest.TestCase):

    def setUp(self) -> None:

        self.course_book_pdf_file = os.path.join(
            os.path.dirname(__file__),
            '../samples/samples_for_chapter_retrieval/course_book_full.pdf'
        )

    def test_line_profiler(self):
        lp = LineProfiler()
        lp_wrapper = lp(dumppdf.get_chapters_from_outline)
        lp_wrapper(self.course_book_pdf_file)
        lp.print_stats(output_unit=1)

    def test_memory_profiler(self):
        mp = MemProfiler()
        mp_wrapper = mp(dumppdf.get_chapters_from_outline)
        mp_wrapper(self.course_book_pdf_file)
        show_results(mp)


if __name__ == '__main__':
    unittest.main()
