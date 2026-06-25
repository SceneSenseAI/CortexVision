
from collections import deque
from dataclasses import field
from scene import Scene
from trajectory import Trajectory
from event import Event
from dataclasses import dataclass

@dataclass
class HistoryBuffer:

    scenes: deque[Scene] = field(default_factory=lambda: deque(maxlen=30))

    trajectories: dict[int, Trajectory] = field(default_factory=dict)

    events: list[Event] = field(default_factory=list)