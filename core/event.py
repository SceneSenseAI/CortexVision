#  DATAFLOW implemented 

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any


@dataclass
class Event:

    timestamp: datetime

    source_id: int

    involved_objects: list[int]

    description: str

    target_id: int | None = None

    event_type: str = "unknown"

    distance_change: float = 0.0

    depth_change: float = 0.0

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {

            "timestamp": str(self.timestamp),

            "event_type": self.event_type,

            "source_id": self.source_id,

            "target_id": self.target_id,

            "description": self.description,

            "distance_change": self.distance_change,

            "depth_change": self.depth_change

        }

        

        