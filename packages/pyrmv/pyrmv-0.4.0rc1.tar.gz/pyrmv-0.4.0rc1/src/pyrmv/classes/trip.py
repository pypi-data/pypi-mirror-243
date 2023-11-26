from isodate import parse_duration

from pyrmv.classes.leg import Leg
from pyrmv.classes.stop import StopTrip


class Trip:
    """Trip object."""

    def __init__(self, data: dict):
        self.raw_data = data
        self.origin = StopTrip(data["Origin"])
        self.destination = StopTrip(data["Destination"])
        self.legs = []
        self.legs.extend(Leg(leg) for leg in data["LegList"]["Leg"])
        self.calculation = data["calculation"]
        self.index = data["idx"]
        self.id = data["tripId"]
        self.ctx_recon = data["ctxRecon"]
        self.duration = parse_duration(data["duration"])
        self.real_time_duration = (
            None if "rtDuration" not in data else parse_duration(data["rtDuration"])
        )
        self.checksum = data["checksum"]
        self.transfer_count = data.get("transferCount", 0)

    def __str__(self) -> str:
        return f"Trip from {self.origin.name} to {self.destination.name} lasting {self.duration} ({self.real_time_duration}) with {len(self.legs)} legs and {self.transfer_count} transfers"
