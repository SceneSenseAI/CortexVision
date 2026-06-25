from core.frame import Frame
from core.track import Track


class DepthEstimator:
    """
    Dummy depth estimator.

    Later:
        Depth Pro
    """

    def estimate(

        self,

        frame: Frame,

        tracks: list[Track]

    ) -> list[Track]:

        fake_depth = {

            "person": 2.3,

            "chair": 3.1,

            "table": 4.2

        }

        for track in tracks:

            label = track.scene_object.label

            track.scene_object.depth = fake_depth.get(label, 5.0)

        return tracks