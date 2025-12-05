import os
import unittest
from entities.citation import Citation


os.environ["TEST_ENV"] = "true"

class TestCitation(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

    def test_citation_creation(self):        
        ref_info = [1,
                    "example-citation",
                    "book",
                    "example address",
                    "example author", 
                    "example exambooktitle", 
                    "example edition", 
                    "example editor", 
                    "example howpublished", 
                    "example journal",
                    "example keywords",
                    "example month", 
                    "example note", 
                    "example number", 
                    "example organization", 
                    "example pages", 
                    "example publisher", 
                    "example school", 
                    "example series", 
                    "example title", 
                    "example type", 
                    "example volume", 
                    "example year"] 
        citation = Citation(ref_info)
        self.assertEqual(citation.id, 1)
        self.assertEqual(citation.get_field("id"), 1)
        self.assertEqual(citation.get_field("name"), "example-citation")
        self.assertEqual(citation.get_field("citation_type"), "book")
        self.assertEqual(citation.get_field("author"), "example author")
        self.assertEqual(citation.get_field("title"), "example title")
        self.assertEqual(citation.get_field("journal"), "example journal")
        self.assertEqual(citation.get_field("year"), "example year")

    def test_get_invalid_field(self):
        ref_info = [2, "example-citation"] + [None for _ in range(23)]
        citation = Citation(ref_info)
        self.assertRaises(ValueError, citation.get_field, "non_existent_field")

if __name__ == "__main__":
    unittest.main()
