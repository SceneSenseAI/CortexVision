from pathlib import Path
from time import time

from core.frame import Frame

from models.detection.detector import Detector
from models.tracking.tracker import Tracker
from models.depth.depth_estimator import DepthEstimator
from models.scene_graph.scene_graph import SceneGraphBuilder
from models.world_model.world_state import WorldModel

from utils.logger import CortexVisionLogger
from utils.mlflow_logger import MLFlowLogger
from utils.visualization import Visualizer


logger = CortexVisionLogger()
mlflow = MLFlowLogger()


class CortexVisionPipeline:

    def __init__(self):
        self.detector    = Detector()
        self.tracker     = Tracker()
        self.depth       = DepthEstimator()
        self.scene_graph = SceneGraphBuilder()
        self.world_model = WorldModel()

    def run(
    self,
    frame: Frame,
    save_outputs: bool = True,  
    log_to_mlflow: bool = True,
    verbose=False    # VEBROSE FALSE FOR DEMOS
    ):
        if verbose:
            logger.pipeline_started()

        with mlflow.pipeline("Dummy Pipeline"):

            # --------------------------------------------------
            # Run Metadata
            # --------------------------------------------------

            mlflow.log_pipeline_info(
                detector="DummyDetector",
                tracker="DummyTracker",
                depth="DummyDepth",
            )
            mlflow.set_tag("detector",   "DummyDetector")
            mlflow.set_tag("tracker",    "DummyTracker")
            mlflow.set_tag("depth",      "DummyDepth")
            mlflow.set_tag("git_branch", "main")          # TODO: automate

            mlflow.log_system_info()
            mlflow.log_git_commit()

            mlflow.log_params({
                "image_width":  frame.image.shape[1],
                "image_height": frame.image.shape[0],
                "fps":          frame.fps,
            })

            for cfg in ("configs/mlflow.yaml", "configs/models.yaml"):
                if Path(cfg).exists():
                    mlflow.log_config(cfg)

            # --------------------------------------------------
            # Frame
            # --------------------------------------------------

            logger.frame_captured(frame.frame_id)
            pipeline_start = time()

            # --------------------------------------------------
            # Detection
            # --------------------------------------------------

            det_start  = time()
            detections = self.detector.detect(frame)
            det_ms     = (time() - det_start) * 1000

            logger.objects_detected(len(detections))
            mlflow.log_metric("num_detections", len(detections))
            mlflow.log_metric("detector_ms",    det_ms)

            # --------------------------------------------------
            # Tracking
            # --------------------------------------------------

            track_start = time()
            tracks      = self.tracker.update(detections)
            track_ms    = (time() - track_start) * 1000

            logger.tracks_created(len(tracks))
            mlflow.log_metric("num_tracks", len(tracks))
            mlflow.log_metric("tracker_ms", track_ms)

            # --------------------------------------------------
            # Depth
            # --------------------------------------------------

            depth_start = time()
            tracks      = self.depth.estimate(frame, tracks)
            depth_ms    = (time() - depth_start) * 1000

            mlflow.log_metric("depth_ms", depth_ms)

            # --------------------------------------------------
            # Scene Graph
            # --------------------------------------------------

            scene_start = time()
            scene       = self.scene_graph.build(frame, tracks)
            scene_ms    = (time() - scene_start) * 1000

            logger.relations_created(len(scene.relations))
            mlflow.log_metric("num_relations",  len(scene.relations))
            mlflow.log_metric("scene_graph_ms", scene_ms)

            # --------------------------------------------------
            # World Model
            # --------------------------------------------------

            world_start = time()
            world_state = self.world_model.update(scene)
            world_ms    = (time() - world_start) * 1000

            mlflow.log_metric("world_model_ms", world_ms)

            # --------------------------------------------------
            # Save JSON
            # --------------------------------------------------

            world_state.save_json("outputs/json/world_state.json")
            logger.json_saved("outputs/json/world_state.json")
            mlflow.log_json("outputs/json/world_state.json")

            # --------------------------------------------------
            # Visualization
            # --------------------------------------------------

            image = Visualizer.draw_world_state(world_state)
            Visualizer.save(image, "outputs/images/annotated_frame.jpg")
            logger.image_saved("outputs/images/annotated_frame.jpg")
            mlflow.log_image("outputs/images/annotated_frame.jpg")

            # --------------------------------------------------
            # Pipeline Summary
            # --------------------------------------------------

            pipeline_ms = (time() - pipeline_start) * 1000
            fps         = 1000.0 / pipeline_ms if pipeline_ms > 0 else 0.0

            mlflow.log_metric("pipeline_time_ms", pipeline_ms)
            mlflow.log_metric("pipeline_fps",     fps)

            summary = (
                f"\n{'='*34}\n"
                f" Pipeline Summary\n"
                f"{'='*34}\n"
                f" Detector      : {det_ms:>8.2f} ms\n"
                f" Tracker       : {track_ms:>8.2f} ms\n"
                f" Depth         : {depth_ms:>8.2f} ms\n"
                f" Scene Graph   : {scene_ms:>8.2f} ms\n"
                f" World Model   : {world_ms:>8.2f} ms\n"
                f"{'-'*34}\n"
                f" Total         : {pipeline_ms:>8.2f} ms\n"
                f" FPS           : {fps:>8.2f}\n"
                f"{'='*34}"
            )
            logger.info(summary)

            logger.pipeline_finished()

            return world_state, image