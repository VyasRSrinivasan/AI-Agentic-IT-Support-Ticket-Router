from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, confloat

Urgency = Literal["Low", "Medium", "High", "Critical"]
Complexity = Literal["Simple", "Moderate", "Complex"]


class TriageOutput(BaseModel):
    """
    Output of agents/classifier.py.
    """

    department: str = Field(..., description="Routing label/queue name (e.g., Billing, Account, Technical Support)")
    urgency: Urgency
    complexity: Complexity

    confidence: confloat(ge=0.0, le=1.0) = 0.5

    summary: List[str] = Field(default_factory=list, description="2–5 bullet points for human context")
    entities: List[str] = Field(default_factory=list, description="Key extracted entities (optional)")
    sentiment: Optional[Literal["Negative", "Neutral", "Positive"]] = None