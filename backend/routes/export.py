from flask import Blueprint, request, send_file
import pandas as pd
import os
import re

export_bp = Blueprint("export", __name__)

def parse_period(period: str):
    if not period or not isinstance(period, str):
        return None

    normalized = period.strip()
    parts = normalized.split("-")
    if len(parts) != 2:
        return None

    def parse_time(value: str):
        cleaned = re.sub(r"\s+", "", value).replace(":00", "")
        parts = cleaned.split(":")
        try:
            if len(parts) == 1:
                hour = int(parts[0])
                minute = 0
            else:
                hour = int(parts[0])
                minute = int(parts[1])
        except ValueError:
            return None
        return hour * 60 + minute

    start = parse_time(parts[0].strip())
    end = parse_time(parts[1].strip())
    if start is None or end is None:
        return None
    return {"start": start, "end": end}


def normalize_period(period: str):
    parsed = parse_period(period)
    if not parsed:
        return period.strip() if period else ""
    return f"{parsed['start'] // 60:02d}:{parsed['start'] % 60:02d}-{parsed['end'] // 60:02d}:{parsed['end'] % 60:02d}"


def get_display_periods(data, is_exam_timetable: bool):
    unique_periods = set()
    for item in data:
        period = item.get("period")
        if period:
            unique_periods.add(normalize_period(period))

    parsed_periods = []
    for period in unique_periods:
        parsed = parse_period(period)
        if parsed:
            parsed_periods.append({"period": period, "parsed": parsed})

    parsed_periods.sort(key=lambda item: item["parsed"]["start"])
    sorted_periods = [item["period"] for item in parsed_periods]

    if is_exam_timetable:
        return sorted_periods

    display_periods = []
    for idx, current in enumerate(sorted_periods):
        display_periods.append(current)
        next_parsed = parse_period(sorted_periods[idx + 1]) if idx + 1 < len(sorted_periods) else None
        current_parsed = parse_period(current)
        if current_parsed and next_parsed and next_parsed["start"] > current_parsed["end"]:
            display_periods.append(f"{current_parsed['end'] // 60:02d}:{current_parsed['end'] % 60:02d}-{next_parsed['start'] // 60:02d}:{next_parsed['start'] % 60:02d}")

    return display_periods


def format_class_entry(item: dict):
    parts = [
        item.get("course") or "N/A",
        item.get("lecturer") or "No lecturer",
        item.get("room") or "No room"
    ]

    if item.get("group"):
        parts.append(f"Group: {item.get('group')}")
    if item.get("students") is not None and item.get("students") != "":
        parts.append(f"Students: {item.get('students')}")
    if item.get("capacity") is not None and item.get("capacity") != "":
        parts.append(f"Capacity: {item.get('capacity')}")

    return "\n".join(parts)


def is_break_row(period: str, data):
    normalized = normalize_period(period)
    for item in data:
        if normalize_period(item.get("period", "")) == normalized:
            return False
    return True


@export_bp.route("", methods=["OPTIONS"])
@export_bp.route("/", methods=["OPTIONS"])
def options_export():
    return '', 200


@export_bp.route("", methods=["POST"])
@export_bp.route("/", methods=["POST"])
def export():
    data = request.json.get("timetable", [])
    filename = request.json.get("filename", "timetable.xlsx")
    format_type = request.json.get("format", "xlsx")
    timetable_type = request.json.get("timetable_type", "course")

    if not isinstance(data, list) or len(data) == 0:
        return {"error": "No timetable data provided"}, 400

    if format_type not in ["xlsx", "csv"]:
        format_type = "xlsx"

    if format_type == "csv" and not filename.endswith(".csv"):
        filename = filename.replace(".xlsx", "") + ".csv"
    elif format_type == "xlsx" and not filename.endswith(".xlsx"):
        filename = filename.replace(".csv", "") + ".xlsx"

    os.makedirs("exports", exist_ok=True)
    filepath = os.path.join("exports", filename)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    is_exam_timetable = timetable_type == "exam"
    periods = get_display_periods(data, is_exam_timetable)

    grid_data = []
    for period in periods:
        row = {"Time": period}
        for day in days:
            classes = [
                item for item in data
                if item.get("day") == day and normalize_period(item.get("period", "")) == normalize_period(period)
            ]
            if classes:
                row[day] = "\n\n".join(format_class_entry(item) for item in classes)
            elif not is_exam_timetable and is_break_row(period, data):
                row[day] = "Break"
            else:
                row[day] = ""
        grid_data.append(row)

    df = pd.DataFrame(grid_data)

    if format_type == "csv":
        df.to_csv(filepath, index=False)
    else:
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Timetable')
            workbook = writer.book
            worksheet = writer.sheets['Timetable']
            workbook.active = workbook.sheetnames.index('Timetable')
            worksheet.sheet_view.tabSelected = True

            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        cell.alignment = cell.alignment.copy(wrap_text=True)
                        value = str(cell.value) if cell.value is not None else ""
                        for line in value.split('\n'):
                            if len(line) > max_length:
                                max_length = len(line)
                    except Exception:
                        pass
                worksheet.column_dimensions[column_letter].width = min(max(max_length + 2, 12), 50)

            for row_idx, row in enumerate(worksheet.iter_rows(), 1):
                max_lines = 1
                for cell in row:
                    if cell.value:
                        lines = str(cell.value).split('\n')
                        if len(lines) > max_lines:
                            max_lines = len(lines)
                worksheet.row_dimensions[row_idx].height = max(20, max_lines * 15)

    return send_file(filepath, as_attachment=True)
