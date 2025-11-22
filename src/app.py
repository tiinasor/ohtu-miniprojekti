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

    fields = {field: request.form.get(field) for field in REF_FIELDS}

    required = ["name", "year", "volume"]
    for r in required:
        if not fields.get(r):
            flash("Missing required fields")
            return redirect("/")
        
    if citation_name_exists(fields["name"]):
        flash("Citation name must be unique")
        return redirect("/")

    fields["citation_type"] = request.form.get("citation_type")

    try:
        fields["year"] = int(fields["year"])
        fields["volume"] = float(fields["volume"])
        fields["number"] = int(fields["number"]) if fields.get("number") else None

        create_citation(fields)
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
        return redirect("/")
    return render_template("remove_citation.html", citation_id = citation_id)

if test_env:
    @app.route("/reset_db")
    def reset_database():
        """Reset the database (test only)."""
        reset_db()
        return jsonify({ 'message': "db reset" })
