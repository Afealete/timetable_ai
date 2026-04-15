# Sample Data Setup Guide

This guide will help you set up the system with sample data to generate perfect course and exam timetables.

## Files Included

### Course Timetable Files
- **sample_courses.csv** - 16 courses across 8 departments with 2 groups each
- **data/lecturers_sample.json** - 8 lecturers
- **data/rooms_sample.json** - 16 rooms (labs and halls)
- **data/timeslots_sample.json** - 30 timeslots (Mon-Fri, 6 slots per day)

### Exam Timetable Files
- **data/exam_periods_sample.json** - 15 exam periods (3 per day, Mon-Fri)
- **data/exams_sample.json** - 8 exams (one per course)

## Setup Instructions

### Option 1: Database-Driven Setup (Recommended)

1. **Start the backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Import Lecturers** (via Data Management UI)
   - Go to Data Management → Lecturers tab
   - Add each lecturer from `lecturers_sample.json`:
     - Dr. Smith
     - Prof. Johnson
     - Dr. Williams
     - Prof. Brown
     - Mrs. Davis
     - Dr. Anderson
     - Prof. Thomas
     - Dr. Moore

3. **Import Rooms** (via Data Management UI)
   - Go to Data Management → Rooms tab
   - Add all 16 rooms from `rooms_sample.json` with their capacities
   - Lab rooms: Lab1-Lab8 (various capacities)
   - Hall rooms: Hall1-Hall4 (50 capacity each)
   - Classroom rooms: Room101-Room104 (40 capacity each)

4. **Import Timeslots** (via Data Management UI)
   - Go to Data Management → Timeslots tab
   - Add all 30 timeslots from `timeslots_sample.json`
   - Format: T1 (Monday 8-9), T2 (Monday 9-10), etc.

5. **Import Courses** (Upload CSV)
   - Go to Dashboard
   - Upload `sample_courses.csv`
   - Click "Generate Timetable" with type set to "Course Timetable"
   - Wait for optimal solution to be generated

### Option 2: File-Based Setup (Manual)

1. **For Course Timetable:**
   - Use `sample_courses.csv` directly via upload feature
   - Or manually enter courses in Data Management UI

2. **For Exam Timetable:**
   - Add Exam Periods from `exam_periods_sample.json`
   - Add Exams from `exams_sample.json`

## Data Characteristics

### Course Data
```
Total: 16 courses
Groups: 32 sections (2 per course)
Student Range: 26-50 per section
Lecturers: 8 (2 courses each)
Rooms: 16 (varied capacities)
Timeslots: 30 (Mon-Fri, 6 hours/day)
```

### Exam Data
```
Total: 8 exams (one per course)
Duration: 120 minutes each
Exam Periods: 15 slots (3 per day, Mon-Fri)
Room Type: Exam halls required
```

## Expected Results

### Course Timetable
✅ **Perfect Schedule** with:
- No lecturer conflicts
- No room conflicts
- No student group conflicts
- All courses scheduled within 30 timeslots
- ~60% room utilization

**Expected Generation Time:** 5-10 seconds

### Exam Timetable
✅ **Optimal Schedule** with:
- No lecturer supervision conflicts
- No exam hall conflicts
- 8 exams spread across 15 periods
- Balanced daily distribution

**Expected Generation Time:** 3-5 seconds

## Sample Schedule Output

### Course Example
```
Course: CS101 (CS-A)
Lecturer: Dr. Smith
Room: Lab1
Day: Monday
Time: 8:00-9:00
Students: 45
```

### Exam Example
```
Course: CS101
Lecturer: Dr. Smith
Room: Hall1
Day: Monday
Time: 9:00 (120 min)
```

## Customization

### To Add More Data
1. **Courses:** Duplicate entries in CSV and adjust group names
2. **Lecturers:** Add new names in Data Management
3. **Rooms:** Add room IDs and capacities
4. **Timeslots:** Add more days/times (maintain format: "H1-H2")
5. **Exam Periods:** Add more slots with duration

### To Optimize Further
- Balance student counts (within 5% of each other)
- Ensure room capacities exceed student counts
- Distribute courses evenly among lecturers
- Avoid back-to-back classes for same lecturer

## Troubleshooting

### "No suitable room found"
- ✅ Solution: Increase room capacities in `rooms_sample.json`

### "Lecturer conflict"
- ✅ Solution: Ensure enough timeslots (≥ number of courses per lecturer)

### "Low fitness score"
- ✅ Solution: Add more timeslots or reduce courses

## Performance Notes

- **Optimal data ratio:** 1 lecturer : 2 courses : 3 rooms : 4 timeslots
- **Maximum courses:** 50 (with proportional resources)
- **Generation performance:** O(generations × population_size × courses)

---

**Ready to generate!** Start with the Dashboard and select your timetable type. 📅✨
