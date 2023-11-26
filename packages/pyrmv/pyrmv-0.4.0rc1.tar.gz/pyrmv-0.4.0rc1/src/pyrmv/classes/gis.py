from typing import Any, Mapping

from isodate import parse_duration


class Gis:
    """Gis object."""

    def __init__(self, ref: str, route: Mapping[str, Any]):
        self.ref = ref
        self.dist = route["dist"]
        self.duration = parse_duration(route["durS"])
        self.geo = route["dirGeo"]
