from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

# represents one edge of the graph

@dataclass

class Relation:

    subject_id: int

    object_id: int

    predicate: str

    confidence: float

    distance: float | None = None
    def to_dict(self):

        return {

            "subject_id": self.subject_id,

            "object_id": self.object_id,

            "predicate": self.predicate,

            "confidence": self.confidence,

            "distance": self.distance

        }