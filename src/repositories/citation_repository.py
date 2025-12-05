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

def save_citation(fields: dict, citation_id):
    """Save a citation by id."""
    if citation_id is None or fields["name"] is None:
        return
    original_citation = get_citation_by_id(citation_id)
    if fields["name"] != original_citation.get_field("name"):
        if citation_name_exists(fields["name"]):
            return

    sql_command = f"""
        UPDATE citations
        SET {", ".join(f"{f} = :{f}" for f in REF_FIELDS)}
        WHERE id = :id
    """
    params = {field: fields.get(field) or None for field in REF_FIELDS}
    params["id"] = citation_id

    db.session.execute(text(sql_command), params)
    db.session.commit()


def citation_name_exists(name: str) -> bool:
    """Return True if a citation with `name` exists."""
    sql = text("SELECT 1 FROM citations WHERE name = :name")
    result = db.session.execute(sql, {"name": name}).first()
    return result is not None


def get_citation_by_id(citation_id: int):
    """Return a single citation by id as a Citation object."""
    sql_command = "SELECT id, " + ", ".join(REF_FIELDS) + " FROM citations WHERE id = :id"
    result = db.session.execute(text(sql_command), {"id": citation_id})
    citation = result.fetchone()

    if citation is None:
        return None

    return Citation(citation)
