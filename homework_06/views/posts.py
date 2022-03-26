from http import HTTPStatus

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import NotFound, InternalServerError

from forms import PostForm
from models import Post
from models.database import db

posts_app = Blueprint("posts_app", __name__)


@posts_app.get("/", endpoint="posts_list")
def list_posts():
    posts: list[Post] = Post.query.all()
    return render_template("posts/list.html", posts=posts)


@posts_app.get("/<int:post_id>/", endpoint="post_details")
def get_post(post_id: int):
    post = Post.query.get(post_id)
    if post is None:
        raise NotFound(f"Post #{post_id} not found!")

    return render_template(
        "posts/details.html",
        post=post,
    )


@posts_app.route("/add/", methods=["GET", "POST"], endpoint="post_add")
def add_post():
    form = PostForm()
    if request.method == "GET":
        return render_template("posts/add.html", form=form)

    if not form.validate_on_submit():
        return render_template("posts/add.html", form=form), HTTPStatus.BAD_REQUEST

    post_username = form.data["username"]
    post_title = form.data["title"]
    post_body = form.data["body"]
    post = Post(username=post_username, title=post_title, body=post_body)
    db.session.add(post)

    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save post, unexpected error")

    post_url = url_for("posts_app.post_details", post_id=post.id)
    return redirect(post_url)
