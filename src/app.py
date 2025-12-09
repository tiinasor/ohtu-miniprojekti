"""Flask app routes for citation management."""

import os
from flask import redirect, render_template, request, jsonify, flash, send_file
from db_helper import create_demo_citations, reset_db
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


def check_required_fields(citation_type, fields):
    """Return required fields for a given citation type.

    Returns:
        error_message: str or None
        If error_message is not None, validation failed.
    """

    required_fields_map = {
        "article": ["name", "author", "title", "journal", "year"],
        "book": ["name", "title", "publisher", "year"],  # special case handled separately
        "inproceedings": ["name", "author", "title", "booktitle", "year"],
        "mastersthesis": ["name", "author", "title", "school", "year"],
        "phdthesis": ["name", "author", "title", "school", "year"],
        "misc": ["name"],
    }

    # Book special case: requires *either* author or editor
    if citation_type == "book":
        if not fields.get("author") and not fields.get("editor"):
            return "Book requires either an author or an editor."

    required = required_fields_map.get(citation_type, [])

    for field in required:
        if not fields.get(field):
            return f"Missing required field: {field}"

    return None


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


@app.route("/generate_bibtex_selected", methods=["POST"])
def generate_bibtex_selected():
    """Generate a BibTeX file from selected citations and return it for download."""
    selected_ids = request.form.getlist("selected[]")

    citations = [get_citation_by_id(int(cid)) for cid in selected_ids]
    citations = [c for c in citations if c is not None]

    file_path = create_bibtex_file(citations)

    return send_file(
        file_path,
        as_attachment=True,
        download_name="selected_citations.bib",
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
            for field in REF_FIELDS[2:]:  # Skip 'citation_type' field
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

def validate_citation_fields(fields, citation_type):
    """Validate citation fields and return error message if any, otherwise None."""
    missing_required_fields = check_required_fields(citation_type, fields)

    if missing_required_fields:
        return missing_required_fields

    # Check name for spaces
    if fields.get("name") and " " in fields["name"]:
        return "Citation name cannot contain spaces"

    # Check valid month
    if not is_valid_month(fields.get("month")):
        return "Month must be one of: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec"

    # Check numeric fields
    for numeric_field in ["year", "volume", "number"]:
        if fields.get(numeric_field):
            try:
                int(fields[numeric_field])
            except ValueError:
                return f"{numeric_field.capitalize()} must be a whole number"

    return None

@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    """Create a new citation entry."""
    fields = {field: request.form.get(field) for field in REF_FIELDS}
    citation_type = request.form.get("citation_type")
    fields["citation_type"] = citation_type

    # Validate fields
    validation_error = validate_citation_fields(fields, citation_type)
    if validation_error:
        flash(validation_error)
        return redirect("/")

    # Check unique name
    if citation_name_exists(fields["name"]):
        flash("Citation name must be unique")
        return redirect("/")

    create_citation(fields)
    return redirect("/")


@app.route("/remove/<int:citation_id>", methods=["POST"])
def remove(citation_id):
    """Delete a citation immediately (confirmation handled by JS popup)."""
    citation = get_citation_by_id(citation_id)
    if citation is None:
        flash("Citation not found")
        return redirect("/")

    remove_citation(citation_id)
    return redirect("/")


@app.route("/save/<int:citation_id>", methods=["POST"])
def save(citation_id):
    """Save edited information of a citation."""
    fields = {field: request.form.get(field) for field in REF_FIELDS}
    citation_type = request.form.get("citation_type")
    fields["citation_type"] = citation_type

    # Validate fields
    validation_error = validate_citation_fields(fields, citation_type)
    if validation_error:
        flash(validation_error)
        return redirect("/")

    # Check unique name
    existing_citation = get_citation_by_id(citation_id)
    if existing_citation.get_field("name") != fields["name"]:
        if citation_name_exists(fields["name"]):
            flash("Citation name must be unique")
            return redirect("/")

    save_citation(fields, citation_id)
    return redirect("/")


@app.route("/edit/<citation_type>/<int:citation_id>", methods=["GET"])
def edit(citation_type,citation_id):
    """Open edit page according to citation type."""
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

    @app.route("/demo")
    def create_demo():
        """Reset the database and add demo citations (test only)."""
        reset_db()
        create_demo_citations()
        return redirect("/")
