import json
from datetime import datetime

import streamlit as st

from apps.service import run_pipeline
from schemas import Ticket

CHANNEL_OPTIONS = ["Email", "Chat", "Social media", "Web", "Phone", "Unknown"]

st.set_page_config(page_title="Agentic IT Support Ticket Router", layout="wide")
st.title("Agentic IT Support Ticket Router")
st.markdown(
    "Use this interface to submit a ticket into the router pipeline and inspect the returned triage, decision, resolution, and verification outputs."
)

with st.form("ticket_form"):
    ticket_id = st.text_input("Ticket ID", value="TICKET-001")
    channel = st.selectbox("Channel", CHANNEL_OPTIONS, index=0)
    subject = st.text_input("Subject", value="Unable to access account")
    body = st.text_area(
        "Body",
        value="I can't access my account after a password reset. The login page shows an error and I need help.",
        height=180,
    )
    product = st.text_input("Product", value="")
    ticket_type = st.text_input("Ticket Type", value="")
    ticket_priority = st.text_input("Ticket Priority", value="")
    ticket_status = st.text_input("Ticket Status", value="")
    created_at = st.text_input(
        "Created At (ISO format)", value=datetime.now().isoformat(timespec="seconds")
    )
    extras_text = st.text_area(
        "Extras (JSON)",
        value="{}",
        help="Optional JSON metadata fields such as customer satisfaction or response SLA.",
        height=120,
    )

    submit = st.form_submit_button("Route Ticket")

if submit:
    try:
        extras = json.loads(extras_text) if extras_text.strip() else {}
        created_at_dt = None
        if created_at.strip():
            created_at_dt = datetime.fromisoformat(created_at.strip())

        ticket = Ticket(
            ticket_id=ticket_id.strip() or "TICKET-001",
            channel=channel,
            subject=subject.strip() or "(no subject)",
            body=body.strip() or "(no body)",
            product=product.strip() or None,
            ticket_type=ticket_type.strip() or None,
            ticket_priority=ticket_priority.strip() or None,
            ticket_status=ticket_status.strip() or None,
            created_at=created_at_dt,
            extras=extras,
        )

        st.info("Running ticket pipeline...")
        result = run_pipeline(ticket)

        st.success("Ticket routed successfully")

        st.subheader("Pipeline Output")
        st.json(result)

        if "decision" in result:
            st.subheader("Decision Summary")
            decision = result["decision"]
            st.write(
                f"**{decision.get('decision', 'UNKNOWN')}** — {decision.get('reason', '')}"
            )
            if decision.get("escalation_level"):
                st.write(f"Escalation level: {decision['escalation_level']}")

        if "triage" in result:
            st.subheader("Triage Summary")
            triage = result["triage"]
            st.write(
                f"Department: {triage.get('department', 'Unknown')} | "
                f"Urgency: {triage.get('urgency', 'Unknown')} | "
                f"Complexity: {triage.get('complexity', 'Unknown')}"
            )

    except Exception as error:
        st.error(f"Unable to route ticket: {error}")
        st.exception(error)
