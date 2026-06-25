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

    def to_dict(self):

        return {

            "frame": self.frame.to_dict(),

            "brightness": self.brightness,

            "tracks": [

                track.to_dict()

                for track in self.tracks

            ],

            "relations": [

                relation.to_dict()

                for relation in self.relations

            ]

        }
    def __repr__(self) -> str:

        lines = []

        lines.append("=" * 50)
        lines.append(f"FRAME #{self.frame.frame_id}")
        lines.append("=" * 50)

        lines.append("\nObjects")
        lines.append("-" * 20)

        for track in self.tracks:
            lines.append(str(track))

        lines.append("\nRelations")
        lines.append("-" * 20)

        if not self.relations:
            lines.append("None")

        else:

            id_to_label = {
                track.track_id: track.scene_object.label
                for track in self.tracks
            }

            for relation in self.relations:

                subject = id_to_label.get(relation.subject_id, relation.subject_id)

                obj = id_to_label.get(relation.object_id, relation.object_id)

                lines.append(
                    f"{subject} ---- {relation.predicate} ----> {obj}"
                )

        return "\n".join(lines)