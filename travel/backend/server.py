from flask import request, jsonify, Flask
from travel.backend.db import DBSession, User, Event, Thread, Level
import os


app = Flask(
    "travel",
    static_url_path="",
    static_folder=os.getcwd() + "/static",
)
app.config["DEBUG"] = True


@app.route("/unregister", methods=["POST", "GET"])
def unregister():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with DBSession() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                return jsonify({"message": "User does not exist."})
            if user.password != password:
                return jsonify({"message": "Incorrect password."})
            session.delete(user)
            session.commit()
        return jsonify({"message": "Unregister successful."})
    return jsonify({"message": "Unregister failed."})


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # hashed password
        with DBSession() as session:
            user = session.query(User).filter_by(username=username).first()

        if user is None:
            return jsonify({"message": "User does not exist."})
        if user.password == password:
            return jsonify({"message": "Login successful."})
        else:
            return jsonify({"message": "Incorrect password."})
    elif request.method == "GET":
        return app.send_static_file("signin_side.html")


# register
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session = DBSession()
        username = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", None)
        try:
            with session.begin():
                user = User(
                    username=username,
                    password=password,
                    email=email,
                    level=Level.BEGINNER,
                )
                session.add(user)
                session.commit()
            return jsonify({"message": "Register successful."})
        except Exception as e:
            return jsonify({"message": "Username already exists."})
    elif request.method == "GET":
        return app.send_static_file("signup.html")


# create thread
@app.route("/thread", methods=["POST", "GET"])
def thread():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        try:
            with DBSession() as session:
                thread = Thread(title=title, content=content)
                session.add(thread)
                session.commit()
            return jsonify({"message": "Thread created."})
        except Exception as e:
            return jsonify({"message": "Thread creation failed."})
    elif request.method == "GET":
        return app.send_static_file("thread.html")

# create profile
@app.route("/profile", methods=["GET"])
def profile():
    return app.send_static_file("html/profile.html")

# create event
@app.route("/event", methods=["POST", "GET"])
def event():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        ranking = request.form["ranking"]
        category = request.form["category"]
        try:
            with DBSession() as session:
                event = Event(
                    name=name,
                    description=description,
                    location=location,
                    date=date,
                    ranking=ranking,
                    category=category,
                )
                session.add(event)
                session.commit()
            return jsonify({"message": "Event created."})
        except Exception as e:
            return jsonify({"message": "Event creation failed."})
    elif request.method == "GET":
        return app.send_static_file("event.html")


# get all threads
@app.route("/threads", methods=["GET"])
def threads():
    if request.method == "GET":
        with DBSession() as session:
            threads = session.query(Thread).all()
            return jsonify([thread.to_dict() for thread in threads])


# get all events
@app.route("/events", methods=["GET"])
def events():
    if request.method == "GET":
        with DBSession() as session:
            events = session.query(Event).all()
            return jsonify(events)


# index
@app.route("/")
def redirect_to_index():
    return app.send_static_file("index.html")


@app.route("/index")
def index():
    return app.send_static_file("index.html")


@app.route("/index.html")
def index_html():
    return app.send_static_file("index.html")


@app.route("/static/<path:path>")
def send_static(path):
    return app.send_static_file(path)


@app.route("/css/<path:path>")
def send_css(path):
    return app.send_static_file("css/" + path)


@app.route("/js/<path:path>")
def send_js(path):
    return app.send_static_file("js/" + path)


@app.route("/img/<path:path>")
def send_img(path):
    return app.send_static_file("img/" + path)
