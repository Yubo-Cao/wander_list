import inspect
import os

from flask import jsonify

from travel.backend.db import DBSession, Event, Level, Thread, User


def ensure_login(fn):
    # ensure password and username parameters
    sign = inspect.signature(fn)
    if "password" not in sign.parameters:
        raise Exception("password parameter is required")
    if "username" not in sign.parameters:
        raise Exception("username parameter is required")

    def wrapper(*args, **kwargs):
        ba = sign.bind(*args, **kwargs)
        username = ba.arguments["username"]
        password = ba.arguments["password"]

        with DBSession() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                return jsonify({"message": "User does not exist."})
            if user.password != password:
                return jsonify({"message": "Incorrect password."})
        return fn(*args, **kwargs)

    return wrapper
