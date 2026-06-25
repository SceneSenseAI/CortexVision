from core.frame import Frame
from core.object import SceneObject


class Detector:
    """
    Dummy detector.
    Later replaced by YOLO-World.
    """

    def detect(self, frame: Frame) -> list[SceneObject]:

        return [

            SceneObject(
                label="person",
                confidence=0.98,
                bbox=(100, 50, 220, 420),
                centroid=(160, 235),
                depth=None,
            ),

            SceneObject(
                label="chair",
                confidence=0.94,
                bbox=(300, 210, 410, 420),
                centroid=(355, 315),
                depth=None,
            ),

        ]