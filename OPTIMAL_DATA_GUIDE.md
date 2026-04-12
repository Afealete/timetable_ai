# Optimal Data Format for Best Timetable Generation

## 📊 REQUIRED COLUMNS (CSV Format)

Your CSV file should contain these **essential columns** for optimal GA performance:

### Core Scheduling Columns:
- **course** (or subject, module) - Course name/code
- **lecturer** (or teacher, instructor) - Lecturer name
- **group** (or class, level) - Student group/class identifier
- **students** (or enrollment) - Number of students enrolled
- **capacity** (or size) - Maximum room capacity needed

### Optional but Recommended:
- **room** (or hall, venue) - Preferred room (GA will optimize if missing)

## 🎯 OPTIMAL DATA CHARACTERISTICS

### 1. **Complete Information**
```csv
course,lecturer,group,students,capacity,room
CS101,Dr. Smith,CS200,45,50,Lab1
MATH201,Prof. Johnson,MATH300,30,40,HallA
PHYS101,Dr. Brown,PHYS100,60,80,Lab2
```

### 2. **Realistic Capacity Matching**
- **students** ≤ **capacity** (prevents impossible assignments)
- Include room capacity data for better optimization

### 3. **Balanced Workload**
- Distribute courses evenly across lecturers
- Avoid single lecturer with 80% of courses
- Balance group sizes

### 4. **Diverse Constraints**
- Multiple lecturers (3-10 for medium institution)
- Multiple rooms with different capacities
- Multiple student groups
- Various course sizes (small seminars to large lectures)

## 📈 DATA QUALITY IMPACT

### ✅ GOOD DATA = PERFECT TIMETABLES
- **Fitness Score: 0** (zero constraint violations)
- **100% feasible** schedules
- **Optimal resource utilization**

### ❌ POOR DATA = CONSTRAINT VIOLATIONS
- Missing capacity data → Room overcrowding
- Single lecturer bottleneck → Scheduling conflicts
- Inconsistent naming → Parsing errors

## 🔧 COLUMN NAME FLEXIBILITY

The parser auto-detects columns using keywords:

| Required Field | Accepted Column Names |
|----------------|----------------------|
| course | course, subject, module, code |
| lecturer | lecturer, teacher, instructor, prof |
| group | group, class, level, batch |
| students | students, enrollment, size |
| capacity | capacity, room_size, max_students |
| room | room, hall, venue, location |

## 📋 SAMPLE OPTIMAL DATASET

```csv
course,lecturer,group,students,capacity,room
CS101,Dr. Smith,CS200,45,50,ComputerLab1
CS102,Dr. Smith,CS200,42,50,ComputerLab2
MATH201,Prof. Johnson,MATH300,30,40,LectureHallA
MATH202,Prof. Johnson,MATH300,35,40,LectureHallB
PHYS101,Dr. Brown,PHYS100,60,80,PhysicsLab1
PHYS102,Dr. Brown,PHYS100,55,80,PhysicsLab2
CHEM101,Dr. Davis,CHEM100,25,30,ChemistryLab1
CHEM102,Dr. Davis,CHEM100,28,30,ChemistryLab2
BIO101,Prof. Wilson,BIO100,40,50,BiologyLab1
BIO102,Prof. Wilson,BIO100,38,50,BiologyLab2
```

## 🎯 BEST PRACTICES

### 1. **Data Validation**
- Ensure no empty cells in required columns
- Verify students ≤ capacity for all rows
- Check lecturer names are consistent

### 2. **Size Optimization**
- **Small datasets (20-50 courses)**: Fast convergence, perfect solutions
- **Medium datasets (100-500 courses)**: Good performance, may need more generations
- **Large datasets (1000+ courses)**: May need parameter tuning

### 3. **Constraint Diversity**
- **Lecturer variety**: 5-15 lecturers for 100 courses
- **Room variety**: Different capacity rooms (20-200 seats)
- **Time preferences**: Include lecturer availability if possible

### 4. **File Format**
- **CSV preferred** (most reliable parsing)
- **UTF-8 encoding** for special characters
- **No special characters** in column headers
- **Clean data** (no merged cells, formulas)

## 🚀 EXPECTED RESULTS

With optimal data format:
- **GA Convergence**: Fast (100-300 generations)
- **Fitness Score**: 0 (perfect solution)
- **Constraint Satisfaction**: 100%
- **Timetable Quality**: Optimal resource utilization

## ⚠️ COMMON ISSUES TO AVOID

1. **Missing capacity data** → Random room assignments
2. **Single lecturer bottleneck** → Impossible schedules
3. **Inconsistent naming** → Parsing failures
4. **Over-constrained problems** → No feasible solutions
5. **Too many small groups** → Fragmented schedules

## 📊 PERFORMANCE METRICS

| Data Quality | GA Performance | Result Quality |
|-------------|----------------|----------------|
| ⭐⭐⭐⭐⭐ Excellent | Fast convergence | Perfect timetable |
| ⭐⭐⭐⭐ Good | Good convergence | High-quality timetable |
| ⭐⭐⭐ Average | Slow convergence | Acceptable timetable |
| ⭐⭐ Poor | May not converge | Many violations |
| ⭐ Very Poor | Fails to find solution | Infeasible |

**Recommendation**: Aim for ⭐⭐⭐⭐⭐ quality data for production use!</content>
<parameter name="filePath">c:\Users\EMMANUEL\projects\timetable_ai\OPTIMAL_DATA_GUIDE.md