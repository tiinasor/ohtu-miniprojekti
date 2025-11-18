from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import (
    get_citations,
    create_citation,
    remove_citation,
    citation_name_exists,
)
from config import app, test_env

@app.route("/")
def index():
    citations = get_citations()
    return render_template("index.html", citations=citations)

@app.route("/create_citation", methods=["POST"])
def create_citation_route():
    name = request.form.get("name")
    author = request.form.get("author")
    title = request.form.get("title")
    journal = request.form.get("journal")
    year = request.form.get("year")
    volume = request.form.get("volume")
    number = request.form.get("number")
    pages = request.form.get("pages")

    if not name or not year or not volume or not number or not pages:
        flash("Missing required fields")
        return redirect("/")

    if citation_name_exists(name):
        flash("Citation name must be unique")
        return redirect("/")

    try:
        year_int = int(year)
        volume_float = float(volume)
        number_int = int(number)

        create_citation(
            name=name,
            citation_type="article",
            author=author,
            title=title,
            journal=journal,
            year=year_int,
            volume=volume_float,
            number=number_int,
            pages=pages,
        )
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return redirect("/")

@app.route("/toggle_citation/<citation_id>", methods=["POST"])
def toggle_citation(citation_id):
    set_done(citation_id)
    return redirect("/")


@app.route("/remove/<int:citation_id>", methods=["GET","POST"])
def remove(citation_id):
    
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
        reset_db()
        return jsonify({ 'message': "db reset" })
