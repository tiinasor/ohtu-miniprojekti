from sqlalchemy import text

from config import db
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


def remove_citation(citation_id):
    
    if citation_id is None:
        return
    
    sql = text(f"DELETE FROM citations WHERE id = :id")
    db.session.execute(sql, {"id": citation_id})
    db.session.commit()
    
    
def citation_name_exists(name: str) -> bool:
    sql = text("SELECT 1 FROM citations WHERE name = :name")
    result = db.session.execute(sql, {"name": name}).first()
    return result is not None