from typing import Any, Mapping

from pyrmv.classes.message import Message
from pyrmv.classes.stop import Stop
from pyrmv.utility import ref_upgrade


class Journey:
    """Journey object."""

    def __init__(self, data: Mapping[str, Any]):
        self.stops = []

        # Upgrade is temporarily used due to RMV API mismatch
        # self.ref = data["ref"]
        self.ref = ref_upgrade(data["ref"])

        self.direction = data["Directions"]["Direction"][0]["value"]
        self.direction_flag = data["Directions"]["Direction"][0]["flag"]
        self.stops.extend(Stop(stop) for stop in data["Stops"]["Stop"])
        self.messages = []

        if "Messages" in data:
            self.messages.extend(Message(message) for message in data["Messages"]["Message"])

    def __str__(self) -> str:
        return f"Journey with total of {len(self.stops)} stops and {len(self.messages)} messages heading {self.direction} ({self.direction_flag})"
