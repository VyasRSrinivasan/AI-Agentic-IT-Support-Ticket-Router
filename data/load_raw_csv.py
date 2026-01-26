from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator, Optional

from schemas import Ticket

DEFAULT_TICKETS_PATH = Path(__file__).parent / "tickets" / "customer_support_tickets.csv"

def load_tickets(
    csv_path: Optional[Path] = None,
    limit: Optional[int] = None,
) -> Iterator[Ticket]:
    """
    Load support tickets from a CSV file and yield normalized Ticket objects.

    - Raw CSV is treated as read-only.
    - PII fields are intentionally ignored.
    - Invalid rows are skipped safely.

    Args:
        csv_path: Optional path to CSV file
        limit: Optional max number of tickets to load

    Yields:
        Ticket objects
    """
    path = csv_path or DEFAULT_TICKETS_PATH

    if not path.exists():
        raise FileNotFoundError(f"Ticket CSV not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        count = 0
        for row in reader:
            try:
                ticket = Ticket.from_customer_support_csv_row(row)
                yield ticket
                count += 1

                if limit is not None and count >= limit:
                    break

            except Exception as e:
                # Skip bad rows without killing the pipeline
                print(f"[load_raw_csv] Skipping row due to error: {e}")
                continue