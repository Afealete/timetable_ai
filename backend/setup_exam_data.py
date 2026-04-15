#!/usr/bin/env python3
"""
Setup Exam Data Script - Import exam periods and exams
Run after courses are created: python setup_exam_data.py
"""

import json
import os
import sys
from models import db, ExamPeriod, Exam, Course
from app import app

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"❌ Error: {filename} not found in data directory")
        return None
    with open(filepath, 'r') as f:
        return json.load(f)

def setup_exam_periods():
    """Import exam time periods"""
    print("\n📝 Setting up exam periods...")
    exam_periods_data = load_json('exam_periods_sample.json')
    
    if not exam_periods_data:
        return False
    
    added = 0
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
            print(f"  ✓ {ep_data['id']}: {ep_data['day']} {ep_data['time']} ({ep_data['duration']}min)")
            added += 1
        else:
            print(f"  ⊜ {ep_data['id']} already exists")
    
    db.session.commit()
    print(f"✅ Exam periods: {added} added\n")
    return True

def setup_exams():
    """Import exams linked to courses"""
    print("🎓 Setting up exams...")
    exams_data = load_json('exams_sample.json')
    
    if not exams_data:
        return False
    
    added = 0
    skipped = 0
    
    for exam_data in exams_data:
        existing = Exam.query.filter_by(id=exam_data['id']).first()
        if not existing:
            # Find course by name
            course = Course.query.filter_by(name=exam_data['course']).first()
            if course:
                exam = Exam(
                    id=exam_data['id'],
                    course_id=course.id,
                    duration=exam_data['duration'],
                    required_room_type=exam_data.get('required_room_type')
                )
                db.session.add(exam)
                print(f"  ✓ {exam_data['course']}: {exam_data['duration']}min, {exam_data.get('required_room_type', 'any')} room")
                added += 1
            else:
                print(f"  ✗ {exam_data['course']}: Course not found (create it first)")
                skipped += 1
        else:
            print(f"  ⊜ Exam {exam_data['id']} already exists")
    
    db.session.commit()
    print(f"✅ Exams: {added} added, {skipped} skipped\n")
    return added > 0

def main():
    print("=" * 50)
    print("🎓 EXAM DATA SETUP")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check if courses exist
            course_count = Course.query.count()
            if course_count == 0:
                print("\n❌ Error: No courses found in database!")
                print("   Please import courses first:")
                print("   1. Upload sample_courses.csv via Dashboard")
                print("   2. Or add courses manually in Data Management\n")
                sys.exit(1)
            
            print(f"\n✓ Found {course_count} courses in database\n")
            
            # Setup exam periods
            if not setup_exam_periods():
                sys.exit(1)
            
            # Setup exams
            if not setup_exams():
                print("\n⚠️  No exams were added. Check if courses exist.")
            
            # Show summary
            print("=" * 50)
            print("✅ EXAM SETUP COMPLETE!")
            print("=" * 50 + "\n")
            
            exam_period_count = ExamPeriod.query.count()
            exam_count = Exam.query.count()
            
            print(f"📊 Summary:")
            print(f"  - Courses: {course_count}")
            print(f"  - Exam Periods: {exam_period_count}")
            print(f"  - Exams: {exam_count}\n")
            
            print("🚀 Next Steps:")
            print("  1. Go to Dashboard")
            print("  2. Select 'Exam Timetable' as the type")
            print("  3. Click 'Generate Timetable'")
            print("  4. View your optimized exam schedule!\n")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()
