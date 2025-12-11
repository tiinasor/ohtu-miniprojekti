"""Database helper utilities for creating and resetting the schema."""

import os

from sqlalchemy import text

from config import db, app
from repositories.citation_repository import create_citation


def reset_db():
    """Delete all rows from the `citations` table."""
    print("Clearing contents from table citations")
    sql = text("DELETE FROM citations")
    db.session.execute(sql)
    db.session.commit()


def tables():
    """Returns all table names from the database except those ending with _id_seq"""
    sql = text(
        "SELECT table_name "
        "FROM information_schema.tables "
        "WHERE table_schema = 'public' "
        "AND table_name NOT LIKE '%_id_seq'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def create_demo_citations():
    """Creates sample citations for demonstration purposes."""
    article = {
        "name": "voyager",
        "citation_type": "article",
        "author": "Paukku, Timo",
        "title": (
            "Voyager-luotain lähti matkaan 1970-luvulla - on pian yhden valopäivän päässä Maasta"
        ),
        "journal": "Helsingin Sanomat",
        "year": "2025",
        "volume": "1",
        "month": "Dec",
        "note": "Accessed: 8.12.2025",
    }
    book = {
        "name": "algorithms2022",
        "citation_type": "book",
        "author": "Cormen, Thomas H.; Leiserson, Charles E.; Rivest, Ronald L.; Stein, Clifford",
        "title": "Introduction to Algorithms (2022)",
        "publisher": "MIT Press; McGraw-Hill",
        "year": "1990",
        "edition": "4th",
        "note": "Accessed: 8.12.2025",
    }
    inproceedings = {
        "name": "productlines",
        "citation_type": "inproceedings",
        "author": "Simon, Daniel; Eisenbarth, Thomas",
        "title": "Evolutionary Introduction of Software Product Lines",
        "booktitle": (
            "Proceedings of the Second International Software Product Line Conference, "
            "SPLC 2, San Diego, CA, USA, August 2002"
        ),
        "series": "Lecture Notes in Computer Science",
        "volume": "2379",
        "pages": "272-283",
        "publisher": "Springer",
        "year": "2002",
        "note": "Accessed: 8.12.2025",
    }
    masters = {
        "name": "linux",
        "citation_type": "mastersthesis",
        "author": "Torvalds, Linus",
        "title": "Linux: a Portable Operating System",
        "school": "University of Helsinki",
        "type": "M. Sc. thesis",
        "year": "1997",
        "month": "Jan",
        "address": "Helsinki, Finland",
        "note": "Accessed: 9.12.2025",
    }
    phd = {
        "name": "quantumML",
        "citation_type": "phdthesis",
        "author": "Salmenperä, Ilmo",
        "title": "Investigating Implementation Issues in Quantum Machine Learning",
        "school": "University of Helsinki",
        "year": "2025",
        "month": "Dec",
        "address": "Helsinki, Finland",
        "note": "Accessed: 9.12.2025",
    }
    misc = {
        "name": "enisa",
        "citation_type": "misc",
        "author": "European Union Agency for Cybersecurity (ENISA)",
        "title": "ENISA Threat Landscape 2025",
        "year": "2025",
        "month": "Oct",
        "howpublished": "https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025",
        "note": "Accessed: 8.12.2025",
    }

    create_citation(article)
    create_citation(book)
    create_citation(inproceedings)
    create_citation(masters)
    create_citation(phd)
    create_citation(misc)


def setup_db():
    """
    Creating the database
    If database tables already exist, those are dropped before the creation
    """
    tables_in_db = tables()
    if len(tables_in_db) > 0:
        print("Tables exist, dropping: {', '.join(tables_in_db)}")
        for table in tables_in_db:
            sql = text(f"DROP TABLE {table}")
            db.session.execute(sql)
        db.session.commit()

    print("Creating database")

    # Read schema from schema.sql file
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read().strip()

    sql = text(schema_sql)
    db.session.execute(sql)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        setup_db()
