from dataclasses import dataclass, field

@dataclass
class Trajectory:
    """
    Stores the temporal motion history of a tracked object.
    """

    object_id: int

    history: list[tuple[float, float]] = field(default_factory=list)    ##(x,y,t)

    speed: float = 0.0

    direction: float = 0.0

    predicted_path: list[tuple[float, float]] = field(default_factory=list)

    def to_dict(self):

        return {

            "object_id": self.object_id,

            "history": self.history,

            "speed": self.speed,

            "direction": self.direction,

            "predicted_path": self.predicted_path

        }