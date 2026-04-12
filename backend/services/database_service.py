from models import Lecturer, Room, Timeslot, Course
import pandas as pd
import json

def get_lecturers_data():
    lecturers = Lecturer.query.all()
    return [{"id": l.id, "name": l.name, "unavailable_slots": json.loads(l.unavailable_slots) if l.unavailable_slots else []} for l in lecturers]

def get_rooms_data():
    rooms = Room.query.all()
    return [{"id": r.id, "capacity": r.capacity} for r in rooms]

def get_timeslots_data():
    timeslots = Timeslot.query.all()
    return [{"id": t.id, "day": t.day, "time": t.time} for t in timeslots]

def get_courses_dataframe():
    courses = Course.query.all()
    data = []
    for c in courses:
        data.append({
            "course": c.name,
            "lecturer": c.lecturer.name,
            "group": c.group,
            "students": c.students,
            "capacity": c.capacity,
            "room": c.room.id if c.room else None
        })
    return pd.DataFrame(data)