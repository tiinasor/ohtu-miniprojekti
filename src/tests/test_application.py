import os
import unittest

os.environ["TEST_ENV"] = "true"

from app import app
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_citation_by_id


class TestApplication(unittest.TestCase):
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
            "editor": "E",
            "title": "T",
            "booktitle": "B",
            "school": "S",
            "publisher": "P",
            "journal": "J",
            "year": "2024",
            "volume": "1",
            "pages": "1-10",
        }

        base.update(overrides)
        return self.client.post("/create_citation", data=base, follow_redirects=True)

    def test_create_citation_shows_citation_in_citation_list(self):
        response = self.submit(name="test-citation")
        self.assertIn(b"test-citation", response.data)
    
    """ ----------------- FORM VALIDITY TESTS ----------------- """

    def test_create_citation_works_for_all_citation_types(self):
        citation_types = [
            "article",
            "inproceedings",
            "book",
            "mastersthesis",
            "phdthesis",
            "misc",
        ]
        for ctype in citation_types:
            reset_db()
            response = self.submit(name=f"test-{ctype}", citation_type=ctype)
            self.assertIn(f"test-{ctype}".encode(), response.data)

    def test_nonunique_citation_name_shows_error(self):
        self.submit(name="unique-name")
        response = self.submit(name="unique-name")
        citations = get_citations()
        self.assertEqual(len(citations), 1)
        self.assertIn(b"Citation name must be unique", response.data)

    def test_missing_required_fields_shows_error(self):
        
        required_fields_map = {
            "article": ["name", "author", "title", "journal", "year"],
            "inproceedings": ["name", "author", "title", "booktitle", "year"],
            "mastersthesis": ["name", "author", "title", "school", "year"],
            "phdthesis": ["name", "author", "title", "school", "year"],
            "misc": ["name"],
        }
        for citation_type, required_fields in required_fields_map.items():
            for field in required_fields:
                response = self.submit(citation_type=citation_type, **{field: ""})
                self.assertEqual(len(get_citations()), 0)
                self.assertIn(b"Missing required field:", response.data)
                response = self.submit(citation_type=citation_type, **{field: None})
                self.assertEqual(len(get_citations()), 0)
                self.assertIn(b"Missing required field", response.data)

    def test_invalid_numeric_fields(self):
        integer_fields = ["year", "volume", "number"]
        invalids = ["abcd", "x.y", "xyz", "adfs123", "1.1.1", "2.3", "1,23", " "]
        for field in integer_fields:
            for bad_value in invalids:
                response = self.submit(**{field: bad_value})
                self.assertEqual(len(get_citations()), 0)
                self.assertIn(f"{field.capitalize()} must be a whole number".encode(), response.data)
    
    def test_invalid_month_field(self):
        invalid_months = ["13", "0", "-1", "abc", "1.5"]
        for bad_value in invalid_months:
            response = self.submit(month=bad_value)
            self.assertEqual(len(get_citations()), 0)
            self.assertIn(b"Month must be one of: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec", response.data)

    def test_book_input_allows_either_author_or_editor(self):
        for required_field in ("author", "editor"):
            self.submit(citation_type="book", **{required_field: ""})
            self.assertEqual(len(get_citations()), 1)
            reset_db()
        response = self.submit(citation_type="book", author="", editor="")
        self.assertEqual(len(get_citations()), 0)
        self.assertIn(b"Book requires either an author or an editor", response.data)

    def test_citation_name_cannot_contain_spaces(self):
        response = self.submit(name="name with spaces")
        self.assertEqual(len(get_citations()), 0)
        self.assertIn(b"Citation name cannot contain spaces", response.data)

    """ ----------------- INFO PAGE TESTS ----------------- """

    def test_get_citation_by_id_returns_citation(self):
        self.submit(name="test-id")
        citation_id = get_citations()[0].get_field("id")
        citation = get_citation_by_id(citation_id)
        self.assertIsNotNone(citation)
        self.assertEqual(citation.get_field("name"), "test-id")

    def test_get_citation_by_id_returns_none_for_invalid_id(self):
        citation = get_citation_by_id(99999)
        self.assertIsNone(citation)

    def test_info_page_shows_citation_data(self):
        
        fields_map = {
            "article": ["name", "author", "title", "journal"],
            "book": ["name", "author", "title", "publisher"],
            "inproceedings": ["name", "author", "title", "booktitle"],
            "mastersthesis": ["name", "author", "title", "school"],
            "phdthesis": ["name", "author", "title", "school"],
            "misc": ["name"],
        }
        for citation_type, fields in fields_map.items():
            overrides = {field: f"Test-{field.capitalize()}" for field in fields}
            overrides["citation_type"] = citation_type
            self.submit(**overrides)
            citation_id = get_citations()[0].get_field("id")
            response = self.client.get(f"/info/{citation_type}/{citation_id}")
            self.assertEqual(response.status_code, 200)
            for field in fields:
                self.assertIn(f"Test-{field.capitalize()}".encode(), response.data)
            reset_db()

    def test_info_page_redirects_for_invalid_id(self):
        response = self.client.get("/info/article/99999", follow_redirects=True)
        self.assertIn(b"Citation not found", response.data)

    """ ----------------- DELETE TESTS ----------------- """

    def test_delete_citation_removes_it_from_list(self):
        self.submit(name="to-be-deleted")
        citation_id = get_citations()[0].get_field("id")
        response = self.client.post(f"/remove/{citation_id}", follow_redirects=True)
        self.assertEqual(len(get_citations()), 0)
        self.assertNotIn(b"to-be-deleted", response.data)

    def test_delete_citation_removes_its_info_page(self):
        self.submit(name="to-be-deleted-info")
        citation_id = get_citations()[0].get_field("id")
        self.client.post(f"/remove/{citation_id}", follow_redirects=True)
        response = self.client.get(f"/info/article/{citation_id}", follow_redirects=True)
        self.assertIn(b"Citation not found", response.data)
    
    def test_delete_invalid_id_shows_error(self):
        response = self.client.post("/remove/99999", follow_redirects=True)
        self.assertIn(b"Citation not found", response.data)

    """ ----------------- EDIT TESTS ----------------- """

    def test_edit_page_shows_existing_data(self):
        self.submit(name="edit-test", author="Edit Author", title="Original Title")
        citation_id = get_citations()[0].get_field("id")

        response = self.client.get(f"/edit/article/{citation_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Original Title", response.data)

    def test_save_updates_citation(self):
        self.submit(name="save-test", author="Save Author", title="Old Title")
        citation_id = get_citations()[0].get_field("id")

        data = {
            "name": "save-test",
            "citation_type": "article",
            "author": "Save Author",
            "title": "New Title",
            "journal": "J",
            "year": "2000",
            "volume": "1",
            "number": "1",
            "pages": "1-2",
        }
        response = self.client.post(f"/save/{citation_id}", data=data, follow_redirects=True)

        citation = get_citation_by_id(citation_id)
        self.assertEqual(citation.get_field("title"), "New Title")
        self.assertIn(b"New Title", response.data)


if __name__ == "__main__":
    unittest.main()
