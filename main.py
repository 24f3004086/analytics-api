from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key

API_KEY = "ak_jterj68e69pbvmxn5ufq0tl4"


EMAIL = "24f3004086@ds.study.iitm.ac.in"

# Models

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class EventRequest(BaseModel):
    events: List[Event]

# Endpoint

@app.post("/analytics")
def analytics(
    data: EventRequest,
    x_api_key: str = Header(None)
):

    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(data.events)

    unique_users = len(set(event.user for event in data.events))

    revenue = 0

    user_totals = {}

    for event in data.events:

        if event.amount > 0:

            revenue += event.amount

            user_totals[event.user] = (
                user_totals.get(event.user, 0)
                + event.amount
            )

    if user_totals:
        top_user = max(user_totals, key=user_totals.get)
    else:
        top_user = ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }