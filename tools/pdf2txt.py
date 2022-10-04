#!/usr/bin/env python
import sys
import getopt

import pdfminer.image
from pdfminer.cmapdb import CMapDB
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
from typing import List, Tuple, Union, Set
from dataclasses import dataclass
from enum import Enum

import re

from pdfminer.pdfparser import PDFParser


@dataclass
class ConverterParams:
    pagenos: Set
    laparams: pdfminer.layout.LAParams
    debug: int = 0
    password: bytes = b''
    maxpages: int = 0
    imagewriter: Union[pdfminer.image.ImageWriter, None] = None
    rotation: int = 0
    stripcontrol: bool = False
    layoutmode: str = 'normal'
    encoding: str = 'utf-8'
    pageno: int = 1
    scale: int = 1
    caching: bool = True
    showpageno: bool = True
    get_chapters: bool = False


class OutputType(Enum):
    TEXT = "text"
    HTML = "html"
    XML = "xml"
    TAG = "tag"


def _print_help_message(command: str = ""):
    print(f'usage: {command} [-P password] [-o output] [-t text|html|xml|tag]'
          ' [-O output_dir] [-c encoding] [-s scale] [-R rotation]'
          ' [-Y normal|loose|exact] [-p pagenos] [-m maxpages]'
          ' [-S] [-C] [-n] [-A] [-V] [-h] [-M char_margin] [-L line_margin]'
          ' [-W word_margin] [-F boxes_flow] [-d] input.pdf ...')


def handle_input_variables(
    options: List[Tuple[str, str]],
    filenames: List[str],
    command_name: str = ""): \

    # input option
    converter_params = ConverterParams(pagenos=set(), laparams=LAParams())

    # output option
    outfile = None
    outtype: Union[OutputType, None] = None

    for (k, v) in options:
        if k == '-d':
            ConverterParams.debug += 1
        elif k == '-P':
            ConverterParams.password = v.encode('ascii')
        elif k == '-o':
            outfile = v
        elif k == '-t':
            outtype = OutputType(v)
        elif k == '-O':
            ConverterParams.imagewriter = ImageWriter(v)
        elif k == '-c':
            ConverterParams.encoding = v
        elif k == '-s':
            ConverterParams.scale = float(v)
        elif k == '-R':
            ConverterParams.rotation = int(v)
        elif k == '-Y':
            ConverterParams.layoutmode = v
        elif k == '-p':
            ConverterParams.pagenos.update(int(x) - 1 for x in v.split(','))
        elif k == '-m':
            ConverterParams.maxpages = int(v)
        elif k == '-S':
            ConverterParams.stripcontrol = True
        elif k == '-C':
            ConverterParams.caching = False
        elif k == '-n':
            ConverterParams.laparams = None
        elif k == '-A':
            ConverterParams.laparams.all_texts = True
        elif k == '-V':
            ConverterParams.laparams.detect_vertical = True
        elif k == '-M':
            ConverterParams.laparams.char_margin = float(v)
        elif k == '-W':
            ConverterParams.laparams.word_margin = float(v)
        elif k == '-L':
            ConverterParams.laparams.line_margin = float(v)
        elif k == '-F':
            ConverterParams.laparams.boxes_flow = float(v)
        elif k == '-h':
            ConverterParams.get_chapters = True

    # Special considerations if the user wants to generate the book chapters as txt.
    if ConverterParams.get_chapters:
        chapters = split_by_chapters(filenames[0])
        write_chapters_to_files(chapters, outfile)
        return
    convert_from_pdf(filenames, converter_params, outtype, outfile)


def convert_from_pdf(filenames: List[str],
                     params: ConverterParams,
                     outtype: Union[OutputType, None] = None,
                     outfile: Union[str, None] = None) -> Union[None, int]:
    PDFDocument.debug = params.debug
    PDFParser.debug = params.debug
    CMapDB.debug = params.debug
    PDFPageInterpreter.debug = params.debug
    rsrcmgr = PDFResourceManager(caching=params.caching)
    if not outtype:
        outtype = OutputType.TEXT
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = OutputType.HTML
            elif outfile.endswith('.xml'):
                outtype = OutputType.XML
            elif outfile.endswith('.tag'):
                outtype = OutputType.TAG

    outfp = (
        open(outfile, 'w', encoding=params.encoding) if outfile else sys.stdout
    )

    if outtype == OutputType.TEXT:
        device = TextConverter(rsrcmgr, outfp, laparams=params.laparams,
                               imagewriter=params.imagewriter)
    elif outtype == OutputType.XML:
        device = XMLConverter(rsrcmgr, outfp, laparams=params.laparams,
                              imagewriter=params.imagewriter,
                              stripcontrol=params.stripcontrol)
    elif outtype == OutputType.HTML:
        device = HTMLConverter(rsrcmgr, outfp, scale=params.scale,
                               layoutmode=params.layoutmode,
                               laparams=params.laparams,
                               imagewriter=params.imagewriter,
                               debug=params.debug)
    elif outtype == OutputType.TAG:
        device = TagExtractor(rsrcmgr, outfp)
    else:
        _print_help_message()
        return 100

    for fname in filenames:
        with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, params.pagenos,
                                          maxpages=params.maxpages,
                                          password=params.password,
                                          caching=params.caching,
                                          check_extractable=True):
                page.rotate = (page.rotate + params.rotation) % 360
                interpreter.process_page(page)

    device.close()
    outfp.close()


def split_by_chapters(file_name: str) -> List[str]:
    if not file_name.endswith('.txt'):
        raise Exception('File type must be Text File')
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chapter = 0

    chapters = [""]

    for line_nr in range(0, len(lines) - 1):

        curr_line, next_line = lines[line_nr], lines[line_nr + 1]

        if 'Chapter' in curr_line:
            if next_line == '\n':
                is_number = re.compile(r'\d+$')  # Find number and only number
                chapter_number = curr_line.split('Chapter')[1].strip()

                if is_number.match(chapter_number):
                    chapter += 1
                    chapters.append('')
        chapters[chapter] += curr_line

    return chapters


def write_chapters_to_files(chapters: List[str], path='') -> None:
    index = 0
    for chapter in chapters:
        chapter_name = 'introduction.txt' if index == 0 else 'chapter' + str(index) + '.txt'
        with open(path + chapter_name, 'w', encoding='utf-8') as f:
            f.write(chapter)
        index += 1


def main(argv):
    try:
        options, filenames = getopt.getopt(
            argv[1:],
            'dP:o:t:O:c:s:R:Y:p:m:SCnAVM:W:L:F:h:'
        )
        handle_input_variables(options, filenames)
    except getopt.GetoptError:
        _print_help_message()
        return 100
    if not filenames:
        _print_help_message()
        return 100


if __name__ == '__main__':
    sys.exit(main(sys.argv))
