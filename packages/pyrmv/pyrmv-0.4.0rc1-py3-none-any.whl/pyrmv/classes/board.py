from datetime import datetime
from typing import Any, Mapping

from pyrmv.classes.message import Message
from pyrmv.utility import ref_upgrade


class LineArrival:
    def __init__(self, data: Mapping[str, Any], client, retrieve_stops: bool = True):
        # Upgrade is temporarily used due to RMV API mismatch
        # self.journey = client.journey_detail(data["JourneyDetailRef"]["ref"])
        self.journey = client.journey_detail(ref_upgrade(data["JourneyDetailRef"]["ref"]))

        self.status = data["JourneyStatus"]
        self.messages = []
        self.name = data["name"]
        self.type = data["type"]
        self.stop_name = data["stop"]
        self.stop_id = data["stopid"]
        self.stop_id_ext = data["stopExtId"]
        self.stop = client.stop_by_id(self.stop_id) if retrieve_stops else None
        self.stop = client.stop_by_id(self.stop_id)
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.reachable = data["reachable"]
        self.origin = data["origin"]
        self.origin = data["origin"]

        if "Messages" in data:
            self.messages.extend(Message(message) for message in data["Messages"]["Message"])

        if ("rtTime" in data) and ("rtDate" in data):
            self.time_real_time = datetime.strptime(data["rtTime"], "%H:%M:%S")
            self.date_real_time = datetime.strptime(data["rtDate"], "%Y-%m-%d")
        else:
            self.time_real_time = None
            self.date_real_time = None

    def __str__(self) -> str:
        return (
            f"{self.name} coming from {self.origin} at {self.time.time()} {self.date.date()}"
        )


class LineDeparture:
    def __init__(self, data: Mapping[str, Any], client, retrieve_stops: bool = True):
        # Upgrade is temporarily used due to RMV API mismatch
        # self.journey = client.journey_detail(data["JourneyDetailRef"]["ref"])
        self.journey = client.journey_detail(ref_upgrade(data["JourneyDetailRef"]["ref"]))

        self.status = data["JourneyStatus"]
        self.messages = []
        self.name = data["name"]
        self.type = data["type"]
        self.stop_name = data["stop"]
        self.stop_id = data["stopid"]
        self.stop_id_ext = data["stopExtId"]
        self.stop = client.stop_by_id(self.stop_id) if retrieve_stops else None
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.reachable = data["reachable"]
        self.direction = data["direction"]
        self.direction_flag = data["directionFlag"]

        if "Messages" in data:
            self.messages.extend(Message(message) for message in data["Messages"]["Message"])

        if ("rtTime" in data) and ("rtDate" in data):
            self.time_real_time = datetime.strptime(data["rtTime"], "%H:%M:%S")
            self.date_real_time = datetime.strptime(data["rtDate"], "%Y-%m-%d")
        else:
            self.time_real_time = None
            self.date_real_time = None

    def __str__(self) -> str:
        return (
            f"{self.name} heading {self.direction} at {self.time.time()} {self.date.date()}"
        )


class BoardArrival(list):
    def __init__(self, data: Mapping[str, Any], client, retrieve_stops: bool = True):
        super().__init__([])

        if "Arrival" not in data:
            return

        for line in data["Arrival"]:
            self.append(LineArrival(line, client, retrieve_stops=retrieve_stops))

    def __str__(self) -> str:
        return "Arrival board\n" + "\n".join([str(line) for line in self])


class BoardDeparture(list):
    def __init__(self, data: Mapping[str, Any], client, retrieve_stops: bool = True):
        super().__init__([])

        if "Departure" not in data:
            return

        for line in data["Departure"]:
            self.append(LineDeparture(line, client, retrieve_stops=retrieve_stops))

    def __str__(self) -> str:
        return "Departure board\n" + "\n".join([str(line) for line in self])
