"""Representation of a citation and helper accessors."""

from ref_fields import REF_FIELDS


class Citation:  # pylint: disable=too-few-public-methods
    """Represents a citation row (id and its fields)."""

    def __init__(self, ref_info: list):
        """Initialize from a DB row where the first element is id."""
        self.id = ref_info[0]
        self.ref_info = ref_info[1:]

    def get_field(self, field_name: str):
        """Return the value for `field_name` or raise ValueError if unknown."""
        if field_name == 'id':
            return self.id
        if field_name in REF_FIELDS:
            return self.ref_info[REF_FIELDS.index(field_name)]
        raise ValueError(f"Field '{field_name}' is not a valid reference field.")
