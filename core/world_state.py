from dataclasses import dataclass, field
from datetime import datetime
from typing import List 
from pathlib import Path
from core.scene import Scene
from core.event import Event
import json
from core.HistoryBuffer import HistoryBuffer

@dataclass
class WorldState:

    current_scene: Scene

    history: HistoryBuffer

    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):

        return {

            "current_scene":

                self.current_scene.to_dict(),

            "history":

                self.history.to_dict(),

            "created_at":

                str(self.created_at)

        }

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict(), indent=4)
    def save_json(self, filename: str):

        path = Path(filename)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(path, "w") as f:
            json.dump(
                self.to_dict(),
                f,
                indent=4,
            )

        print(f"Saved: {path}")
    def __repr__(self) -> str:

        lines = []

        lines.append(str(self.current_scene))

        lines.append("\nHistory")
        lines.append("-" * 20)

        lines.append(f"Scenes : {len(self.history.scenes)}")
        lines.append(f"Events : {len(self.history.events)}")

        return "\n".join(lines)