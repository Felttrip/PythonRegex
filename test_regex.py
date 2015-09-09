import unittest
import regex


class TestRegex(unittest.TestCase):

    def test_single_letter(self):
        p = regex.build_regex("a")
        result = regex.match(p, "a")
        self.assertTrue(result)

    def test_single_letter_in_long_string(self):
        p = regex.build_regex("a")
        result = regex.match(p, "abcde")
        self.assertTrue(result)

    def test_single_letter_in_middle_of_long_string(self):
        p = regex.build_regex("c")
        result = regex.match(p, "abcde")
        self.assertTrue(result)

    def test_single_letter_at_end_of_long_string(self):
        p = regex.build_regex("e")
        result = regex.match(p, "abcde")
        self.assertTrue(result)

    def test_letter_not_in_string(self):
        p = regex.build_regex("e")
        result = regex.match(p, "abcd")
        self.assertFalse(result)

    def test_char_pattern_in_string(self):
        p = regex.build_regex("This")
        result = regex.match(p, "Is This The Real Life")
        self.assertTrue(result)


    def test_match_any_char(self):
        p = regex.build_regex(".")
        result = regex.match(p, "a")
        self.assertTrue(result)

    def test_match_any_char_longer(self):
        p = regex.build_regex("a.c")
        result = regex.match(p, "abc")
        self.assertTrue(result)

    def test_match_beginning(self):
        p = regex.build_regex(".bc")
        result = regex.match(p, "abc")
        self.assertTrue(result)

    def test_match_any_end(self):
        p = regex.build_regex("ab.")
        result = regex.match(p, "abk")
        self.assertTrue(result)

    def test_match_zero_or_more(self):
        p = regex.build_regex("ab*c")
        result = regex.match(p, "abbbbbbbc")
        self.assertTrue(result)

    def test_match_zero_or_more_begining(self):
        p = regex.build_regex("a*b*c")
        result = regex.match(p, "bbbbbbbc")
        self.assertTrue(result)

    def test_match_zero_or_more_end(self):
        p = regex.build_regex("a*b*c*")
        result = regex.match(p, "bbbbbbb")
        self.assertTrue(result)

    def test_match_zero_or_more_end1(self):
        p = regex.build_regex("a*b*c*")
        result = regex.match(p, "aaaaabbbbbbbc")
        self.assertTrue(result)

    def test_match_zero_or_more_matches_empty(self):
        p = regex.build_regex("a*b*c*")
        result = regex.match(p, "")
        self.assertTrue(result)

    def test_match_zero_or_more_matches_any(self):
        p = regex.build_regex("a.*c")
        result = regex.match(p, "aasdhfjkli ieuxnreu;anjanxeearunjkljadsxnfldjc")
        self.assertTrue(result)

    def test_match_complicated(self):
        p = regex.build_regex("a .og was* wa*lking down .h. stre*t")
        result = regex.match(p, "a dog was walking down the street")
        self.assertTrue(result)

    def test_escaped_chars(self):
        p = regex.build_regex("\*\.")
        result = regex.match(p, "*.")
        self.assertTrue(result)

    def test_exception(self):
        try:
            p = regex.build_regex("**.")
            self.assertTrue(False)
        except SyntaxError:
            self.assertTrue(True)

    def test_one_or_more(self):
        p = regex.build_regex("a+")
        result = regex.match(p, "a")
        self.assertTrue(result)

    def test_one_or_more1(self):
        p = regex.build_regex("a+")
        result = regex.match(p, "aaaa")
        self.assertTrue(result)

    def test_one_or_more2(self):
        p = regex.build_regex("a+")
        result = regex.match(p, "bab")
        self.assertTrue(result)

    def test_one_or_more3(self):
        p = regex.build_regex("a+")
        result = regex.match(p, "b")
        self.assertFalse(result)

    def test_one_or_more_exception(self):
        try:
            p = regex.build_regex("+")
            self.assertTrue(False)
        except SyntaxError:
            self.assertTrue(True)