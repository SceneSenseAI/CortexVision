from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

# represents one edge of the graph

@dataclass
class Relation:

    subject_id: int

    predicate: str

    object_id: int

    relation_type: str

    confidence: float

    distance: float | None = None