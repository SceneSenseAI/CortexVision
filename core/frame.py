from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class Frame:
    """
    Represents one captured frame.
    """

    frame_id: int
    timestamp: float
    image: np.ndarray

    fps: float | None = None