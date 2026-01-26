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

 
    def from_customer_support_csv_row(cls, row: Dict[str, Any]) -> "Ticket":
        """
        Construct a Ticket from a row of customer_support_tickets.csv.

        Expected columns (based on your sample):
          - Ticket ID
          - Ticket Channel
          - Ticket Subject
          - Ticket Description
          - Product Purchased
          - Ticket Type
          - Ticket Priority
          - Ticket Status
          - Date of Purchase
          - First Response Time (optional)
          - Time to Resolution (optional)
          - Customer Satisfaction Rating (optional)
          - Resolution (optional)

        PII columns are intentionally ignored:
          - Customer Name
          - Customer Email
          - Customer Age
          - Customer Gender
        """
        ticket_id = cls._clean_str(row.get("Ticket ID"))
        if not ticket_id:
            raise ValueError("Missing required field: Ticket ID")

        subject = cls._clean_str(row.get("Ticket Subject")) or "(no subject)"
        body = cls._clean_str(row.get("Ticket Description")) or "(no description)"

        product = cls._clean_str(row.get("Product Purchased"))
        ticket_type = cls._clean_str(row.get("Ticket Type"))
        ticket_priority = cls._clean_str(row.get("Ticket Priority"))
        ticket_status = cls._clean_str(row.get("Ticket Status"))

        # Optional timestamps
        date_of_purchase = cls._parse_dt(row.get("Date of Purchase"))
        created_at = cls._parse_dt(row.get("Created At")) or cls._parse_dt(row.get("Ticket Created At"))

        # Keep extra non-PII fields here if useful for analysis/eval
        extras: Dict[str, Any] = {}
        for k in ("First Response Time", "Time to Resolution", "Customer Satisfaction Rating", "Resolution"):
            if k in row and row.get(k) not in (None, ""):
                extras[k] = row.get(k)

        return cls(
            ticket_id=ticket_id,
            channel=cls._normalize_channel(row.get("Ticket Channel")),
            subject=subject,
            body=body,
            product=product,
            ticket_type=ticket_type,
            ticket_priority=ticket_priority,
            ticket_status=ticket_status,
            date_of_purchase=date_of_purchase,
            created_at=created_at,
            extras=extras,
        )