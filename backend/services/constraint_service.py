import json
import os

# Load reference data for constraints
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'lecturers.json'), 'r') as f:
    LECTURERS = json.load(f)
with open(os.path.join(data_dir, 'timeslots.json'), 'r') as f:
    TIMESLOTS = json.load(f)

# For exams, we'll need exam periods data
exam_periods_path = os.path.join(data_dir, 'exam_periods.json')
if os.path.exists(exam_periods_path):
    with open(exam_periods_path, 'r') as f:
        EXAM_PERIODS = json.load(f)
else:
    EXAM_PERIODS = []


def check_hard_constraints(individual):
    penalty = 0

    lecturer_time = {}
    room_time = {}
    group_time = {}

    # Create lecturer availability map
    lecturer_availability = {}
    for lect in LECTURERS:
        lecturer_availability[lect['name']] = set(lect.get('unavailable_slots', []))

    for gene in individual:
        course, lecturer, room, timeslot, group, capacity, students = gene

        timeslot_id = TIMESLOTS[timeslot]['id'] if 0 <= timeslot < len(TIMESLOTS) else None

        # Lecturer clash
        if (lecturer, timeslot) in lecturer_time:
            penalty += 100

        # Lecturer unavailable
        if lecturer in lecturer_availability and timeslot_id in lecturer_availability[lecturer]:
            penalty += 100

        # Room clash (only if room is assigned)
        if room is not None and (room, timeslot) in room_time:
            penalty += 100

        # Student clash
        if (group, timeslot) in group_time:
            penalty += 100

        # Capacity violation (only if room is assigned)
        if room is not None and students > capacity:
            penalty += 100

        # Penalty for unassigned room
        if room is None:
            penalty += 50

        group_time[(group, timeslot)] = True

    return penalty

def check_exam_hard_constraints(individual):
    penalty = 0

    lecturer_time = {}
    room_time = {}
    student_time = {}  # Track student schedules across exams

    # Create lecturer availability map
    lecturer_availability = {}
    for lect in LECTURERS:
        lecturer_availability[lect['name']] = set(lect.get('unavailable_slots', []))

    for gene in individual:
        course, lecturer, room, exam_period, group, students = gene

        exam_period_id = EXAM_PERIODS[exam_period]['id'] if 0 <= exam_period < len(EXAM_PERIODS) else None

        # Lecturer clash
        if (lecturer, exam_period) in lecturer_time:
            penalty += 100

        # Lecturer unavailable (assuming exam periods map to timeslot IDs)
        if lecturer in lecturer_availability and exam_period_id in lecturer_availability[lecturer]:
            penalty += 100

        # Room clash (only if room is assigned)
        if room is not None and (room, exam_period) in room_time:
            penalty += 100

        # Student clash - check if any student group has overlapping exams
        # This is simplified; in reality, we'd need student enrollment data
        if (group, exam_period) in student_time:
            penalty += 100

        # Capacity violation (only if room is assigned)
        # For exams, we might have different capacity requirements
        if room is not None and students > 50:  # Assume exam room capacity
            penalty += 100

        # Penalty for unassigned room
        if room is None:
            penalty += 50

        lecturer_time[(lecturer, exam_period)] = True
        if room is not None:
            room_time[(room, exam_period)] = True
        student_time[(group, exam_period)] = True

    return penalty