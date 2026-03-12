from fastapi import FastAPI
from schemas import Ticket
from apps.service import run_pipeline

app = FastAPI(title="Agentic IT Support Ticket Router", version="0.1")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tickets/route")
def route_ticket(ticket: Ticket):
    return run_pipeline(ticket)