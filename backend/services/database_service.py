from models import Lecturer, Room, Timeslot, Course, ExamPeriod, Exam
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

def get_exam_periods_data():
    exam_periods = ExamPeriod.query.all()
    return [{"id": ep.id, "day": ep.day, "time": ep.time, "duration": ep.duration} for ep in exam_periods]

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

def get_exams_dataframe():
    exams = Exam.query.all()
    data = []
    for e in exams:
        data.append({
            "course": e.course.name,
            "lecturer": e.course.lecturer.name,
            "group": e.course.group,
            "students": e.course.students,
            "duration": e.duration,
            "required_room_type": e.required_room_type
        })
    return pd.DataFrame(data)