import unittest
from pdfminer import utils


class TestUtilities(unittest.TestCase):

    def test_url_basic(self):
        test_url = utils.url("testsite.com/search?", name="John", lastname="Doe", age="25")
        self.assertEqual(test_url, "testsite.com/search?name=John&lastname=Doe&age=25")

    def test_url_special_characters(self):
        test_url = utils.url("testsite.com/search?", name="Äööl_&==??!!  ")
        self.assertEqual(test_url,
                         "testsite.com/search?name=%C3%84%C3%B6%C3%B6l_%26%3D%3D%3F%3F%21%21++")

    def test_url_empty(self):
        test_url = utils.url("testsite.com/search?", name="")
        self.assertEqual(test_url, "testsite.com/search?name=")

    def test_mult_matrix(self):
        test_matrix = utils.mult_matrix((1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12))
        self.assertEqual(test_matrix, (25, 28, 57, 64, 100, 112))

    def test_translate_matrix(self):
        test_matrix = utils.translate_matrix((1, 2, 3, 4, 5, 6), (7, 8))
        self.assertEqual(test_matrix, (1, 2, 3, 4, 36, 52))

    def test_apply_matrix_pt(self):
        test_matrix = utils.apply_matrix_pt((1, 2, 3, 4, 5, 6), (7, 8))
        self.assertEqual(test_matrix, (36, 52))

    def test_apply_matrix_norm(self):
        test_matrix = utils.apply_matrix_norm((1, 2, 3, 4, 5, 6), (7, 8))
        self.assertEqual(test_matrix, (31, 46))

    def test_matrix2str(self):
        test_matrix = utils.matrix2str((1, 2, 3, 4, 5, 6))
        self.assertEqual('[1.00,2.00,3.00,4.00, (5.00,6.00)]', test_matrix)

    def test_uniq(self):
        test_list = [1, 2, 3, 3, 3, 4, 4, 5, 6, 1]
        unique_list = utils.uniq(test_list)
        self.assertEqual(list(unique_list), [1, 2, 3, 4, 5, 6])

    def test_get_bound(self):
        test_box = ((1, 2), (3, 4), (5, 6), (7, 8))
        bounds = utils.get_bound(test_box)
        self.assertEqual(bounds, (1, 2, 7, 8))

    def test_unpack_bytes(self):
        unpacked_byte = utils.nunpack(b'0')
        self.assertEqual(unpacked_byte, 48)

        unpacked_byte = utils.nunpack(b'')
        self.assertEqual(unpacked_byte, 0)

        unpacked_byte = utils.nunpack(b'00')
        self.assertEqual(unpacked_byte, 12336)

        unpacked_byte = utils.nunpack(b'000')
        self.assertEqual(unpacked_byte, 3158064)

        unpacked_byte = utils.nunpack(b'0000')
        self.assertEqual(unpacked_byte, 808464432)

        self.assertRaises(TypeError, utils.nunpack, b'00000')


if __name__ == '__main__':
    unittest.main()
