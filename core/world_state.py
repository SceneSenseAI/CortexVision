from dataclasses import dataclass, field
from datetime import datetime
from typing import List 

from core.scene import Scene
from core.event import Event

from core.HistoryBuffer import HistoryBuffer

@dataclass
class WorldState:

    current_scene: Scene

    history: HistoryBuffer

    created_at: datetime = field(default_factory=datetime.now)

