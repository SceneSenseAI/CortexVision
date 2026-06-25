from dataclasses import dataclass, field

from core.object import SceneObject
from core.trajectory import Trajectory


@dataclass
class Track:
    """
    Represents a tracked object across multiple frames.
    """

    track_id: int

    scene_object: SceneObject

    age: int = 1

    hits: int = 1

    missed_frames: int = 0

    trajectory: Trajectory = field(
        default_factory=lambda: Trajectory(object_id=-1)
    )