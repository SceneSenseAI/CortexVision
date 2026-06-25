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
    def to_dict(self):

        return {

            "track_id": self.track_id,

            "age": self.age,

            "hits": self.hits,

            "missed_frames": self.missed_frames,

            "scene_object": self.scene_object.to_dict(),

            "trajectory": self.trajectory.to_dict()

        }
    def __repr__(self) -> str:
        return (
            f"Track {self.track_id} | "
            f"{self.scene_object.label} | "
            f"Depth={self.scene_object.depth:.2f}m | "
            f"Age={self.age} | "
            f"Hits={self.hits}"
        )