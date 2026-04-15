#!/usr/bin/env python3
"""
Quick Setup Script - Bulk Import Sample Data
Run this from the backend directory: python setup_sample_data.py
"""

import json
import os
import sys
from models import db, Lecturer, Room, Timeslot, ExamPeriod, Exam, Course
from app import app

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
        return json.load(f)

def setup_lecturers():
    print("📚 Setting up lecturers...")
    lecturers_data = load_json('lecturers_sample.json')
    
    for lect_data in lecturers_data:
        existing = Lecturer.query.filter_by(name=lect_data['name']).first()
        if not existing:
            lecturer = Lecturer(
                name=lect_data['name'],
                unavailable_slots=json.dumps(lect_data.get('unavailable_slots', []))
            )
            db.session.add(lecturer)
            print(f"  ✓ Added {lect_data['name']}")
    
    db.session.commit()
    print("✅ Lecturers setup complete!\n")

def setup_rooms():
    print("🏢 Setting up rooms...")
    rooms_data = load_json('rooms_sample.json')
    
    for room_data in rooms_data:
        existing = Room.query.filter_by(id=room_data['id']).first()
        if not existing:
            room = Room(id=room_data['id'], capacity=room_data['capacity'])
            db.session.add(room)
            print(f"  ✓ Added {room_data['id']} (capacity: {room_data['capacity']})")
    
    db.session.commit()
    print("✅ Rooms setup complete!\n")

def setup_timeslots():
    print("⏰ Setting up timeslots...")
    timeslots_data = load_json('timeslots_sample.json')
    
    for ts_data in timeslots_data:
        existing = Timeslot.query.filter_by(id=ts_data['id']).first()
        if not existing:
            timeslot = Timeslot(
                id=ts_data['id'],
                day=ts_data['day'],
                time=ts_data['time']
            )
            db.session.add(timeslot)
            print(f"  ✓ Added {ts_data['id']} ({ts_data['day']} {ts_data['time']})")
    
    db.session.commit()
    print("✅ Timeslots setup complete!\n")

def setup_exam_periods():
    print("📝 Setting up exam periods...")
    exam_periods_data = load_json('exam_periods_sample.json')
    
    for ep_data in exam_periods_data:
        existing = ExamPeriod.query.filter_by(id=ep_data['id']).first()
        if not existing:
            exam_period = ExamPeriod(
                id=ep_data['id'],
                day=ep_data['day'],
                time=ep_data['time'],
                duration=ep_data['duration']
            )
            db.session.add(exam_period)
            print(f"  ✓ Added {ep_data['id']} ({ep_data['day']} {ep_data['time']}, {ep_data['duration']}min)")
    
    db.session.commit()
    print("✅ Exam periods setup complete!\n")

def setup_exams():
    print("🎓 Setting up exams...")
    exams_data = load_json('exams_sample.json')
    
    for exam_data in exams_data:
        existing = Exam.query.filter_by(id=exam_data['id']).first()
        if not existing:
            course = Course.query.filter_by(name=exam_data['course']).first()
            if course:
                exam = Exam(
                    course_id=course.id,
                    duration=exam_data['duration'],
                    required_room_type=exam_data.get('required_room_type')
                )
                db.session.add(exam)
                print(f"  ✓ Added exam for {exam_data['course']} ({exam_data['duration']}min)")
            else:
                print(f"  ⚠ Skipped {exam_data['course']} - course not found")
    
    db.session.commit()
    print("✅ Exams setup complete!\n")

def main():
    print("=" * 50)
    print("🚀 AI TIMETABLE - Sample Data Setup")
    print("=" * 50 + "\n")
    
    with app.app_context():
        try:
            # Check if data already exists
            lecturer_count = Lecturer.query.count()
            if lecturer_count > 0:
                print("⚠️  Data already exists. Skipping import to avoid duplicates.")
                print(f"   Found {lecturer_count} lecturers in database.")
                print("\n   To reset, delete 'instance/timetable.db' and run again.\n")
                return
            
            setup_lecturers()
            setup_rooms()
            setup_timeslots()
            setup_exam_periods()
            
            # Note: Exams require courses to exist first
            # So we'll show instructions for manual import
            print("=" * 50)
            print("✅ Setup Complete!")
            print("=" * 50 + "\n")
            
            print("📋 Summary:")
            print(f"  - Lecturers: {Lecturer.query.count()}")
            print(f"  - Rooms: {Room.query.count()}")
            print(f"  - Timeslots: {Timeslot.query.count()}")
            print(f"  - Exam Periods: {ExamPeriod.query.count()}")
            print(f"  - Courses: {Course.query.count()}")
            print(f"  - Exams: {Exam.query.count()}\n")
            
            print("📝 Next Steps:")
            print("  1. Start the frontend: cd frontend && npm run dev")
            print("  2. Go to Data Management → Courses")
            print("  3. Upload 'sample_courses.csv' file")
            print("  4. Go to Dashboard and generate timetables!")
            print("  5. For exams, add them in Data Management → Exams tab\n")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    main()
