from pathlib import Path


class JSONExporter:

    @staticmethod
    def save(world_state, filepath: str):

        path = Path(filepath)

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            f.write(world_state.to_json())

        print(f"Saved: {path}")