from __future__ import annotations

import logging
from pathlib import Path


class CortexVisionLogger:
    """
    Central logging utility for CortexVision.

    Logs are written to both:
    - Console
    - outputs/logs/pipeline.log
    """

    def __init__(
        self,
        name: str = "CortexVision",
        log_file: str = "outputs/logs/pipeline.log",
        level: int = logging.INFO,
    ):

        Path(log_file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger(name)

        self.logger.setLevel(level)

        # Avoid duplicate handlers
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s | %(message)s",
            "%H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    # ---------------- Logging API ---------------- #

    def info(self, message: str):

        self.logger.info(message)

    def warning(self, message: str):

        self.logger.warning(message)

    def error(self, message: str):

        self.logger.error(message)

    def debug(self, message: str):

        self.logger.debug(message)

    def critical(self, message: str):

        self.logger.critical(message)

    # ---------------- Pipeline Helpers ---------------- #

    def pipeline_started(self):

        self.info("=" * 60)
        self.info("Pipeline Started")

    def pipeline_finished(self):

        self.info("Pipeline Finished")
        self.info("=" * 60)

    def frame_captured(self, frame_id: int):

        self.info(f"Captured Frame #{frame_id}")

    def stage(self, stage_name: str):

        self.info(f"{stage_name} completed")

    def objects_detected(self, count: int):

        self.info(f"Detected {count} object(s)")

    def tracks_created(self, count: int):

        self.info(f"Tracking {count} object(s)")

    def relations_created(self, count: int):

        self.info(f"Generated {count} relation(s)")

    def json_saved(self, filename: str):

        self.info(f"Saved JSON -> {filename}")

    def image_saved(self, filename: str):

        self.info(f"Saved Image -> {filename}")