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

@app.route("/")
def index():
    """Show citations."""
    citations = get_citations()
    return render_template("index.html", citations=citations, ref_fields=REF_FIELDS)

@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    """Handle citation creation form."""
    citation_info = [None for field in REF_FIELDS]
    idx = 0
    for ref_field in REF_FIELDS:
        field = request.form.get(f'{ref_field}')
        if field:
            citation_info[idx] = field
        idx += 1
    citation_info[REF_FIELDS.index("citation_type")] = "article"
    for required_info in ["name", "year", "volume"]:
        if citation_info[REF_FIELDS.index(required_info)] is None:
            flash("Missing required fields")
            return redirect("/")
    if citation_name_exists(citation_info[REF_FIELDS.index("name")]):
        flash("Citation name must be unique")
        return redirect("/")
    try:
        int(citation_info[REF_FIELDS.index("year")])
        float(citation_info[REF_FIELDS.index("volume")])
        int(citation_info[REF_FIELDS.index("number")])
        create_citation(citation_info)
        return redirect("/")
    except Exception as error:
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
    else:
        return render_template("remove_citation.html", citation_id = citation_id)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        """Reset the database (test only)."""
        reset_db()
        return jsonify({ 'message': "db reset" })
