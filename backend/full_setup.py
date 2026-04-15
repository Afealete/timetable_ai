#!/usr/bin/env python3
"""
Master Setup Script - Complete sample data import in one go
Run from backend directory: python full_setup.py
"""

import json
import os
import sys
import subprocess
from models import db, Lecturer, Room, Timeslot, ExamPeriod, Exam, Course
from app import app

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
COURSES_FILE = os.path.join(os.path.dirname(__file__), '..', 'sample_courses.csv')

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"  ⚠  {filename} not found")
        return None
    with open(filepath, 'r') as f:
        return json.load(f)

def clear_database():
    """Drop all tables and recreate them"""
    print("\n🔄 Resetting database...")
    db.drop_all()
    db.create_all()
    print("  ✓ Database reset\n")

def import_lecturers():
    """Import lecturer data"""
    print("📚 Importing lecturers...")
    lecturers_data = load_json('lecturers_sample.json')
    
    if not lecturers_data:
        return 0
    
    count = 0
    for lect_data in lecturers_data:
        lecturer = Lecturer(
            name=lect_data['name'],
            unavailable_slots=json.dumps(lect_data.get('unavailable_slots', []))
        )
        db.session.add(lecturer)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} lecturers imported\n")
    return count

def import_rooms():
    """Import room data"""
    print("🏢 Importing rooms...")
    rooms_data = load_json('rooms_sample.json')
    
    if not rooms_data:
        return 0
    
    count = 0
    for room_data in rooms_data:
        room = Room(id=room_data['id'], capacity=room_data['capacity'])
        db.session.add(room)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} rooms imported\n")
    return count

def import_timeslots():
    """Import timeslot data"""
    print("⏰ Importing timeslots...")
    timeslots_data = load_json('timeslots_sample.json')
    
    if not timeslots_data:
        return 0
    
    count = 0
    for ts_data in timeslots_data:
        timeslot = Timeslot(
            id=ts_data['id'],
            day=ts_data['day'],
            time=ts_data['time']
        )
        db.session.add(timeslot)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} timeslots imported\n")
    return count

def import_exam_periods():
    """Import exam period data"""
    print("📝 Importing exam periods...")
    exam_periods_data = load_json('exam_periods_sample.json')
    
    if not exam_periods_data:
        return 0
    
    count = 0
    for ep_data in exam_periods_data:
        exam_period = ExamPeriod(
            id=ep_data['id'],
            day=ep_data['day'],
            time=ep_data['time'],
            duration=ep_data['duration']
        )
        db.session.add(exam_period)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} exam periods imported\n")
    return count

def import_courses_from_csv():
    """Import course data from CSV"""
    print("📚 Importing courses from CSV...")
    
    if not os.path.exists(COURSES_FILE):
        print(f"  ⚠  sample_courses.csv not found\n")
        return 0
    
    import csv
    count = 0
    
    with open(COURSES_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Find lecturer
            lecturer = Lecturer.query.filter_by(name=row['lecturer']).first()
            if not lecturer:
                print(f"  ⚠  Lecturer '{row['lecturer']}' not found, skipping {row['course']}")
                continue
            
            # Find room
            room = Room.query.filter_by(id=row['room']).first()
            
            # Create course
            course = Course(
                name=row['course'],
                lecturer_id=lecturer.id,
                group=row['group'],
                students=int(row['students']),
                capacity=int(row['capacity']),
                room_id=room.id if room else None
            )
            db.session.add(course)
            count += 1
    
    db.session.commit()
    print(f"  ✓ {count} courses imported\n")
    return count

def import_exams():
    """Import exam data"""
    print("🎓 Importing exams...")
    exams_data = load_json('exams_sample.json')
    
    if not exams_data:
        return 0
    
    count = 0
    skipped = 0
    
    for exam_data in exams_data:
        course = Course.query.filter_by(name=exam_data['course']).first()
        if not course:
            skipped += 1
            continue
        
        exam = Exam(
            id=exam_data['id'],
            course_id=course.id,
            duration=exam_data['duration'],
            required_room_type=exam_data.get('required_room_type')
        )
        db.session.add(exam)
        count += 1
    
    db.session.commit()
    print(f"  ✓ {count} exams imported, {skipped} skipped\n")
    return count

def show_summary():
    """Show data summary"""
    print("=" * 50)
    print("✅ SETUP COMPLETE!")
    print("=" * 50 + "\n")
    
    print("📊 Database Summary:")
    print(f"  • Lecturers: {Lecturer.query.count()}")
    print(f"  • Rooms: {Room.query.count()}")
    print(f"  • Timeslots: {Timeslot.query.count()}")
    print(f"  • Courses: {Course.query.count()}")
    print(f"  • Exam Periods: {ExamPeriod.query.count()}")
    print(f"  • Exams: {Exam.query.count()}\n")
    
    print("🎯 Ready to use!")
    print("  1. Start frontend: cd frontend && npm run dev")
    print("  2. Go to Dashboard")
    print("  3. Select timetable type (Course or Exam)")
    print("  4. Click 'Generate Timetable'")
    print("  5. View and export results!\n")

def main():
    print("\n" + "=" * 50)
    print("🚀 FULL SYSTEM SETUP")
    print("=" * 50)
    print("\nThis will import all sample data for course and exam timetables.\n")
    
    # Confirm if resetting
    response = input("Reset database first? (y/n) [y]: ").strip().lower()
    should_reset = response != 'n'
    
    with app.app_context():
        try:
            if should_reset:
                clear_database()
            
            # Import all data
            import_lecturers()
            import_rooms()
            import_timeslots()
            import_exam_periods()
            import_courses_from_csv()
            import_exams()
            
            # Show results
            show_summary()
            
        except Exception as e:
            print(f"\n❌ Error during setup: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
