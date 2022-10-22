import inspect
import os
from collections.abc import Callable
from typing import TypeVar

import requests
from flask import jsonify

from travel.backend.db import DBSession, Event, Level, Thread, User

T = TypeVar("T")


def ensure_login(fn: Callable[[User], T]) -> Callable[[str, str], T]:
    # ensure password and username parameters

    def wrapper(password, username):
        with DBSession() as session:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                return jsonify({"message": "User does not exist."})
            if user.password != password:
                return jsonify({"message": "Incorrect password."})
        return fn(user)

    return wrapper


@ensure_login
def profile(user):
    """
    Return: {
        "level": level (int),
        "events": event (list[Event]),
        "streak": streak (int)
        "percent_category": percent_category (dict[Category: float])
        "XP": xp (int) (number_of_city_visited * 10 + number_of_events * 5)
        "number_of_city_visited": number (int),
        "number_of_country_visited": number (int),
        "number_of_events": number (int),
        "number_of_threads": number (int),
    }
    """

    with DBSession() as session:
        events = session.query(Event).filter_by(user=user).all()
        threads = session.query(Thread).filter_by(user=user).all()
        number_of_city_visited = len(
            set(event.location.split(", ", 2)[0] for event in events)
        )
        number_of_country_visited = len(
            set(
                event.location.split(", ", 2)[-1] for event in events
            )  # location: "city, country"
        )
        number_of_events = len(events)
        number_of_threads = len(threads)
        xp = number_of_city_visited * 10 + number_of_events * 5
        streak = 0
        events = sorted(events, key=lambda event: event.date)
        for i in range(len(events) - 1):
            if events[i + 1].date - events[i].date == datetime.timedelta(days=1):
                streak += 1
            else:
                break

        percent_category = {}
        return jsonify(
            {
                "level": user.level.value,
                "events": [event.as_dict() for event in events],
                "streak": streak,
                "percent_category": percent_category,
                "XP": xp,
                "number_of_city_visited": number_of_city_visited,
                "number_of_country_visited": number_of_country_visited,
                "number_of_events": number_of_events,
                "number_of_threads": number_of_threads,
            }
        )


@ensure_login
def get_recommendation(user):
    pass


def get_common_places(city: str):
    """
    Calling google map API to get common places
    """

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": city,
        "key": os.environ["GOOGLE_MAPS_API_KEY"],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
