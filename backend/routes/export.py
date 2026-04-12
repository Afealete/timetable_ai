from flask import Blueprint, request, send_file
import pandas as pd
import os

export_bp = Blueprint("export", __name__)

@export_bp.route("/", methods=["OPTIONS"])
def options_export():
    return '', 200

@export_bp.route("/", methods=["POST"])
def export():
    data = request.json["timetable"]

    df = pd.DataFrame(data, columns=[
        "Course", "Lecturer", "Room", "Timeslot", "Group", "Capacity", "Students"
    ])

    filepath = "exports/timetable.xlsx"
    os.makedirs("exports", exist_ok=True)

    df.to_excel(filepath, index=False)

    return send_file(filepath, as_attachment=True)