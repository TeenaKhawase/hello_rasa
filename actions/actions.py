"""Optional custom action for Session 1 — not wired up by default.

To use it: uncomment the `action_endpoint` block in endpoints.yml, add an
`action_hello_world_custom` step to data/rules.yml in place of
`utter_hello_world`, then run `rasa run actions` in a second terminal
alongside `rasa shell`.
"""

from typing import Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorldCustom(Action):
    def name(self) -> str:
        return "action_hello_world_custom"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: dict[str, Any],
    ) -> list[dict[str, Any]]:
        dispatcher.utter_message(
            text="Hello, World! This reply came from Python code in actions/actions.py."
        )
        return []
