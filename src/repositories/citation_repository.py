from config import db
from sqlalchemy import text

from entities.citation import Citation

def get_citations():
    result = db.session.execute(
        text("""SELECT id, name, citation_type, author, title, journal,
                year, volume, number, pages FROM citations""")
    )
    citations = result.fetchall()
    return [
        Citation(
            citation[0], citation[1], citation[2], citation[3],
            citation[4], citation[5], citation[6], citation[7],
            citation[8], citation[9]
        ) for citation in citations
    ]

def create_citation(
    name: str, citation_type: str, author: str, title: str,
    journal: str, year: int, volume: float, number: int, pages: str
):
    sql = text(
        """INSERT INTO citations (name, citation_type, author, title,
           journal, year, volume, number, pages)
           VALUES (:name, :citation_type, :author, :title, :journal,
           :year, :volume, :number, :pages)"""
    )
    db.session.execute(sql, {
        "name": name, "citation_type": citation_type, "author": author,
        "title": title, "journal": journal, "year": year, "volume": volume,
        "number": number, "pages": pages
    })
    db.session.commit()
