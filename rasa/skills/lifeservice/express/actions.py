# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Tracker
from rasa_sdk import Action
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, SlotSet
import time
import json
import requests

express_list = {
    "圆通": "yuantong",
    "顺丰": "shunfeng",
    "中通": "zhongtong"
}


def get_url(code, id):
    time_new = str(int(time.time() * 1000))
    url = "http://www.kuaidi.com/index-ajaxselectcourierinfo-" + \
        id + "-" + code + "-UUCAO" + time_new + ".html"
    return url


class ActionSubmitSearchExpressForm(Action):

    def name(self) -> Text:
        return "action_submit_search_express_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[EventType]:
        express = tracker.get_slot("express")
        number = tracker.get_slot("number")
        
        print(express, number)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            "Referer": "http://www.kuaidi.com/cominterface2345.html"
        }
        url = get_url(express_list[express], number)
        response = requests.get(url, headers=headers)
        datas = json.loads(response.text)['data']
        text = ""
        for item in datas:
            time_ = item['time']
            info = item['context']
            text += f'时间：{time_}'
            text += f'物流状态：{info}' + '\n'

        dispatcher.utter_message(text=text)
        return []