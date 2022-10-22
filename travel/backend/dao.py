import datetime
from collections.abc import Callable
from typing import TypeVar

from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from yarl import URL

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

        events = sorted(events, key=lambda event: event.date, reverse=True)
        for i in range(len(events) - 1):
            if events[i + 1].date - events[i].date <= datetime.timedelta(days=7):
                streak += 1

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

_map_base_url = URL("https://www.google.com/maps")

def _query_google_map(query):
    return _map_base_url.with_query({"q": query})

_chrome_options = Options()
_chrome_options.add_argument("--headless")
_driver = webdriver.Chrome(options=_chrome_options)


def _get_common_places(city: str):
    """
    Calling google map to get common places
    """

    import os
    os.environ["PATH"] = os.getcwd() + r"\bin"

    
    _driver.get(str(_query_google_map(city)))
    WebDriverWait(_driver, 10).until(EC.url_changes(_driver.current_url))
    return [
        dict(
            zip(
                "name rate reviews description".split(" "),
                e.get_attribute("aria-label").split(" · "),
            )
        )
        for e in _driver.find_element(
            By.CSS_SELECTOR,
            'div[aria-label*="Iconic"]',
        ).find_elements(By.CSS_SELECTOR, ".dryRY>div")
    ]

def get_common_places(city: str):
    """
    Return: {
        "places": places (list[dict])
    }
    """
    try:
        return jsonify({"places": _get_common_places(city)})
    except Exception as e:
        return jsonify({"places": []})