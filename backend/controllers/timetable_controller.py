from flask import Blueprint, request, jsonify
from services.parser_service import parse_file
from services.ga_engine import run_ga, run_exam_ga, TIMESLOTS
from services.database_service import get_exam_periods_data

timetable_bp = Blueprint("timetable", __name__)

@timetable_bp.route("/generate", methods=["OPTIONS"])
def options_generate():
    return '', 200

@timetable_bp.route("/generate", methods=["POST"])
def generate():
    data = request.json
    timetable_type = data.get("type", "course")  # Default to course timetable

    if timetable_type == "exam":
        return generate_exam_timetable(data)
    else:
        return generate_course_timetable(data)

def generate_course_timetable(data):
    filepath = data.get("path")
    column_map = data.get("columns", {})

    if not filepath:
        return jsonify({"error": "path is required"}), 400

    try:
        df = parse_file(filepath, column_map)
    except (KeyError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"unexpected error: {exc}"}), 500

    result = run_ga(df)

    formatted = []

    for g in result:
        timeslot_idx = g[3]
        if 0 <= timeslot_idx < len(TIMESLOTS):
            timeslot = TIMESLOTS[timeslot_idx]
            day = timeslot['day']
            time_parts = timeslot['time'].split('-')
            period = f"{time_parts[0]}:00-{time_parts[1]}:00"
        else:
            day = "Unknown"
            period = "Unknown"
        
        formatted.append({
            "course": g[0],
            "lecturer": g[1],
            "room": g[2],
            "day": day,
            "period": period,
            "group": g[4],
            "capacity": g[5],
            "students": g[6]
        })

    return jsonify({"timetable": formatted})

def generate_exam_timetable(data):
    filepath = data.get("path")
    column_map = data.get("columns", {})

    if not filepath:
        return jsonify({"error": "path is required"}), 400

    try:
        df = parse_file(filepath, column_map)
    except (KeyError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"unexpected error: {exc}"}), 500

    result = run_exam_ga(df)

    exam_periods = get_exam_periods_data()
    formatted = []

    for g in result:
        exam_period_idx = g[3]
        if 0 <= exam_period_idx < len(exam_periods):
            exam_period = exam_periods[exam_period_idx]
            day = exam_period['day']
            time = exam_period['time']
            duration = exam_period['duration']
        else:
            day = "Unknown"
            time = "Unknown"
            duration = 0
        
        formatted.append({
            "course": g[0],
            "lecturer": g[1],
            "room": g[2],
            "day": day,
            "time": time,
            "duration": duration,
            "group": g[4],
            "students": g[5]
        })

    return jsonify({"timetable": formatted})