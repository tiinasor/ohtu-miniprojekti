"""Utility helpers for validating citation input."""


class UserInputError(Exception):
    """Exception raised for invalid user input in forms."""


def validate_citation_info(ref_info):
    """Validate citation information in `ref_info` mapping."""
    if not ref_info:
        raise UserInputError("Missing citation data")

    name = ref_info.get("name")
    if not name or str(name).strip() == "":
        raise UserInputError("Name is required")

    if ref_info.get("citation_type") in ("article", "book", "inproceedings",
                                          "mastersthesis", "phdthesis"):
        title = ref_info.get("title")
        if not title or str(title).strip() == "":
            raise UserInputError("Title is required")

    if ref_info.get("citation_type") in ("article", "book", "inproceedings",
                                          "mastersthesis", "phdthesis"):
        author = ref_info.get("author")
        if not author or str(author).strip() == "":
            raise UserInputError("Author is required")

    if ref_info.get("citation_type") == "article":
        journal = ref_info.get("journal")
        if not journal or str(journal).strip() == "":
            raise UserInputError("Journal is required")

    year = ref_info.get("year")
    if ref_info.get("citation_type") in ("article", "book", "inproceedings",
                                          "mastersthesis", "phdthesis"):
        if year is not None and year != "":
            try:
                year_int = int(year)
                if year_int >= 2100:
                    raise UserInputError("Year must be smaller than 2100")
            except (ValueError, TypeError) as exc:
                raise UserInputError("Year must be a number") from exc
        else:
            raise UserInputError("Year is required")

    if ref_info.get("citation_type") == "book":
        editor = ref_info.get("editor")
        if not editor or str(editor).strip() == "":
            raise UserInputError("Editor is required")

    if ref_info.get("citation_type") == "book":
        publisher = ref_info.get("publisher")
        if not publisher or str(publisher).strip() == "":
            raise UserInputError("Publisher is required")

    if ref_info.get("citation_type") == "inproceedings":
        booktitle = ref_info.get("booktitle")
        if not booktitle or str(booktitle).strip() == "":
            raise UserInputError("Booktitle is required")

    if ref_info.get("citation_type") in ("mastersthesis", "phdthesis"):
        school = ref_info.get("school")
        if not school or str(school).strip() == "":
            raise UserInputError("School is required")

    for field, value in ref_info.items():
        if value is not None and value != "":
            if len(str(value)) > 300:
                raise UserInputError(f"Field '{field}' must be less than 300 characters")
