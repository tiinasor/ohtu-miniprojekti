"""Utility helpers for validating citation input."""


class UserInputError(Exception):
    """Exception raised for invalid user input in forms."""


def _validate_required_field(ref_info, field_name, error_msg):
    """Helper to validate that a required field is not empty."""
    value = ref_info.get(field_name)
    if not value or str(value).strip() == "":
        raise UserInputError(error_msg)


def _validate_year(year_value):
    """Helper to validate year field."""
    if year_value is None or year_value == "":
        raise UserInputError("Year is required")
    try:
        year_int = int(year_value)
        if year_int >= 2100:
            raise UserInputError("Year must be smaller than 2100")
    except (ValueError, TypeError) as exc:
        raise UserInputError("Year must be a number") from exc


def _validate_field_lengths(ref_info):
    """Helper to validate all field lengths."""
    for field, value in ref_info.items():
        if value is not None and value != "" and len(str(value)) > 300:
            raise UserInputError(f"Field '{field}' must be less than 300 characters")


def validate_citation_info(ref_info):
    """Validate citation information in `ref_info` mapping."""
    if not ref_info:
        raise UserInputError("Missing citation data")

    citation_type = ref_info.get("citation_type")

    # Name is always required
    _validate_required_field(ref_info, "name", "Name is required")

    # Define validation rules per citation type
    common_required = ("article", "book", "inproceedings", "mastersthesis", "phdthesis")

    if citation_type in common_required:
        _validate_required_field(ref_info, "title", "Title is required")
        _validate_required_field(ref_info, "author", "Author is required")
        _validate_year(ref_info.get("year"))

    # Type-specific validations
    type_specific_fields = {
        "article": [("journal", "Journal is required")],
        "book": [("editor", "Editor is required"), ("publisher", "Publisher is required")],
        "inproceedings": [("booktitle", "Booktitle is required")],
        "mastersthesis": [("school", "School is required")],
        "phdthesis": [("school", "School is required")]
    }

    if citation_type in type_specific_fields:
        for field_name, error_msg in type_specific_fields[citation_type]:
            _validate_required_field(ref_info, field_name, error_msg)

    # Validate field lengths
    _validate_field_lengths(ref_info)
