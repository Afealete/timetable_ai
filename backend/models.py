from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lecturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unavailable_slots = db.Column(db.Text)  # JSON string of unavailable timeslot IDs

class Room(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)

class Timeslot(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    group = db.Column(db.String(50), nullable=False)
    students = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.String(10), db.ForeignKey('room.id'))

    lecturer = db.relationship('Lecturer', backref=db.backref('courses', lazy=True, cascade='all, delete-orphan'))
    room = db.relationship('Room', backref=db.backref('courses', lazy=True))

class ExamPeriod(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    required_room_type = db.Column(db.String(50))  # e.g., 'exam_hall', 'lab'

    course = db.relationship('Course', backref=db.backref('exams', lazy=True))