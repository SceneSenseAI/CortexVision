"""
MLflow Logger

Centralized experiment tracking utility for CortexVision.

Responsibilities
----------------
- Read MLflow configuration
- Start / End experiment runs
- Log parameters, metrics, artifacts
- Log models, system info, git commit
"""

from __future__ import annotations

import platform
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import mlflow
import yaml


class MLFlowLogger:
    """
    Wrapper around MLflow.

    Example
    -------
    >>> logger = MLFlowLogger("configs/mlflow.yaml")
    >>> with logger.pipeline("Dummy Pipeline"):
    ...     logger.log_pipeline_info("YOLOWorld", "ByteTrack", "DepthPro")
    ...     logger.log_metric("fps", 31.8)
    """

    def __init__(self, config_path: str = "configs/mlflow.yaml"):

        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(config_path)

        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.experiment_name = cfg.get("experiment_name", "Default")

        tracking_uri = cfg.get("tracking_uri", "sqlite:///mlflow.db")

        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(self.experiment_name)

        self.default_tags = cfg.get("tags", {})

    ######################################################################
    # Run Management
    ######################################################################

    def start_run(
        self,
        run_name: str | None = None,
        tags: dict[str, Any] | None = None,
    ) -> None:
        if mlflow.active_run() is not None:
            mlflow.end_run()

        merged_tags = dict(self.default_tags)
        if tags:
            merged_tags.update(tags)

        mlflow.start_run(run_name=run_name, tags=merged_tags)

    def end_run(self) -> None:
        mlflow.end_run()

    def close(self) -> None:
        """End the active run if one exists. Safe to call at any time."""
        if mlflow.active_run():
            mlflow.end_run()

    @contextmanager
    def run(
        self,
        run_name: str | None = None,
        tags: dict[str, Any] | None = None,
    ):
        """Context manager for a single MLflow run.

        >>> with logger.run("Detection"):
        ...     logger.log_metric("fps", 31.5)
        """
        self.start_run(run_name, tags)
        try:
            yield self
        finally:
            self.end_run()

    @contextmanager
    def pipeline(self, name: str):
        """Top-level pipeline context manager. Alias for run().

        >>> with logger.pipeline("Dummy Pipeline"):
        ...     logger.log_metric("fps", 31.5)
        """
        self.start_run(name)
        try:
            yield self
        finally:
            self.end_run()

    ######################################################################
    # Parameters
    ######################################################################

    def log_param(self, name: str, value: Any) -> None:
        mlflow.log_param(name, value)

    def log_params(self, params: dict[str, Any]) -> None:
        mlflow.log_params(params)

    def log_pipeline_info(
        self,
        detector: str,
        tracker: str,
        depth: str,
    ) -> None:
        """Log the three core model components as run parameters.

        >>> logger.log_pipeline_info("YOLOWorld", "ByteTrack", "DepthPro")
        """
        self.log_params({
            "detector": detector,
            "tracker":  tracker,
            "depth":    depth,
        })

    def log_system_info(self) -> None:
        """Log OS and Python version. Extend later with CUDA / GPU / TensorRT."""
        self.log_params({
            "platform": platform.platform(),
            "python":   platform.python_version(),
        })

    ######################################################################
    # Metrics
    ######################################################################

    def log_metric(
        self,
        name: str,
        value: float,
        step: int | None = None,
    ) -> None:
        if step is None:
            mlflow.log_metric(name, value)
        else:
            mlflow.log_metric(name, value, step=step)

    def log_metrics(
        self,
        metrics: dict[str, float],
        step: int | None = None,
    ) -> None:
        if step is None:
            mlflow.log_metrics(metrics)
        else:
            for k, v in metrics.items():
                mlflow.log_metric(k, v, step=step)

    ######################################################################
    # Artifacts
    ######################################################################

    def log_artifact(
        self,
        path: str,
        artifact_path: str | None = None,
    ) -> None:
        mlflow.log_artifact(path, artifact_path)

    def log_artifacts(
        self,
        directory: str,
        artifact_path: str | None = None,
    ) -> None:
        mlflow.log_artifacts(directory, artifact_path)

    def log_image(self, image_path: str) -> None:
        """Log an annotated frame / visualization → artifacts/images/."""
        mlflow.log_artifact(image_path, artifact_path="images")

    def log_json(self, json_path: str) -> None:
        """Log a world-state export → artifacts/json/."""
        mlflow.log_artifact(json_path, artifact_path="json")

    def log_config(self, config_path: str) -> None:
        """Log a YAML/JSON config file → artifacts/configs/."""
        mlflow.log_artifact(config_path, artifact_path="configs")

    def log_directory(self, directory: str) -> None:
        """Log all files in a local directory as artifacts."""
        mlflow.log_artifacts(directory)

    ######################################################################
    # Models
    ######################################################################

    def log_pytorch_model(
        self,
        model,
        artifact_path: str = "model",
    ) -> None:
        mlflow.pytorch.log_model(model, artifact_path)

    ######################################################################
    # Tags
    ######################################################################

    def set_tag(self, key: str, value: Any) -> None:
        mlflow.set_tag(key, value)

    ######################################################################
    # Git
    ######################################################################

    def log_git_commit(self) -> None:
        """Tag the run with the current HEAD SHA. Silent on failure."""
        try:
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"]
            ).decode().strip()
            self.set_tag("git_commit", commit)
        except Exception:
            pass

    ######################################################################
    # Utilities
    ######################################################################

    @staticmethod
    def active() -> bool:
        return mlflow.active_run() is not None

    def log_stage_time(
    self,
    stage: str,
    milliseconds: float,
    ):
        self.log_metric(
            f"{stage.lower()}_ms",
            milliseconds,
    )