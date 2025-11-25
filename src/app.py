"""Flask app routes for citation management."""

from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    remove_citation,
    citation_name_exists,
)
from config import app, test_env #pylint: disable=W0611
from ref_fields import REF_FIELDS
from util import  UserInputError

def get_required_fields(citation_type, fields):
    """Return required fields for a given citation type.

    Returns:
        (required_fields, error_message)
        If error_message is not None, validation failed.
    """

    required_fields_map = {
        "article": ["name", "author", "title", "journal", "year"],
        "inproceedings": ["name", "author", "title", "booktitle", "year"],
        "mastersthesis": ["name", "author", "title", "school", "year"],
        "phdthesis": ["name", "author", "title", "school", "year"],
        "misc": ["name"],
    }

    # Book special case: requires *either* author or editor
    if citation_type == "book":
        if not fields.get("author") and not fields.get("editor"):
            return None, "Book requires either an author or an editor."
        return ["name", "title", "publisher", "year"], None

    required = required_fields_map.get(
        citation_type,
        ["name", "author", "title", "journal", "year"]
    )
    return required, None


@app.route("/")
def index():
    """Show all saved citations."""
    citations = get_citations()
    return render_template("index.html", citations=citations, ref_fields=REF_FIELDS)


@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    """Create a new citation entry."""
    fields = {field: request.form.get(field) for field in REF_FIELDS}

    citation_type = request.form.get("citation_type")
    fields["citation_type"] = citation_type

    # Validate required fields
    required, error = get_required_fields(citation_type, fields)

    if error:
        flash(error)
        return redirect("/")

    for field in required:
        if not fields.get(field):
            flash("Missing required fields")
            return redirect("/")

    if citation_name_exists(fields["name"]):
        flash("Citation name must be unique")
        return redirect("/")

    try:
        # convert numeric fields
        if fields.get("year"):
            fields["year"] = int(fields["year"])
        if fields.get("volume"):
            fields["volume"] = float(fields["volume"])
        if fields.get("number"):
            fields["number"] = int(fields["number"])

        create_citation(fields)
        return redirect("/")

    except UserInputError as error:
        flash(str(error))
        return redirect("/")
    except (ValueError, TypeError) as error:
        flash(str(error))
        return redirect("/")


# NEW simplified delete route
@app.route("/remove/<int:citation_id>", methods=["POST"])
def remove(citation_id):
    """Delete a citation immediately (confirmation handled by JS popup)."""
    remove_citation(citation_id)
    return redirect("/")

# pylint: disable=W0101
# Test-only: reset DB
# if test_env:
    @app.route("/reset_db")
    def reset_database():
        """Reset the database (test only)."""
        reset_db()
        return jsonify({"message": "db reset"})
# pylint: enable=W0101
