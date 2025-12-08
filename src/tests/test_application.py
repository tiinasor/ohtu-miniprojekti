import os
import unittest

os.environ["TEST_ENV"] = "true"

from app import app
from db_helper import reset_db
from repositories.citation_repository import get_citations, get_citation_by_id
from ref_fields import REF_FIELDS


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

    def edit(self, citation_id, **overrides):
        citation = get_citation_by_id(citation_id)
        base = {}
        for field in REF_FIELDS:
            base[field] = citation.get_field(field)

        base.update(overrides)
        return self.client.post(f"/save/{citation_id}", data=base, follow_redirects=True)

    def test_edit_page_shows_existing_data(self):
        self.submit(title="Original Title")
        citation_id = get_citations()[0].get_field("id")

        response = self.client.get(f"/edit/article/{citation_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Original Title", response.data)

    def test_edit_page_for_invalid_id_shows_error(self):
        response = self.client.get("/edit/article/99999", follow_redirects=True)
        self.assertIn(b"Citation not found", response.data)

    def test_save_updates_citation_name(self):
        self.submit(name="Old-name")
        citation_id = get_citations()[0].get_field("id")
        response = self.edit(citation_id, name="New-name")
        citation = get_citation_by_id(citation_id)
        self.assertEqual(citation.get_field("name"), "New-name")
        self.assertIn(b"New-name", response.data)

    def test_save_updates_multiple_fields(self):
        self.submit(
            name="Initial-name",
            author="Initial Author",
            title="Initial Title",
            journal="Initial Journal",
            year=2023,
        )
        citation_id = get_citations()[0].get_field("id")
        response = self.edit(
            citation_id,
            name="Updated-name",
            author="Updated Author",
            title="Updated Title",
            journal="Updated Journal",
            year=2024,
        )
        citation = get_citation_by_id(citation_id)
        self.assertEqual(citation.get_field("name"), "Updated-name")
        self.assertEqual(citation.get_field("author"), "Updated Author")
        self.assertEqual(citation.get_field("title"), "Updated Title")
        self.assertEqual(citation.get_field("journal"), "Updated Journal")
        self.assertEqual(citation.get_field("year"), 2024)
        self.assertIn(b"Updated-name", response.data)


    def test_invalid_inputs_on_save_shows_error(self):
        self.submit()
        citation_id = get_citations()[0].get_field("id")
        for field in ["year", "volume", "number"]:
            response = self.edit(citation_id, **{field: "invalid-number"})
            self.assertIn(f"{field.capitalize()} must be a whole number".encode(), response.data)
        for required_field in ["name", "author", "title", "journal", "year"]:
            response = self.edit(citation_id, **{required_field: ""})
            self.assertIn(f"Missing required field: {required_field}".encode(), response.data)

    def test_save_duplicate_name_shows_error(self):
        self.submit(name="original-name")
        self.submit(name="duplicate-name")
        citation_id = get_citations()[1].get_field("id")
        response = self.edit(citation_id, name="original-name")
        self.assertIn(b"Citation name must be unique", response.data)

    """ ----------------- BIBTEX FILE GENERATION TESTS ----------------- """

    def test_generate_bibtex_file(self):
        self.submit(name="bibtex-endpoint-test", author="Endpoint Author")
        response = self.client.post("/generate_bibtex")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Disposition"],
            'attachment; filename=citations.bib'
        )
        self.assertIn(b"@article{bibtex-endpoint-test", response.data)
        self.assertIn(b"author = {Endpoint Author}", response.data)
        bib_path = os.path.join(os.path.dirname(__file__), "..", "citations.bib")
        if os.path.exists(bib_path):
            os.remove(bib_path)

    def test_generate_bibtex_selected_citations_file(self):
        self.submit(name="citation-1", author="Author One", title="Title One")
        self.submit(name="citation-2", author="Author Two", title="Title Two")
        self.submit(name="citation-3", author="Author Three", title="Title Three")
        
        citations = get_citations()
        selected_ids = [str(citations[0].id), str(citations[2].id)]
        
        response = self.client.post("/generate_bibtex_selected", 
                                   data={"selected[]": selected_ids})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["Content-Disposition"],
            'attachment; filename=selected_citations.bib'
        )
        self.assertIn(b"@article{citation-1", response.data)
        self.assertIn(b"author = {Author One}", response.data)
        self.assertIn(b"@article{citation-3", response.data)
        self.assertIn(b"author = {Author Three}", response.data)
        self.assertNotIn(b"citation-2", response.data)
        
        bib_path = os.path.join(os.path.dirname(__file__), "..", "selected_citations.bib")
        if os.path.exists(bib_path):
            os.remove(bib_path)

if __name__ == "__main__":
    unittest.main()

