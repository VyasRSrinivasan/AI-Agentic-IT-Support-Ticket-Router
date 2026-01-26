from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field

Channel = Literal["Email", "Chat", "Social media", "Web", "Phone", "Unknown"]


class Ticket(BaseModel):
    """
    Normalized ticket object used across the pipeline.

    Intentionally excludes PII fields (name/email/age/gender). Keep the original CSV immutable:
    load row -> create Ticket -> run agents.
    """

    ticket_id: str = Field(..., description="Stable identifier used in logs/UI")
    channel: Channel = Field(default="Unknown")

    subject: str = Field(..., description="Ticket title/subject")
    body: str = Field(..., description="Ticket description / main content")

    product: Optional[str] = Field(default=None, description="Product purchased/affected")
    ticket_type: Optional[str] = Field(default=None, description="Raw Ticket Type from dataset (optional hint)")
    ticket_priority: Optional[str] = Field(default=None, description="Raw Ticket Priority from dataset (optional hint)")
    ticket_status: Optional[str] = Field(default=None, description="Raw Ticket Status from dataset (optional)")

    date_of_purchase: Optional[datetime] = None
    created_at: Optional[datetime] = None

    # Keep any extra non-PII fields here (optional)
    extras: Dict[str, Any] = Field(default_factory=dict)

    def text_for_llm(self) -> str:
        """
        Canonical text passed into detector/classifier/RAG/resolver.
        Keep stable to reduce prompt drift across experiments.
        """
        parts = [
            f"Subject: {self.subject}".strip(),
            f"Body: {self.body}".strip(),
        ]
        if self.product:
            parts.append(f"Product: {self.product}".strip())
        if self.ticket_type:
            parts.append(f"Ticket Type: {self.ticket_type}".strip())
        if self.ticket_priority:
            parts.append(f"Ticket Priority: {self.ticket_priority}".strip())
        return "\n".join(parts).strip()