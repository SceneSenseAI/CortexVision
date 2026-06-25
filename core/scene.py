from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from core.Relation import Relation
from core.object import SceneObject
from core.frame import Frame
from core.track import Track
@dataclass
class Scene:
    """
    Snapshot of the world at a given moment.
    """

    frame :Frame 
    brightness: float

    tracks: list[Track]

    relations: list[Relation] = field(default_factory=list)

    

    