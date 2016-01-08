from agar.test import BaseTest, WebTest
from utils.iterable_util import delimited_string_to_list


class IterableUtilTest(BaseTest, WebTest):
    def test_comma_delimited_string_to_list_with_goofy_spacing(self):
        email1 = 'admin1@skykit.com'
        email2 = 'admin2@skykit.com'
        email3 = 'admin3@skykit.com'
        comma_delimited_emails = "{0},   {1},{2}".format(email1, email2, email3)
        result = delimited_string_to_list(delimited_string=comma_delimited_emails)
        self.assertLength(3, result)
        self.assertEqual(email1, result[0])
        self.assertEqual(email2, result[1])
        self.assertEqual(email3, result[2])

    def test_comma_delimited_string_to_list_with_expected_no_spacing(self):
        email1 = 'admin1@skykit.com'
        email2 = 'admin2@skykit.com'
        email3 = 'admin3@skykit.com'
        comma_delimited_emails = "{0},{1},{2}".format(email1, email2, email3)
        result = delimited_string_to_list(delimited_string=comma_delimited_emails)
        self.assertLength(3, result)
        self.assertEqual(email1, result[0])
        self.assertEqual(email2, result[1])
        self.assertEqual(email3, result[2])

    def test_comma_delimited_string_with_one_item_and_no_delimiters(self):
        email = 'admin@skykit.com'
        result = delimited_string_to_list(delimited_string=email)
        self.assertLength(1, result)
        self.assertEqual(email, result[0])

    def test_semi_colon_delimited_string_to_list_with_goofy_spacing(self):
        email1 = 'admin1@skykit.com'
        email2 = 'admin2@skykit.com'
        email3 = 'admin3@skykit.com'
        semi_colon_delimited_emails = "{0};   {1};{2}".format(email1, email2, email3)
        result = delimited_string_to_list(delimited_string=semi_colon_delimited_emails, delimiter=';')
        self.assertLength(3, result)
        self.assertEqual(email1, result[0])
        self.assertEqual(email2, result[1])
        self.assertEqual(email3, result[2])

    def test_semi_colon_delimited_string_to_list_with_expected_no_spacing(self):
        email1 = 'admin1@skykit.com'
        email2 = 'admin2@skykit.com'
        email3 = 'admin3@skykit.com'
        semi_colon_delimited_emails = "{0};{1};{2}".format(email1, email2, email3)
        result = delimited_string_to_list(semi_colon_delimited_emails, ';')
        self.assertLength(3, result)
        self.assertEqual(email1, result[0])
        self.assertEqual(email2, result[1])
        self.assertEqual(email3, result[2])

    def test_delimited_string_with_one_item_and_no_delimiters(self):
        email = 'admin@skykit.com'
        result = delimited_string_to_list(email, ';')
        self.assertLength(1, result)
        self.assertEqual(email, result[0])

    def test_passing_empty_string(self):
        result = delimited_string_to_list('')
        self.assertLength(0, result)

    def test_passing_none(self):
        result = delimited_string_to_list(None)
        self.assertLength(0, result)
