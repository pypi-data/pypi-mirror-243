from datetime import datetime
from typing import Any, Mapping

from isodate import parse_duration

from pyrmv.classes.stop import Stop


class Url:
    """Traffic message channel url object."""

    def __init__(self, data: Mapping[str, Any]) -> None:
        self.name = data["name"]
        self.url = data["url"]

    def __str__(self) -> str:
        return f"{self.name}: {self.url}"


class Channel:
    """Traffic message channel object."""

    def __init__(self, data: Mapping[str, Any]) -> None:
        self.name = data["name"]
        url = []
        url.extend(Url(link) for link in url)
        self.url = url
        self.time_start = datetime.strptime(data["validFromTime"], "%H:%M:%S")
        self.date_start = datetime.strptime(data["validFromDate"], "%Y-%m-%d")
        self.time_end = datetime.strptime(data["validToTime"], "%H:%M:%S")
        self.date_end = datetime.strptime(data["validToDate"], "%Y-%m-%d")

    def __str__(self) -> str:
        return f"{self.name}: from {self.time_start} {self.date_start} until {self.time_end} {self.date_end}"


class Message:
    """Traffic message object."""

    def __init__(self, data: Mapping[str, Any]) -> None:
        self.affected_stops = []
        self.valid_from_stop = (
            None if "validFromStop" not in data else Stop(data["validFromStop"])
        )
        self.valid_to_stop = None if "validToStop" not in data else Stop(data["validToStop"])
        self.channels = []
        self.channels.extend(Channel(channel) for channel in data["channel"])
        self.id = data["id"]
        self.active = data["act"]
        self.head = data["head"]
        self.lead = data["lead"]
        self.text = data["text"]
        self.company = data["company"]
        self.category = data["category"]
        self.priority = None if "priority" not in data else data["priority"]
        self.products = data["products"]
        self.icon = data["icon"]
        self.time_start = datetime.strptime(data["sTime"], "%H:%M:%S")
        self.date_start = datetime.strptime(data["sDate"], "%Y-%m-%d")
        self.time_end = datetime.strptime(data["eTime"], "%H:%M:%S")
        self.date_end = datetime.strptime(data["eDate"], "%Y-%m-%d")
        self.date_start_alt = data["altStart"]
        self.date_end_alt = data["altEnd"]
        self.time_modified = datetime.strptime(data["modTime"], "%H:%M:%S")
        self.date_modified = datetime.strptime(data["modDate"], "%Y-%m-%d")
        self.daily_start = datetime.strptime(data["dailyStartingAt"], "%H:%M:%S")
        self.daily_duration = parse_duration(data["dailyDuration"])
        self.base_type = data["baseType"] if "baseType" in data else None

        if "affectedStops" in data:
            self.affected_stops.extend(
                Stop(stop) for stop in data["affectedStops"]["StopLocation"]
            )

    def __str__(self) -> str:
        return f"{self.base_type} message with priority {self.products} valid from {self.time_start.time()} {self.date_start.date()} until {self.time_end.time()} {self.date_end.date()}: {self.head} - {self.lead}"
