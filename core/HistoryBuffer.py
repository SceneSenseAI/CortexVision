
from collections import deque
from dataclasses import field
from core.scene import Scene
from core.trajectory import Trajectory
from core.event import Event
from dataclasses import dataclass
from core.track import Track
@dataclass
class HistoryBuffer:

    scenes: deque[Scene] = field(default_factory=lambda: deque(maxlen=30))

    trajectories: dict[int, Track] = field(default_factory=dict)

    events: list[Event] = field(default_factory=list)

    def to_dict(self):

        return {

            "scenes":[

                scene.to_dict()

                for scene in self.scenes

            ],

            "events":[

                event.to_dict()

                for event in self.events

            ]

        }