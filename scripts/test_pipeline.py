from time import time

import numpy as np

from app.pipeline import CortexVisionPipeline
from core.frame import Frame


pipeline = CortexVisionPipeline()

frame = Frame(
    frame_id=1,
    timestamp=time(),
    image=np.zeros((720, 1280, 3), dtype=np.uint8),
    fps=30,
)

world = pipeline.run(frame)

print(world)