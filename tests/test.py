from unittest import TestCase

from Parser.Instagram_all import InstaParser


class UtilsTestCase(TestCase):

    def test_filename_prefix(self):
        obj = InstaParser(user_id=485935382)
        r = obj.id_to_login()
        self.assertTrue(r == 'khachatryan_jr')