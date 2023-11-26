from datetime import datetime


class Stop:
    """Stop object."""

    def __init__(self, data: dict):
        self.name = data["name"]
        self.id = data["id"]
        self.ext_id = data.get("extId")
        self.description = data.get("description")
        self.lon = data["lon"]
        self.lat = data["lat"]
        self.route_index = data.get("routeIdx")
        self.track_arrival = data.get("arrTrack")
        self.track_departure = data.get("depTrack")

    def __str__(self) -> str:
        return f"Stop {self.name} at {self.lon}, {self.lat}"


class StopTrip(Stop):
    """Trip stop object. It's like a Stop object, but with a date and time."""

    def __init__(self, data: dict):
        self.type = data["type"]
        self.date = datetime.strptime(data["date"], "%Y-%m-%d")
        self.time = datetime.strptime(data["time"], "%H:%M:%S")
        super().__init__(data)

    def __str__(self) -> str:
        return f"Stop {self.name} at {self.lon}, {self.lat} at {self.time.time()} {self.date.date()}"
