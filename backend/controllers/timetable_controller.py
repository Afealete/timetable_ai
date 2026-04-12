from flask import Blueprint, request, jsonify
from services.parser_service import parse_file
from services.ga_engine import run_ga, TIMESLOTS

timetable_bp = Blueprint("timetable", __name__)

@timetable_bp.route("/generate", methods=["OPTIONS"])
def options_generate():
    return '', 200

@timetable_bp.route("/generate", methods=["POST"])
def generate():
    data = request.json

    filepath = data.get("path")
    column_map = data.get("columns", {})  # Default to empty dict if not provided

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