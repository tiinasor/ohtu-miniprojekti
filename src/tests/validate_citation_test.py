import unittest
from util import validate_citation, UserInputError

class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_length_does_not_raise_error(self):
        validate_citation("juokse")
        validate_citation("a" * 100)

    def test_too_short_or_long_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_citation("ole")

        with self.assertRaises(UserInputError):
            validate_citation("koodaa" * 20)
