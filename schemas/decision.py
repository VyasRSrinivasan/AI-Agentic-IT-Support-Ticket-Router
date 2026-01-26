from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, confloat

DecisionType = Literal["AUTO_RESOLVE", "ESCALATE", "ASK_CLARIFYING"]
EscalationLevel = Literal["None", "L1", "L2", "Security"]


class Decision(BaseModel):
    """
    Final decision produced by your router/decider logic (often a LangGraph node).
    """

    decision: DecisionType
    reason: str = ""

    confidence: confloat(ge=0.0, le=1.0) = 0.5

    # Escalation fields
    target_queue: Optional[str] = Field(default=None, description="Queue/team to route to (e.g., Billing, Security)")
    escalation_level: EscalationLevel = "None"

    # Clarifying question path (optional)
    clarifying_questions: Optional[list[str]] = None