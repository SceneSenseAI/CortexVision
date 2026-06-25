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