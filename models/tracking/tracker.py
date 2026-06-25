from core.track import Track
from core.object import SceneObject
from core.trajectory import Trajectory


class Tracker:
    """
    Dummy tracker.

    Later:
        ByteTrack
    """

    def __init__(self):

        self.next_track_id = 1

    def update(
        self,
        detections: list[SceneObject]
    ) -> list[Track]:

        tracks = []

        for detection in detections:

            track = Track(

                track_id=self.next_track_id,

                scene_object=detection,

                trajectory=Trajectory(
                    object_id=self.next_track_id
                )

            )

            self.next_track_id += 1

            tracks.append(track)

        return tracks