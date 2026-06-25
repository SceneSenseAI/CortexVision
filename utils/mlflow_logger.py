"""
MLflow Logger

Centralized experiment tracking utility for CortexVision.

Responsibilities
----------------
- Read MLflow configuration
- Start / End experiment runs
- Log parameters
- Log metrics
- Log artifacts
- Log models
"""

from __future__ import annotations

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
    >>> logger.start_run("Detection")
    >>> logger.log_param("Detector", "YOLO-World")
    >>> logger.log_metric("FPS", 31.8)
    >>> logger.end_run()
    """

    def __init__(self, config_path: str = "configs/mlflow.yaml"):

        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(config_path)

        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)

        self.experiment_name = cfg.get("experiment_name", "Default")

        tracking_uri = cfg.get(
    "tracking_uri",
    "sqlite:///mlflow.db"
)

        mlflow.set_tracking_uri(tracking_uri)

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
    ):

        merged_tags = dict(self.default_tags)

        if tags:
            merged_tags.update(tags)

        mlflow.start_run(
            run_name=run_name,
            tags=merged_tags,
        )

    def end_run(self):

        mlflow.end_run()

    ######################################################################
    # Parameters
    ######################################################################

    def log_param(self, name: str, value: Any):

        mlflow.log_param(name, value)

    def log_params(self, params: dict[str, Any]):

        mlflow.log_params(params)

    ######################################################################
    # Metrics
    ######################################################################

    def log_metric(
        self,
        name: str,
        value: float,
        step: int | None = None,
    ):

        if step is None:
            mlflow.log_metric(name, value)
        else:
            mlflow.log_metric(name, value, step=step)

    def log_metrics(
        self,
        metrics: dict[str, float],
        step: int | None = None,
    ):

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
    ):

        mlflow.log_artifact(path, artifact_path)

    def log_artifacts(
        self,
        directory: str,
        artifact_path: str | None = None,
    ):

        mlflow.log_artifacts(directory, artifact_path)

    ######################################################################
    # Models
    ######################################################################

    def log_pytorch_model(
        self,
        model,
        artifact_path: str = "model",
    ):

        mlflow.pytorch.log_model(model, artifact_path)

    ######################################################################
    # Tags
    ######################################################################

    def set_tag(
        self,
        key: str,
        value: Any,
    ):

        mlflow.set_tag(key, value)

    ######################################################################
    # Convenience
    ######################################################################

    @staticmethod
    def active():

        return mlflow.active_run() is not None