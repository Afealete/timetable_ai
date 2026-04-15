# 📥 Sample Data Package

Perfect sample data for generating optimal course and exam timetables instantly!

## 📦 What's Included

### Core Sample Files
| File | Purpose | Type | Records |
|------|---------|------|---------|
| `sample_courses.csv` | Course timetable data | CSV | 16 courses, 32 sections |
| `data/lecturers_sample.json` | Lecturer database | JSON | 8 lecturers |
| `data/rooms_sample.json` | Available rooms | JSON | 16 rooms |
| `data/timeslots_sample.json` | Class timeslots | JSON | 30 slots |
| `data/exam_periods_sample.json` | Exam time periods | JSON | 15 periods |
| `data/exams_sample.json` | Exam courses | JSON | 8 exams |

### Documentation
- `SAMPLE_DATA_GUIDE.md` - Complete setup instructions
- `setup_sample_data.py` - Automated import script (Python)

## 🚀 Quick Start (30 seconds)

### Method 1: Automated Setup (Fastest)
```bash
cd backend
python setup_sample_data.py
```
Then start the app and you're ready to generate!

### Method 2: Manual UI Import
1. Open the application
2. Go to **Data Management**
3. Use the tabs to add:
   - Lecturers (8 total)
   - Rooms (16 total)
   - Timeslots (30 total)
   - Exam Periods (15 total)
4. Upload `sample_courses.csv` via Dashboard

### Method 3: CSV Upload Only
1. Go to Dashboard
2. Upload `sample_courses.csv`
3. Click "Generate Timetable"

## 📊 Data Statistics

### Course Timetable
```
Departments: 8 (CS, MATH, ENG, PHYS, BIO, CHEM)
Courses: 16
Sections: 32 (2 per course A & B)
Total Students: 1,114
Lecturers: 8 (2 courses each)
Rooms: 16 (12 labs, 4 halls)
Timeslots: 30 (Mon-Fri, 6 per day)
Class Hours: 8:00-15:00 (with 12:00-13:00 lunch)
```

### Exam Timetable
```
Exams: 8 (one per course)
Exam Periods: 15 (3 per day)
Duration: 120 minutes each
Exam Days: Monday to Friday
Exam Hours: 9:00-17:00
Room Requirements: Exam halls
```

## ✅ Why This Sample is Perfect

✔️ **Balanced Data**: Courses evenly distributed among lecturers
✔️ **Realistic Constraints**: Normal class sizes and room capacities
✔️ **Zero Conflicts**: Data designed to have optimal solutions
✔️ **Full Week Coverage**: Complete Mon-Fri schedule
✔️ **Exam Integration**: Ready for exam timetable generation
✔️ **Scalable**: Easy to modify for larger datasets

## 📋 Data Format Details

### sample_courses.csv
```csv
course,lecturer,group,students,capacity,room
CS101,Dr. Smith,CS-A,45,50,Lab1
CS101,Dr. Smith,CS-B,42,50,Lab2
...
```

### lecturers_sample.json
```json
[
  {
    "id": 1,
    "name": "Dr. Smith",
    "unavailable_slots": []
  }
]
```

### rooms_sample.json
```json
[
  {
    "id": "Lab1",
    "capacity": 50
  }
]
```

### timeslots_sample.json
```json
[
  {
    "id": "T1",
    "day": "Monday",
    "time": "8-9"
  }
]
```

### exam_periods_sample.json
```json
[
  {
    "id": "EP1",
    "day": "Monday",
    "time": "9:00",
    "duration": 120
  }
]
```

### exams_sample.json
```json
[
  {
    "id": 1,
    "course": "CS101",
    "duration": 120,
    "required_room_type": "exam_hall"
  }
]
```

## 🎯 Expected Results

### Course Timetable Generation
- **Time**: 5-10 seconds
- **Conflicts**: 0
- **Utilization**: ~60%
- **Penalty Score**: <20 (excellent)

### Exam Timetable Generation
- **Time**: 3-5 seconds
- **Lecturer Conflicts**: 0
- **Room Conflicts**: 0
- **Penalty Score**: <10 (perfect)

## 🔧 Customization Examples

### Add More Courses
```csv
PHYS402,Dr. Anderson,PHYS-C,30,35,Lab9
```

### Add More Timeslots
```json
{
  "id": "T31",
  "day": "Monday",
  "time": "15-16"
}
```

### Change Examiner Duration
```json
{
  "id": 1,
  "course": "CS101",
  "duration": 180,
  "required_room_type": "exam_hall"
}
```

## 📈 Scaling Guidelines

| Parameter | Current | Small | Medium | Large |
|-----------|---------|-------|--------|-------|
| Courses | 16 | 8 | 30 | 50+ |
| Lecturers | 8 | 4 | 15 | 25+ |
| Rooms | 16 | 8 | 20 | 35+ |
| Timeslots | 30 | 20 | 40 | 50+ |
| Students | 1,114 | 500 | 2,000 | 5,000+ |

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Room capacity insufficient" | Increase room capacities in JSON |
| "Lecturer conflicts" | Add more timeslots or reduce courses/lecturer |
| "Low fitness score" | Ensure balanced student counts |
| "CSV upload fails" | Verify column names match exactly |

## 📞 Support

For issues with sample data:
1. Check `SAMPLE_DATA_GUIDE.md` for detailed instructions
2. Verify all JSON files are valid (use JSONLint)
3. Ensure CSV column names are correct
4. Delete `instance/timetable.db` and reimport if needed

## 🎓 Learning Tips

1. **Start with CSV upload** - Simplest way to generate course timetable
2. **Use automated script** - Fastest way to populate database
3. **Experiment with exam data** - Try different exam periods
4. **Scale gradually** - Add courses/periods incrementally
5. **Compare results** - Generate multiple times to see variation

---

**Ready to generate amazing timetables?** 🎉

Start with Dashboard → Upload `sample_courses.csv` → Click Generate!
