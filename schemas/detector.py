from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

Risk = Literal["Low", "Medium", "High"]


class DetectorOutput(BaseModel):
    """
    Output of agents/detector.py.
    Detector should only surface signals/flags (not route or resolve).
    """

    security_risk: Risk = "Low"
    missing_info: bool = False
    signals: List[str] = Field(default_factory=list, description="Human-readable flags for auditing/debugging")