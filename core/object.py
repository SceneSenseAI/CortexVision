from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np

@dataclass
class SceneObject:

    """
    Represents a real-world entity detected in a scene.
    """

    object_id: int

    label: str

    confidence: float

    bbox: tuple[int, int, int, int]        # (x1, y1, x2, y2)

    centroid: tuple[float, float]          # (cx, cy)

    mask: np.ndarray | None = None

    depth: float | None = None             # meters

    speed: float = 0.0                     # m/s

    direction: float = 0.0                 # degrees

    is_stationary: bool = True

    attributes: dict[str, Any] = field(default_factory=dict)

    def __repr__(self):

        return (

            f"{self.label}(id={self.object_id}, "

            f"depth={self.depth}, "

            f"speed={self.speed:.2f})"

        )