from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.citation_repository import get_citations, create_citation
from config import app, test_env
from util import validate_todo

@app.route("/")
def index():
    citations = get_citations()
    unfinished = len(citations)
    return render_template("index.html", todos=citations, unfinished=unfinished)

@app.route("/new_todo")
def new():
    return render_template("new_todo.html")

@app.route("/create_todo", methods=["POST"])
def todo_creation():
    name = request.form.get("content")

    try:
        validate_todo(name)
        create_citation(name, citation_type="article", author="Unknown", title="Untitled", journal="Unknown", year=2024, volume=1.0, number=1, pages="1-10")
        return redirect("/")
    except Exception as error:
        flash(str(error))
        return  redirect("/new_todo")

@app.route("/toggle_todo/<todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    set_done(todo_id)
    return redirect("/")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
