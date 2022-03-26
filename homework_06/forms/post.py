from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import Length


class PostForm(FlaskForm):
    username = StringField("Your name", name="post-username", validators=[Length(min=1, max=100)])
    title = StringField("Title", name="post-title", validators=[Length(min=1, max=100)])
    body = TextAreaField("Body", name="post-body", validators=[Length(min=1, max=2000)])
