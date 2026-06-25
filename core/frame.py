from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np


@dataclass
class Frame:
    """
    Represents one captured frame.
    """

    frame_id: int
    timestamp: float
    image: np.ndarray=field(repr=False)

    fps: float | None = None
    def __repr__(self) -> str:
        return (
            f"Frame(id={self.frame_id}, "
            f"fps={self.fps:.1f}, "
            f"time={self.timestamp:.3f})"
        )
    def to_dict(self):

        return {

            "frame_id": self.frame_id,

            "timestamp": self.timestamp,

            "fps": self.fps

        }