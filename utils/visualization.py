import cv2
import numpy as np

from core.scene import Scene
from core.track import Track
from core.Relation import Relation
from core.world_state import WorldState
from pathlib import Path


class Visualizer:

    # -------------------- COLORS (BGR) --------------------

    BOX_COLOR  = (60, 220, 60)
    BOX_FILL   = (45, 45, 45)
    TEXT       = (255, 255, 255)
    DEPTH      = (255, 255, 0)
    RELATION   = (255, 120, 0)
    CENTROID   = (0, 0, 255)
    HUD_BG     = (30, 30, 30)
    HUD_BORDER = (0, 255, 255)
    FOOTER     = (45, 45, 45)

    # -------------------- HELPERS --------------------

    @staticmethod
    def put_text(
        image: np.ndarray,
        text: str,
        origin: tuple[int, int],
        scale: float = 0.55,
        color: tuple[int, int, int] | None = None,
        thickness: int = 1,
        font: int = cv2.FONT_HERSHEY_SIMPLEX,
    ) -> np.ndarray:
        """Draw anti-aliased text onto image (in-place)."""
        if color is None:
            color = Visualizer.TEXT
        cv2.putText(image, text, origin, font, scale, color, thickness, cv2.LINE_AA)
        return image

    @staticmethod
    def draw_panel(
        image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        alpha: float = 0.45,
        bg_color: tuple[int, int, int] | None = None,
        border_color: tuple[int, int, int] | None = None,
        border_thickness: int = 2,
    ) -> np.ndarray:
        """Draw a semi-transparent filled panel with a border; returns a copy."""
        if bg_color is None:
            bg_color = Visualizer.HUD_BG
        if border_color is None:
            border_color = Visualizer.HUD_BORDER

        output  = image.copy()
        overlay = output.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), bg_color, -1)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
        cv2.rectangle(output, (x, y), (x + w, y + h), border_color, border_thickness)
        return output

    @staticmethod
    def draw_label(
        image: np.ndarray,
        text: str,
        origin: tuple[int, int],
        scale: float = 0.45,
        text_color: tuple[int, int, int] | None = None,
        bg_color: tuple[int, int, int] = (30, 30, 30),
        padding: int = 4,
    ) -> np.ndarray:
        """Draw text inside a small dark background rectangle (in-place)."""
        if text_color is None:
            text_color = Visualizer.RELATION
        font = cv2.FONT_HERSHEY_SIMPLEX
        (tw, th), baseline = cv2.getTextSize(text, font, scale, 1)
        x, y = origin
        cv2.rectangle(
            image,
            (x - padding,      y - th - padding),
            (x + tw + padding, y + baseline + padding),
            bg_color,
            -1,
        )
        cv2.putText(image, text, (x, y), font, scale, text_color, 1, cv2.LINE_AA)
        return image

    # -------------------- DRAWING --------------------

    @staticmethod
    def draw_bboxes(
        image: np.ndarray,
        tracks: list[Track],
    ) -> np.ndarray:
        output = image.copy()
        for track in tracks:
            x1, y1, x2, y2 = track.scene_object.bbox
            cv2.rectangle(output, (x1, y1), (x2, y2), Visualizer.BOX_COLOR, 2)
        return output

    @staticmethod
    def draw_tracks(
        image: np.ndarray,
        tracks: list[Track],
    ) -> np.ndarray:
        output = image.copy()
        for track in tracks:
            obj   = track.scene_object
            x1, y1, x2, y2 = obj.bbox
            label = obj.label.capitalize()

            cv2.rectangle(output, (x1, y1 - 42), (x1 + 170, y1), Visualizer.BOX_FILL,  -1)
            cv2.rectangle(output, (x1, y1 - 42), (x1 + 170, y1), Visualizer.BOX_COLOR,  2)

            Visualizer.put_text(
                output,
                f"{label} #{track.track_id}",
                (x1 + 6, y1 - 23),
                scale=0.55,
                color=Visualizer.TEXT,
                thickness=2,
            )
            Visualizer.put_text(
                output,
                f"Conf : {obj.confidence * 100:.1f}%",
                (x1 + 6, y1 - 6),
                scale=0.45,
                color=Visualizer.TEXT,
                thickness=1,
            )
        return output

    @staticmethod
    def draw_depth(
        image: np.ndarray,
        tracks: list[Track],
    ) -> np.ndarray:
        output = image.copy()
        for track in tracks:
            x1, _, _, y2 = track.scene_object.bbox
            depth = track.scene_object.depth
            if depth is None:
                continue
            Visualizer.put_text(
                output, "Depth",
                (x1, y2 + 18),
                scale=0.42,
                color=Visualizer.DEPTH,
                thickness=1,
            )
            Visualizer.put_text(
                output, f"{depth:.2f} m",
                (x1, y2 + 38),
                scale=0.55,
                color=Visualizer.DEPTH,
                thickness=2,
            )
        return output

    @staticmethod
    def draw_relations(
        image: np.ndarray,
        scene: Scene,
    ) -> np.ndarray:
        output = image.copy()
        lookup = {track.track_id: track for track in scene.tracks}

        for relation in scene.relations:
            if relation.subject_id not in lookup:
                continue
            if relation.object_id not in lookup:
                continue

            subject = lookup[relation.subject_id]
            target  = lookup[relation.object_id]

            c1 = tuple(map(int, subject.scene_object.centroid))
            c2 = tuple(map(int, target.scene_object.centroid))

            # Anti-aliased relation line
            cv2.line(output, c1, c2, Visualizer.RELATION, 2, cv2.LINE_AA)

            # Centroids — filled inner dot + outlined ring
            for c in (c1, c2):
                cv2.circle(output, c, 4, Visualizer.CENTROID, -1)
                cv2.circle(output, c, 8, Visualizer.CENTROID,  2)

            mx = (c1[0] + c2[0]) // 2
            my = (c1[1] + c2[1]) // 2

            Visualizer.draw_label(output, relation.predicate, (mx - 35, my - 15))
            if relation.distance is not None:
                Visualizer.draw_label(output, f"{relation.distance:.2f} m", (mx - 22, my + 12))

        return output

    @staticmethod
    def draw_hud(
        image: np.ndarray,
        world_state: WorldState,
    ) -> np.ndarray:
        scene   = world_state.current_scene
        h, w    = image.shape[:2]
        panel_w = 270
        panel_h = 165
        start_x = w - panel_w - 20
        start_y = 20

        output = Visualizer.draw_panel(image, start_x, start_y, panel_w, panel_h)

        Visualizer.put_text(
            output, "CortexVision",
            (start_x + 15, start_y + 25),
            scale=0.75,
            color=Visualizer.HUD_BORDER,
            thickness=2,
        )

        stats = [
            f"Frame      : {scene.frame.frame_id}",
            f"FPS        : {scene.frame.fps:.1f}",
            f"Objects    : {len(scene.tracks)}",
            f"Relations  : {len(scene.relations)}",
            f"Events     : {len(world_state.history.events)}",
        ]

        y = start_y + 50
        for s in stats:
            Visualizer.put_text(output, s, (start_x + 15, y), scale=0.55)
            y += 22

        return output

    @staticmethod
    def draw_footer(
        image: np.ndarray,
        world_state: WorldState,
    ) -> np.ndarray:
        output = image.copy()
        h, w   = output.shape[:2]
        scene  = world_state.current_scene

        overlay = output.copy()
        cv2.rectangle(overlay, (0, h - 35), (w, h), (40, 40, 40), -1)
        cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)

        text = (
            f"Frame: {scene.frame.frame_id}    "
            f"FPS: {scene.frame.fps:.1f}    "
            f"Objects: {len(scene.tracks)}    "
            f"Relations: {len(scene.relations)}"
        )

        (text_w, _), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        text_x = (w - text_w) // 2

        Visualizer.put_text(output, text, (text_x, h - 12), scale=0.6, thickness=1)

        return output

    @staticmethod
    def draw_world_state(
        world_state: WorldState,
    ) -> np.ndarray:
        scene = world_state.current_scene
        image = scene.frame.image.copy()

        image = Visualizer.draw_bboxes(image, scene.tracks)
        image = Visualizer.draw_tracks(image, scene.tracks)
        image = Visualizer.draw_depth(image, scene.tracks)
        image = Visualizer.draw_relations(image, scene)
        image = Visualizer.draw_hud(image, world_state)
        image = Visualizer.draw_footer(image, world_state)

        return image

    @staticmethod
    def save(
        image: np.ndarray,
        filename: str | Path,
    ) -> None:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), image)
        print(f"Saved image -> {path}")