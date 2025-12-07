import os
import unittest

from app import app
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_citation_by_id, create_citation, remove_citation, save_citation, citation_name_exists

os.environ["TEST_ENV"] = "true"

class TestInitialCitationDatabase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()
    
    def test_initial_database_empty(self):
        citations = get_citations()
        self.assertEqual(len(citations), 0)

    def test_create_citation_saves_to_db(self):
        fields = {
            "name": "test-citation",
            "citation_type": "article",
            "author": "A",
            "title": "T",
            "year": "2024"
        }
        create_citation(fields)
        citations = get_citations()
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].get_field("name"), "test-citation")

class TestExistingCitationDatabase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()
        app.testing = True
        self.client = app.test_client()
        create_citation(self.ref_fields())

    def ref_fields(self, **overrides):
        base_ref_fields = {
            "name": "test-citation",
            "citation_type": "article",
            "author": "A",
            "title": "T",
            "journal": "J",
            "year": "2024",
            "volume": "1",
            "number": "1",
            "pages": "1-10",
        }
        base_ref_fields.update(overrides)
        return base_ref_fields
    
    def tearDown(self):
        self.app_context.pop()

    def test_create_citation_sets_id(self):
        self.assertIsNotNone(get_citations()[0].get_field("id"))

    def test_find_citation_by_id(self):
        citation_id = get_citations()[0].get_field("id")
        citation = get_citation_by_id(citation_id)
        self.assertIsNotNone(citation)
        self.assertEqual(citation.get_field("name"), "test-citation")

    def test_create_citation_sets_unique_id(self):
        fields = self.ref_fields(name="another-citation")
        create_citation(fields)
        citations = get_citations()
        self.assertNotEqual(citations[0].get_field("id"), citations[1].get_field("id"))

    def test_create_citation_with_not_unique_name_does_nothing(self):
        fields = self.ref_fields()
        self.assertRaises(Exception, create_citation, fields)

    def test_find_citation_by_id_not_found(self):
        citation_id = get_citations()[0].get_field("id")
        self.assertNotEqual(citation_id, 9999)
        citation = get_citation_by_id(9999)
        self.assertIsNone(citation)

    def test_no_citations_removed_from_db_if_id_none(self):
        self.assertEqual(len(get_citations()), 1)
        remove_citation(None)
        self.assertEqual(len(get_citations()), 1)

    def test_citation_name_exists(self):
        self.assertTrue(citation_name_exists("test-citation"))
        self.assertFalse(citation_name_exists("non-existing-name"))

    def test_save_citation_updates_existing(self):
        original_citation = get_citations()[0]
        original_author = original_citation.get_field("author")
        original_citation_id = original_citation.get_field("id")
        fields = self.ref_fields(author="B")
        save_citation(fields, original_citation_id)
        updated_citation = get_citation_by_id(original_citation_id)
        self.assertNotEqual(updated_citation.get_field("author"), original_author)
        self.assertEqual(updated_citation.get_field("author"), "B")

    def test_save_citation_with_no_id_does_nothing(self):
        original_citation = get_citations()[0]
        original_author = original_citation.get_field("author")
        original_citation_id = original_citation.get_field("id")
        fields = self.ref_fields(author="C")
        save_citation(fields, None)
        unchanged_citation = get_citation_by_id(original_citation_id)
        self.assertEqual(unchanged_citation.get_field("author"), original_author)

    def test_save_citation_with_no_name_does_nothing(self):
        original_citation = get_citations()[0]
        original_author = original_citation.get_field("author")
        original_citation_id = original_citation.get_field("id")
        fields = self.ref_fields(name=None, author="D")
        save_citation(fields, original_citation_id)
        unchanged_citation = get_citation_by_id(original_citation_id)
        self.assertEqual(unchanged_citation.get_field("author"), original_author)

    def test_save_citation_with_duplicate_name_does_nothing(self):
        create_citation(self.ref_fields(name="other-name"))
        citation_id = get_citations()[1].get_field("id")
        fields = self.ref_fields(name="test-citation", author="E")
        save_citation(fields, citation_id)
        unchanged_citation = get_citation_by_id(citation_id)
        self.assertEqual(unchanged_citation.get_field("name"), "other-name")
        self.assertEqual(len(get_citations()), 2)

