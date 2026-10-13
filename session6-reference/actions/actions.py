"""
Session 6 reference actions: ActionTellJoke and ActionSearchTrains.

These are the exact, tested versions from Session 6. If your own version
isn't behaving, diff your file against this one line by line rather than
retyping from the slides, a pasted snippet is the single most common
source of bugs in this session (see the README in this folder).
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import requests
import sqlite3


class ActionTellJoke(Action):
    def name(self) -> Text:
        return "action_tell_joke"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        try:
            resp = requests.get(
                "https://official-joke-api.appspot.com/random_joke", timeout=3
            )
            resp.raise_for_status()
            joke = resp.json()
            text = f"{joke['setup']} ... {joke['punchline']}"
        except requests.RequestException:
            text = "Couldn't reach the joke API, but here's one anyway."
        dispatcher.utter_message(text=text)
        return []


class ActionSearchTrains(Action):
    def name(self) -> Text:
        return "action_search_trains"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[Dict[Text, Any]]:
        origin = tracker.get_slot("origin")
        destination = tracker.get_slot("destination")
        try:
            conn = sqlite3.connect("trains.db")
            row = conn.execute(
                "SELECT direct FROM routes WHERE LOWER(origin)=LOWER(?) "
                "AND LOWER(destination)=LOWER(?)",
                (origin, destination),
            ).fetchone()
            conn.close()
        except sqlite3.Error:
            return [SlotSet("train_search_result", "error")]
        if row is None:
            return [SlotSet("train_search_result", "not_found")]
        return [SlotSet("train_search_result", "direct" if row[0] else "indirect")]
