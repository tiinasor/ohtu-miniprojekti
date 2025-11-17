from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation, remove_citation
from config import app, test_env
from util import validate_todo

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

    try:
        validate_todo(name)

        year_int = int(year) if year else None
        volume_float = float(volume) if volume else None
        number_int = int(number) if number else None

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

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")


@app.route("/remove/<int:citation_id>", methods=["POST"])
def remove(citation_id):
    remove_citation(citation_id)
    return redirect("/")

if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
