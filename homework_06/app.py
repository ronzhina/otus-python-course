from os import getenv

from flask import Flask, render_template
from flask_migrate import Migrate

from models.database import db
from views.posts import posts_app

app = Flask(__name__)

CONFIG_OBJECT_PATH = "config.{}".format(getenv("CONFIG_NAME", "DevelopmentConfig"))
app.config.from_object(CONFIG_OBJECT_PATH)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(posts_app, url_prefix="/posts")


@app.get("/")
def index():
    return render_template("base.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
