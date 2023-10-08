from typing import Any, Dict, List, Text, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime as dt
import os
import requests
import json
from requests import ConnectionError, HTTPError, TooManyRedirects, Timeout
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("SENIVERSE_KEY", "")  # API key
API = "https://api.seniverse.com/v3/weather/daily.json"  # API URL
UNIT = "c" # Temperature unit
LANGUAGE = "zh-Hans" # language
one_day_timedelta = dt.timedelta(days=1)


def fetch_weather(location: str, start=0, days=15) -> dict:
    result = requests.get(
        API,
        params={
            "key": KEY,
            "location": location,
            "language": LANGUAGE,
            "unit": UNIT,
            "start": start,
            "days": days,
        },
        timeout=2,
    )
    return result.json()


def get_weather_by_date(location: str, date: dt.date) -> dict:
    day_timedelta = date - dt.datetime.today().date()
    day = day_timedelta // one_day_timedelta

    return get_weather_by_day(location, day)


def get_weather_by_day(location: str, day=1) -> dict:
    result = fetch_weather(location)

    normal_result = {
        "location": result["results"][0]["location"],
        "result": result["results"][0]["daily"][day],
    }

    return normal_result

def get_current_location() -> str:
    return "北京"


def get_text_weather_date(
    location: str, date_time: dt.date, raw_date_time: str
) -> dict:
    try:
        result = get_weather_by_date(location, date_time)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = {}
    else:
       
        text_message = {
            "location": result["location"]["name"],
            "datetime": raw_date_time,
            "calendartime": result["result"]["date"],
            "text_day": result["result"]["text_day"],
            "text_night": result["result"]["text_night"],
            "high": result["result"]["high"],
            "low": result["result"]["low"],
        }

    return text_message

# FIXME: conside using multi-language solution instead
def text_to_date(text_date: str) -> Optional[dt.date]:
    """convert text based date info into datatime object

    if the convert is not supprted will return None
    """
    if not text_date:
        date = dt.datetime.today().date()
    else:
        today = dt.datetime.now()
        one_more_day = dt.timedelta(days=1)

        if text_date == "今天":
            date = today.date()
        if text_date == "明天":
            date = (today + one_more_day).date()
        if text_date == "后天":
            date = (today + one_more_day * 2).date()

        # Not supported by weather API provider freely
        if text_date == "大后天":
            # return 3
            date = (today + one_more_day * 3).date()

        if text_date.startswith("星期"):
            # not supported yet
            date = None

        if text_date.startswith("下星期"):
            # not supported yet
            date = None

        # follow APIs are not supported by weather API provider freely
        if text_date == "昨天":
            date =  None
        if text_date == "前天":
            date =  None
        if text_date == "大前天":
            date =  None
    return date


class ActionQueryWeather(Action):
    def name(self) -> Text:
        return "action_query_weather"

    def run(
        self, dispatch: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict]:
        location = tracker.get_slot("location")
        datetime = tracker.get_slot("datetime")

        print(location, datetime)

        if not location:
            location = get_current_location()

        date_object = text_to_date(datetime)

        print(date_object)

        if not date_object:  # parse date_time failed
            dispatch.utter_message(template = "utter_no_weather_info", location = location, datetime = datetime)
        else:
            try:
                weather_data = get_text_weather_date(
                    location, date_object, datetime)
            except Exception as e:
                exec_msg = str(e)
                dispatch.utter_message(exec_msg)
            else:
                dispatch.utter_message(template = "utter_weather_info", **weather_data)

        return []
