from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.db import get_db
import requests
import re

BOT_URL = "http://127.0.0.1:5001"

bp = Blueprint("flag_report", __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute("SELECT id, title, body FROM posts").fetchall()
    return render_template("index.html", posts=posts)


# Bad sanitize function
def sanitize(input):
    pattern = r"<(?!\/?(h[1-6]|img)\b)[^>]+>"
    replaced_string = re.sub(pattern, "XSS_PROTECTION", input)
    return replaced_string


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title or not body:
            error = "Title and body is required."

        # sanitize input (not enough though, XSS still possible)
        title = sanitize(title)
        body = sanitize(body)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO posts (title, body) VALUES (?, ?)",
                (title, body),
            )
            db.commit()
            return redirect(url_for("index"))

    return render_template("create.html")


@bp.route("/report")
def report():
    id = request.args.get("id")
    # make the bot visit the page
    requests.get(f"{BOT_URL}/visit/{id}")
    return render_template("reported.html", id=id)


@bp.route("/post/<int:id>")
def render_single_post(id):
    post = get_post(id)
    return render_template(
        "post.html", id=post["id"], title=post["title"], body=post["body"]
    )


def get_post(id):
    post = (
        get_db()
        .execute(
            "SELECT id, title, body FROM posts WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post
