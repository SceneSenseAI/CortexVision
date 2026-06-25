from utils.mlflow_logger import MLFlowLogger

logger = MLFlowLogger()

logger.start_run("MLflow Test")

logger.log_params({
    "project": "SceneSenseAI",
    "detector": "Dummy Detector"
})

logger.log_metrics({
    "fps": 30.2,
    "latency_ms": 22.5
})

logger.end_run()

print("Run logged successfully!")