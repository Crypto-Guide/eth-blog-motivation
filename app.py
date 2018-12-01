from flask import Flask, render_template, abort, request
from ethblogapp.models import User
from ethblogapp.database import db_session
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def hello():
    contents = User.query.all()

    return "hello"


@app.route("/<address>", methods=["GET"])
def show_content(address):
    content = User.query.filter_by(address=address).first()
    if content is None:
        abort(404)
    return "hello2"


@app.route("/<address>", methods=["POST"])
def post_content(address=None):
    if address is None:
        abort(404)
    content = User.query.filter_by(address=address).first()
    if content is None:
        content = User(address, request.form["url"])
    else:
        content.url = request.form["url"]
        content.date = datetime.now()
    db_session.add(content)
    db_session.commit()
    return content.url

if __name__ == "__main__":
    app.run()