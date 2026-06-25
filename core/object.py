from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
import numpy as np

@dataclass
class SceneObject:

    """
    Represents a real-world entity detected in a scene.
    """

    label: str

    confidence: float

    bbox: tuple[int, int, int, int]        # (x1, y1, x2, y2)

    centroid: tuple[float, float]          # (cx, cy)

    mask: np.ndarray | None = None

    depth: float | None = None             # meters

    attributes: dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (
            f"{self.label}"
            f"(conf={self.confidence:.2f}, "
            f"depth={self.depth:.2f}m)"
            if self.depth is not None
            else
            f"{self.label}"
            f"(conf={self.confidence:.2f})"
        )
    def to_dict(self):

        return {

            "label": self.label,

            "confidence": self.confidence,

            "bbox": self.bbox,

            "centroid": self.centroid,

            "depth": self.depth,

            "attributes": self.attributes

    }