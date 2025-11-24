"""Flask app routes for citation management."""

from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    remove_citation,
    citation_name_exists,
)
from config import app, test_env
from ref_fields import REF_FIELDS

def get_required_fields(citation_type, fields):
    """Get required fields based on citation type.
    
    Returns a tuple of (required_fields, error_message).
    If error_message is not None, validation failed.
    """
    required_fields_map = {
        "article": ["name", "author", "title", "journal", "year"],
        "inproceedings": ["name", "author", "title", "booktitle", "year"],
        "mastersthesis": ["name", "author", "title", "school", "year"],
        "phdthesis": ["name", "author", "title", "year", "school"],
        "misc": ["name"],
    }

    if citation_type == "book":
        if not fields.get("author") and not fields.get("editor"):
            return None, "Missing required fields: book requires either author or editor"
        return ["name", "title", "publisher", "year"], None

    # Get required fields from map or use default
    required = required_fields_map.get(
        citation_type,
        ["name", "author", "title", "journal", "year"]
    )
    return required, None

@app.route("/")
def index():
    """Show citations."""
    citations = get_citations()
    return render_template("index.html", citations=citations, ref_fields=REF_FIELDS)

@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    """Handle citation creation form submission."""

    fields = {field: request.form.get(field) for field in REF_FIELDS}
    citation_type = request.form.get("citation_type")
    fields["citation_type"] = citation_type

    # Get required fields based on citation type
    required, error = get_required_fields(citation_type, fields)

    if error:
        flash(error)
        return redirect("/")

    for r in required:
        if not fields.get(r):
            flash("Missing required fields")
            return redirect("/")

    if citation_name_exists(fields["name"]):
        flash("Citation name must be unique")
        return redirect("/")

    try:
        if fields.get("year"):
            fields["year"] = int(fields["year"])
        if fields.get("volume"):
            fields["volume"] = float(fields["volume"])
        if fields.get("number"):
            fields["number"] = int(fields["number"])

        create_citation(fields)
        return redirect("/")

    except (ValueError, TypeError) as error:
        flash(str(error))
        return redirect("/")


@app.route("/remove/<citation_id>", methods=["GET","POST"])
def remove(citation_id):
    """Remove a citation or show confirmation."""
    if request.method == "POST":
        if "remove" in request.form:
            remove_citation(citation_id)
            return redirect("/")
        if "back" in request.form:
            return redirect("/")
        return redirect("/")
    return render_template("remove_citation.html", citation_id = citation_id)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        """Reset the database (test only)."""
        reset_db()
        return jsonify({ 'message': "db reset" })
