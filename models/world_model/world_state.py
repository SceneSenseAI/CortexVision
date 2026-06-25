from core.scene import Scene
from core.world_state import WorldState
from core.HistoryBuffer import HistoryBuffer


class WorldModel:
    """
    Dummy world model.

    Later:
        Temporal reasoning
        Event engine
        Future prediction
    """

    def __init__(self):

        self.history = HistoryBuffer()

    def update(

        self,

        scene: Scene

    ) -> WorldState:

        self.history.scenes.append(scene)

        world = WorldState(

            current_scene=scene,

            history=self.history

        )

        return world