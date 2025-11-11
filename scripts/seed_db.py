from sqlmodel import Session
from src.db import init_db, engine
from src.models import Activity, ActivityParticipant


def seed():
    init_db()
    with Session(engine) as session:
        # Check if there are any activities already
        existing = session.exec(Activity.select()).first()
        if existing:
            print("DB already seeded")
            return

        activities = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
        ]

        for a in activities:
            act = Activity(name=a["name"], description=a["description"], schedule=a["schedule"], max_participants=a["max_participants"])
            session.add(act)
            session.commit()
            session.refresh(act)
            for email in a["participants"]:
                p = ActivityParticipant(activity_id=act.id, email=email)
                session.add(p)
        session.commit()
        print("Seeded DB with sample activities")


if __name__ == "__main__":
    seed()
