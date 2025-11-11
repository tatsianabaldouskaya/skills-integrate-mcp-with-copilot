"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlmodel import select
from pathlib import Path
import os

from .db import init_db, get_session
from .models import Activity, ActivityParticipant


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist on startup
    init_db()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    with get_session() as session:
        activities = session.exec(select(Activity)).all()
        result = {}
        for act in activities:
            # load participants
            participants = session.exec(select(ActivityParticipant).where(ActivityParticipant.activity_id == act.id)).all()
            emails = [p.email for p in participants]
            result[act.name] = {
                "description": act.description,
                "schedule": act.schedule,
                "max_participants": act.max_participants,
                "participants": emails,
            }
        return result


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        current_count = session.exec(select(ActivityParticipant).where(ActivityParticipant.activity_id == activity.id)).count()
        if activity.max_participants is not None and current_count >= activity.max_participants:
            raise HTTPException(status_code=409, detail="Activity is full")

        already = session.exec(select(ActivityParticipant).where(ActivityParticipant.activity_id == activity.id).where(ActivityParticipant.email == email)).first()
        if already:
            raise HTTPException(status_code=400, detail="Student is already signed up")

        participant = ActivityParticipant(activity_id=activity.id, email=email)
        session.add(participant)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    with get_session() as session:
        activity = session.exec(select(Activity).where(Activity.name == activity_name)).first()
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")

        participant = session.exec(select(ActivityParticipant).where(ActivityParticipant.activity_id == activity.id).where(ActivityParticipant.email == email)).first()
        if not participant:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(participant)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
