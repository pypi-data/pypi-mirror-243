from typing import Any, Mapping

from isodate import parse_duration

from pyrmv.classes.gis import Gis
from pyrmv.classes.message import Message
from pyrmv.classes.stop import StopTrip


class Leg:
    """Trip leg object."""

    def __init__(self, data: Mapping[str, Any]):
        self.origin = StopTrip(data["Origin"])
        self.destination = StopTrip(data["Destination"])
        self.gis = (
            None if "GisRef" not in data else Gis(data["GisRef"]["ref"], data["GisRoute"])
        )
        self.messages = []
        self.index = data["idx"]
        self.name = data["name"]
        self.type = data["type"]
        self.direction = data.get("direction")
        self.number = data.get("number")
        self.duration = parse_duration(data["duration"])
        self.distance = data.get("dist")

        if "Messages" in data:
            self.messages.extend(Message(message) for message in data["Messages"]["Message"])
