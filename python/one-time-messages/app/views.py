from flask.blueprints import Blueprint
from flask import request, render_template, make_response
from app.models import Message
from app import db
import datetime
import uuid

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/index")
def index():
    csrf_token = uuid.uuid4().hex
    response = make_response(render_template("index.html", csrf_token=csrf_token))
    response.set_cookie("X-CSRF-Token", csrf_token)
    return response


def _validate_csrf(req):
    cookie_token = req.cookies.get("X-CSRF-Token", None)
    form_csrf = req.form.get("csrf_token", None)
    if (cookie_token == form_csrf) and (cookie_token is not None):
        return True
    return False


@views.route("/create_message", methods=["POST"])
def create_message():
    if _validate_csrf(request):
        content = request.form.get("content", None)
        expiration_timestamp = request.form.get("due_timestamp", None)
        if content:
            message = Message(
                content=content,
            )
            if expiration_timestamp:
                message.due_timestamp = datetime.datetime.strptime(expiration_timestamp, '%Y-%m-%dT%H:%M')
            db.session.add(message)
            db.session.commit()
            response = make_response(render_template("create_message.html", message=message))
            response.delete_cookie("X-CSRF-Token")
            return response
    return "Form data is not valid", 400


@views.route("/message/<slug>")
def display_message(slug):
    message = Message.query.filter_by(slug=slug).first()
    if message:
        db.session.delete(message)
        db.session.commit()
        time_now, time_due = datetime.datetime.now(), message.expiration_timestamp
        if time_now > time_due != datetime.datetime.min:
            return "Message is due", 404
        return render_template("message.html", message=message)
    return "Message not found", 404

