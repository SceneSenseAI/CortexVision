from dataclasses import dataclass, field

@dataclass
class Trajectory:
    """
    Stores the temporal motion history of a tracked object.
    """

    object_id: int

    positions: list[tuple[float, float]] = field(default_factory=list)

    speed: float = 0.0

    direction: float = 0.0

    predicted_path: list[tuple[float, float]] = field(default_factory=list)