from flask import Blueprint, request, jsonify
from models import db, Lecturer, Room, Timeslot, Course, ExamPeriod, Exam
import json

data_bp = Blueprint("data", __name__)

# Lecturer CRUD
@data_bp.route("/lecturers", methods=["GET"])
def get_lecturers():
    lecturers = Lecturer.query.all()
    return jsonify([{
        "id": l.id,
        "name": l.name,
        "unavailable_slots": json.loads(l.unavailable_slots) if l.unavailable_slots else []
    } for l in lecturers])

@data_bp.route("/lecturers", methods=["POST"])
def add_lecturer():
    data = request.json
    lecturer = Lecturer(
        name=data['name'],
        unavailable_slots=json.dumps(data.get('unavailable_slots', []))
    )
    db.session.add(lecturer)
    db.session.commit()
    return jsonify({"id": lecturer.id, "message": "Lecturer added"}), 201

@data_bp.route("/lecturers/<int:id>", methods=["PUT"])
def update_lecturer(id):
    lecturer = Lecturer.query.get_or_404(id)
    data = request.json
    lecturer.name = data['name']
    lecturer.unavailable_slots = json.dumps(data.get('unavailable_slots', []))
    db.session.commit()
    return jsonify({"message": "Lecturer updated"})

@data_bp.route("/lecturers/<int:id>", methods=["DELETE"])
def delete_lecturer(id):
    lecturer = Lecturer.query.get_or_404(id)
    db.session.delete(lecturer)
    db.session.commit()
    return jsonify({"message": "Lecturer deleted"})

# Room CRUD
@data_bp.route("/rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{"id": r.id, "capacity": r.capacity} for r in rooms])

@data_bp.route("/rooms", methods=["POST"])
def add_room():
    data = request.json
    room = Room(id=data['id'], capacity=data['capacity'])
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room added"}), 201

@data_bp.route("/rooms/<string:id>", methods=["PUT"])
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.json
    room.capacity = data['capacity']
    db.session.commit()
    return jsonify({"message": "Room updated"})

@data_bp.route("/rooms/<string:id>", methods=["DELETE"])
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted"})

# Timeslot CRUD
@data_bp.route("/timeslots", methods=["GET"])
def get_timeslots():
    timeslots = Timeslot.query.all()
    return jsonify([{"id": t.id, "day": t.day, "time": t.time} for t in timeslots])

@data_bp.route("/timeslots", methods=["POST"])
def add_timeslot():
    data = request.json
    timeslot = Timeslot(id=data['id'], day=data['day'], time=data['time'])
    db.session.add(timeslot)
    db.session.commit()
    return jsonify({"message": "Timeslot added"}), 201

@data_bp.route("/timeslots/<string:id>", methods=["PUT"])
def update_timeslot(id):
    timeslot = Timeslot.query.get_or_404(id)
    data = request.json
    timeslot.day = data['day']
    timeslot.time = data['time']
    db.session.commit()
    return jsonify({"message": "Timeslot updated"})

@data_bp.route("/timeslots/<string:id>", methods=["DELETE"])
def delete_timeslot(id):
    timeslot = Timeslot.query.get_or_404(id)
    db.session.delete(timeslot)
    db.session.commit()
    return jsonify({"message": "Timeslot deleted"})

# Course CRUD
@data_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "lecturer": c.lecturer.name,
        "group": c.group,
        "students": c.students,
        "capacity": c.capacity,
        "room": c.room.id if c.room else None
    } for c in courses])

@data_bp.route("/courses", methods=["POST"])
def add_course():
    data = request.json
    lecturer = Lecturer.query.filter_by(name=data['lecturer']).first()
    if not lecturer:
        return jsonify({"error": "Lecturer not found"}), 400
    room = Room.query.get(data['room']) if data.get('room') else None
    course = Course(
        name=data['name'],
        lecturer_id=lecturer.id,
        group=data['group'],
        students=data['students'],
        capacity=data['capacity'],
        room_id=room.id if room else None
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({"id": course.id, "message": "Course added"}), 201

@data_bp.route("/courses/<int:id>", methods=["PUT"])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.json
    lecturer = Lecturer.query.filter_by(name=data['lecturer']).first()
    if not lecturer:
        return jsonify({"error": "Lecturer not found"}), 400
    room = Room.query.get(data['room']) if data.get('room') else None
    course.name = data['name']
    course.lecturer_id = lecturer.id
    course.group = data['group']
    course.students = data['students']
    course.capacity = data['capacity']
    course.room_id = room.id if room else None
    db.session.commit()
    return jsonify({"message": "Course updated"})

@data_bp.route("/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted"})

# ExamPeriod CRUD
@data_bp.route("/exam-periods", methods=["GET"])
def get_exam_periods():
    exam_periods = ExamPeriod.query.all()
    return jsonify([{"id": ep.id, "day": ep.day, "time": ep.time, "duration": ep.duration} for ep in exam_periods])

@data_bp.route("/exam-periods", methods=["POST"])
def add_exam_period():
    data = request.json
    exam_period = ExamPeriod(id=data['id'], day=data['day'], time=data['time'], duration=data['duration'])
    db.session.add(exam_period)
    db.session.commit()
    return jsonify({"message": "Exam period added"}), 201

@data_bp.route("/exam-periods/<string:id>", methods=["PUT"])
def update_exam_period(id):
    exam_period = ExamPeriod.query.get_or_404(id)
    data = request.json
    exam_period.day = data['day']
    exam_period.time = data['time']
    exam_period.duration = data['duration']
    db.session.commit()
    return jsonify({"message": "Exam period updated"})

@data_bp.route("/exam-periods/<string:id>", methods=["DELETE"])
def delete_exam_period(id):
    exam_period = ExamPeriod.query.get_or_404(id)
    db.session.delete(exam_period)
    db.session.commit()
    return jsonify({"message": "Exam period deleted"})

# Exam CRUD
@data_bp.route("/exams", methods=["GET"])
def get_exams():
    exams = Exam.query.all()
    return jsonify([{
        "id": e.id,
        "course": e.course.name,
        "duration": e.duration,
        "required_room_type": e.required_room_type
    } for e in exams])

@data_bp.route("/exams", methods=["POST"])
def add_exam():
    data = request.json
    course = Course.query.filter_by(name=data['course']).first()
    if not course:
        return jsonify({"error": "Course not found"}), 400
    exam = Exam(
        course_id=course.id,
        duration=data['duration'],
        required_room_type=data.get('required_room_type')
    )
    db.session.add(exam)
    db.session.commit()
    return jsonify({"id": exam.id, "message": "Exam added"}), 201

@data_bp.route("/exams/<int:id>", methods=["PUT"])
def update_exam(id):
    exam = Exam.query.get_or_404(id)
    data = request.json
    course = Course.query.filter_by(name=data['course']).first()
    if not course:
        return jsonify({"error": "Course not found"}), 400
    exam.course_id = course.id
    exam.duration = data['duration']
    exam.required_room_type = data.get('required_room_type')
    db.session.commit()
    return jsonify({"message": "Exam updated"})

@data_bp.route("/exams/<int:id>", methods=["DELETE"])
def delete_exam(id):
    exam = Exam.query.get_or_404(id)
    db.session.delete(exam)
    db.session.commit()
    return jsonify({"message": "Exam deleted"})