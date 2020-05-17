from unittest import TestCase

from parsering.instagram_all import InstaParser


class UtilsTestCase(TestCase):

    def test_filename_prefix(self):
        obj = InstaParser(user_id=485935382)
        r = obj.id_to_login()
        self.assertTrue(r == 'khachatryan_jr')

    def test_filename_prefix(self):
        obj = InstaParser(user_id=485935391)
        r = obj.id_to_login()
        self.assertTrue(r != 'khachatryan_jr')
