from core.scene import Scene
from core.frame import Frame
from core.track import Track
from core.Relation import Relation


class SceneGraphBuilder:
    """
    Dummy Scene Graph.

    Later:
        Metric Scene Graph GNN
    """

    def build(

        self,

        frame: Frame,

        tracks: list[Track]

    ) -> Scene:

        relations = []

        if len(tracks) >= 2:

            relations.append(

                Relation(

                    subject_id=tracks[0].track_id,

                    predicate="next_to",

                    object_id=tracks[1].track_id,

                    confidence=0.95,

                    distance=1.2

                )

            )

        return Scene(

            frame=frame,

            brightness=0.80,

            tracks=tracks,

            relations=relations

        )