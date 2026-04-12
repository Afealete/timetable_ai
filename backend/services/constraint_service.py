import json
import os

# Load reference data for constraints
data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
with open(os.path.join(data_dir, 'lecturers.json'), 'r') as f:
    LECTURERS = json.load(f)
with open(os.path.join(data_dir, 'timeslots.json'), 'r') as f:
    TIMESLOTS = json.load(f)


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

        lecturer_time[(lecturer, timeslot)] = True
        if room is not None:
            room_time[(room, timeslot)] = True
        group_time[(group, timeslot)] = True

    return penalty