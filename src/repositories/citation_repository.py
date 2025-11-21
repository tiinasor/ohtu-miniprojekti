"""Repository helpers for reading and writing citations."""

from sqlalchemy import text

from config import db
from entities.citation import Citation
from ref_fields import REF_FIELDS

def get_citations():
    """Return all citations as Citation entities."""
    sql_command = "SELECT id, "
    for field in REF_FIELDS:
        sql_command += field + ", "
    sql_command = sql_command.rstrip(", ")  # Remove trailing comma and space
    sql_command += " FROM citations"
    result = db.session.execute(text(sql_command))
    citations = result.fetchall()
    return [
        Citation(citation) for citation in citations
    ]

def create_citation(ref_info: list):
    """Insert a citation using `ref_info` ordered by `REF_FIELDS`."""

    sql_command = "INSERT INTO citations ("
    sql_command += ", ".join(REF_FIELDS)
    sql_command += ") VALUES ("
    for field in REF_FIELDS:
        sql_command += f":{field}, "
    sql_command = sql_command.rstrip(", ")  # Remove trailing comma and space
    sql_command += ")"

    db.session.execute(text(sql_command), {
        field: ref_info[index] for index, field in enumerate(REF_FIELDS)
    })
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
