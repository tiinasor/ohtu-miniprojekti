import os
import unittest

os.environ["TEST_ENV"] = "true"

from app import app
from db_helper import reset_db
from repositories.citation_repository import get_citations


class ValidateCitationTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        reset_db()
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def submit(self, **overrides):
        base = {
            "name": "test",
            "citation_type": "article",
            "author": "A",
            "title": "T",
            "journal": "J",
            "year": "2024",
            "volume": "1",
            "number": "1",
            "pages": "1-10",
        }
        base.update(overrides)
        return self.client.post("/create_citation", data=base, follow_redirects=True)

    """ ----------------- SQL DATABASE TESTS ----------------- """

    def test_sql_create_article_citation(self):
        response = self.submit(name="test-citation")
        citations = get_citations()
        self.assertEqual(len(citations), 1)
        self.assertEqual(citations[0].get_field("name"), "test-citation")
        self.assertIn(b"test-citation", response.data)

    def test_sql_unique_article_citation_name(self):
        self.submit(name="unique-name")
        response = self.submit(name="unique-name")
        citations = get_citations()
        self.assertEqual(len(citations), 1)
        self.assertIn(b"Citation name must be unique", response.data)

    def test_sql_remove_article_citation(self):
        self.submit(name="to-delete")
        citation_id = get_citations()[0].get_field("id")
        response = self.client.post(f"/remove/{citation_id}", data={"remove": "1"}, follow_redirects=True)
        self.assertEqual(len(get_citations()), 0)
        self.assertNotIn(b"to-delete", response.data)

    """ ----------------- FORM VALIDITY TESTS ----------------- """

    def test_article_form_missing_required_fields(self):
        fields = ["name", "author", "title", "journal", "year"]
        for field in fields:
            reset_db()  # Reset database between iterations
            response = self.submit(**{field: ""})
            self.assertEqual(len(get_citations()), 0)
            self.assertIn(b"Missing required fields", response.data)

    def test_article_form_invalid_numeric_fields(self):
        invalids = {
            "year": "abcd",
            "volume": "x.y",
            "number": "xyz",
        }
        for field, bad_value in invalids.items():
            self.submit(name=f"bad-{field}", **{field: bad_value})
            self.assertEqual(len(get_citations()), 0)


if __name__ == "__main__":
    unittest.main()
