import os
import unittest
from entities.citation import Citation


os.environ["TEST_ENV"] = "true"

class TestCitation(unittest.TestCase):

    def ref_info(self):
        return [1,
                "example-name",
                "misc",
                "example address",
                "example author", 
                "example booktitle"] + [None for _ in range(23)]

    def test_citation_creation(self):
        citation = Citation(self.ref_info())
        self.assertEqual(citation.id, 1)
        self.assertEqual(citation.get_field("id"), 1)
        self.assertEqual(citation.get_field("name"), "example-name")
        self.assertEqual(citation.get_field("citation_type"), "misc")
        self.assertEqual(citation.get_field("author"), "example author")


    def test_get_invalid_field(self):
        citation = Citation(self.ref_info())
        self.assertRaises(ValueError, citation.get_field, "non_existent_field")

if __name__ == "__main__":
    unittest.main()

