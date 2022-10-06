import argparse
import sys
from typing import List, Set, Tuple

from pdfminer.converter import FontExtractor
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def get_fontnames(filenames: List[str], password: bytes = b'') -> Set[Tuple[str, str]]:
    fontnames = set()
    for fname in filenames:
        with open(fname, 'rb') as fp:
            rsrcmgr = PDFResourceManager()
            device = FontExtractor()
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, password=password):
                interpreter.process_page(page)
                fontnames.update(device.get_fontnames())
        device.close()
    return fontnames


def print_fontnames(fontnames: Set[Tuple[str, str]]):
    table: List[Tuple[str, str]] = [
        ('Font', 'Type'),
        ('----------------------', '----------------------')
    ]
    table = table + list(fontnames)
    for row in table:
        print("{:<40} {:<20}".format(*row))


def main(argv: List[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', dest='password', default='', type=str)
    parser.add_argument('filenames', nargs='+', type=str)
    try:
        args = parser.parse_args(argv[1:])
    except Exception:
        print(parser.format_help())
        return 1
    fontnames = get_fontnames(args.filenames, password=args.password.encode('utf-8'))
    print_fontnames(fontnames)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
