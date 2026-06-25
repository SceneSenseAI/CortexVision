from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from Relation import Relation
from core.object import SceneObject
from frame import Frame

@dataclass
class Scene:
    """
    Snapshot of the world at a given moment.
    """

    frame :Frame 
    brightness: float

    objects: List[SceneObject] = field(default_factory=list)

    relations: list[Relation] = field(default_factory=list)

    

    