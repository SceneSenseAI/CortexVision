from utils.mlflow_logger import MLFlowLogger

logger = MLFlowLogger()

from time import time
import numpy as np

from core.frame import Frame

from models.detection.detector import Detector
from models.tracking.tracker import Tracker
from models.depth.depth_estimator import DepthEstimator
from models.scene_graph.scene_graph import SceneGraphBuilder
from models.world_model.world_state import WorldModel


class CortexVisionPipeline:

    def __init__(self):

        self.detector = Detector()

        self.tracker = Tracker()

        self.depth = DepthEstimator()

        self.scene_graph = SceneGraphBuilder()

        self.world_model = WorldModel()

    def run(self):

        frame = Frame(

            frame_id=1,

            timestamp=time(),

            image=np.zeros((720, 1280, 3), dtype=np.uint8),

            fps=30

        )

        detections = self.detector.detect(frame)

        tracks = self.tracker.update(detections)

        tracks = self.depth.estimate(frame, tracks)

        scene = self.scene_graph.build(frame, tracks)

        world_state = self.world_model.update(scene)

        return world_state