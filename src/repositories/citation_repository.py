"""Repository helpers for reading and writing citations."""

from sqlalchemy import text

from config import db
from entities.citation import Citation
from ref_fields import REF_FIELDS


def get_citations():
    """Return all citations as Citation objects."""
    sql_command = "SELECT id, " + ", ".join(REF_FIELDS) + " FROM citations"
    result = db.session.execute(text(sql_command))
    citations = result.fetchall()

    return [Citation(citation) for citation in citations]


def create_citation(fields: dict):
    """Insert a citation record using a mapping of field->value."""
    sql_command = f"""
        INSERT INTO citations (
            {", ".join(REF_FIELDS)}
        ) VALUES (
            {", ".join(f":{f}" for f in REF_FIELDS)}
        )
    """

    # fill missing fields with None, convert empty strings to None
    params = {field: fields.get(field) or None for field in REF_FIELDS}

    db.session.execute(text(sql_command), params)
    db.session.commit()


def remove_citation(citation_id):
    """Delete a citation by id."""
    if citation_id is None:
        return

    sql = text("DELETE FROM citations WHERE id = :id")
    db.session.execute(sql, {"id": citation_id})
    db.session.commit()


def citation_name_exists(name: str) -> bool:
    """Return True if a citation with `name` exists."""
    sql = text("SELECT 1 FROM citations WHERE name = :name")
    result = db.session.execute(sql, {"name": name}).first()
    return result is not None
