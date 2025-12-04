"""Flask app routes for citation management."""

import os
from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    remove_citation,
    citation_name_exists,
    get_citation_by_id,
    save_citation,
)
from config import app, test_env
from ref_fields import REF_FIELDS
from util import UserInputError


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


@app.route("/generate_bibtex", methods=["POST"])
def generate_bibtex():
    """Generate a BibTeX file from all citations and return it for download."""
    citations = get_citations()
    file_path = create_bibtex_file(citations)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="citations.bib",
        mimetype="text/plain"
    )


def create_bibtex_file(citations):
    """Create a BibTeX file inside the src directory."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "citations.bib")

    with open(file_path, "w", encoding="utf-8") as bibtex_file:
        for citation in citations:
            bibtex_content = f'@{citation.get_field("citation_type")}'
            bibtex_content += '{' + f'{citation.get_field("name")},\n'
            for field in REF_FIELDS:
                if citation.get_field(field):
                    bibtex_content += f'  {field} = {{{citation.get_field(field)}}},\n'
            bibtex_content += '}\n'
            bibtex_file.write(bibtex_content + "\n\n")

    return file_path


@app.route("/")
def index():
    """Show all saved citations."""
    citations = get_citations()
    return render_template("index.html", citations=citations, REF_FIELDS=REF_FIELDS)


MONTH_ABBREVIATIONS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def is_valid_month(value):
    """Return True if value is empty or a valid month abbreviation."""
    if not value:
        return True
    return value in MONTH_ABBREVIATIONS


@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    """Create a new citation entry."""
    fields = {field: request.form.get(field) for field in REF_FIELDS}
    citation_type = request.form.get("citation_type")
    fields["citation_type"] = citation_type

    # Validate required fields
    required, error = get_required_fields(citation_type, fields)

    # Collect all validation errors here
    validation_error = None

    if error:
        validation_error = error
    else:
        # Check missing required fields
        for field in required:
            if not fields.get(field):
                validation_error = "Missing required fields"
                break

        # Check valid month
        if not validation_error and not is_valid_month(fields.get("month")):
            validation_error = (
                "Month must be one of: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec"
            )

        # Check unique name
        if not validation_error and citation_name_exists(fields["name"]):
            validation_error = "Citation name must be unique"

    # If any validation failed
    if validation_error:
        flash(validation_error)
        return redirect("/")

    # Attempt conversion and creation
    try:
        if fields.get("year"):
            fields["year"] = int(fields["year"])
        if fields.get("volume"):
            fields["volume"] = int(fields["volume"])
        if fields.get("number"):
            fields["number"] = int(fields["number"])

        create_citation(fields)
        return redirect("/")

    except (UserInputError, ValueError, TypeError) as error:
        flash(str(error))
        return redirect("/")


@app.route("/remove/<int:citation_id>", methods=["POST"])
def remove(citation_id):
    """Delete a citation immediately (confirmation handled by JS popup)."""
    remove_citation(citation_id)
    return redirect("/")


@app.route("/save/<int:citation_id>", methods=["POST"])
def save(citation_id):
    """Save a citation."""
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

    if not is_valid_month(fields.get("month")):
        flash("Month must be one of: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec")
        return redirect("/")

    try:
        # convert numeric fields
        if fields.get("year"):
            fields["year"] = int(fields["year"])
        if fields.get("volume"):
            fields["volume"] = int(fields["volume"])
        if fields.get("number"):
            fields["number"] = int(fields["number"])

        save_citation(fields, citation_id)
        return redirect("/")

    except UserInputError as error:
        flash(str(error))
        return redirect("/")
    except (ValueError, TypeError) as error:
        flash(str(error))
        return redirect("/")

@app.route("/edit/<citation_type>/<int:citation_id>", methods=["GET"])
def edit(citation_type,citation_id):
    """Edit a citation (not implemented)."""
    citation = get_citation_by_id(citation_id)

    if citation is None:
        flash("Citation not found")
        return redirect("/")

    template_name = f"edits/{citation_type}_edit.html"
    return render_template(template_name, citation=citation)

@app.route("/info/<citation_type>/<int:citation_id>", methods=["GET"])
def info(citation_type, citation_id):
    """Show citation info according to type."""
    citation = get_citation_by_id(citation_id)

    if citation is None:
        flash("Citation not found")
        return redirect("/")

    template_name = f"infos/{citation_type}_info.html"
    return render_template(template_name, citation=citation)

# Test-only: reset DB
if test_env:
    @app.route("/reset_db")
    def reset_database():
        """Reset the database (test only)."""
        reset_db()
        return jsonify({"message": "db reset"})
