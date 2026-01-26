from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field

Channel = Literal("Email", "Chat", "Social media", "Web", "Phone", "Unknown")

class Ticket(BaseModel):
    ticket_id: str = Field(..., description="Stable identifier used in logs/UI")
    channel: Channel = Field(default="Unknown")

    subject: str = Field(..., description="Short summary/title of the ticket")
    body: str = Field(..., description="Main ticket text/description")

    product: Optional[str] = Field(default=None, description="Product purchased or affected")
    ticket_type: Optional[str] = Field(default=None, description="Raw ticket type/category from dataset")
    ticket_priority: Optional[str] = Field(default=None, description="Raw priority from dataset")
    ticket_status: Optional[str] = Field(default=None, description="Raw status from dataset")

    date_of_purchase: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None, description="Ticket creation timestamp if available")

    def textForLLM(self):
        parts = [f"Subject: {self.subject}", f"Body: {self.body}"]
        if self.product:
            parts.append(f"Product: {self.product}")
        return "\n".join(parts)
