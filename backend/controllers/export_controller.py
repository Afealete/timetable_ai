from flask import Blueprint, request, send_file
import pandas as pd
import os

export_bp = Blueprint("export", __name__)

@export_bp.route("/", methods=["OPTIONS"])
def options_export():
    return '', 200

def parsePeriod(period: str):
    """Parse period string like '09:00-10:00' into start/end minutes"""
    if not period or not isinstance(period, str):
        return None
    
    normalized = period.strip()
    parts = normalized.split("-")
    if len(parts) != 2:
        return None

    def parseTime(time_str: str):
        import re
        cleaned = re.sub(r'\s+', '', time_str).replace(':00', '')
        time_parts = cleaned.split(":")
        try:
            if len(time_parts) == 1:
                hour = int(time_parts[0])
                minute = 0
            else:
                hour = int(time_parts[0])
                minute = int(time_parts[1])
        except ValueError:
            return None
        return hour * 60 + minute

    start = parseTime(parts[0].strip())
    end = parseTime(parts[1].strip())
    if start is None or end is None:
        return None
    return {"start": start, "end": end}

def formatMinutes(minutes: int):
    """Format minutes into HH:MM string"""
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"

def normalizePeriod(period: str):
    """Normalize period to standard format"""
    parsed = parsePeriod(period)
    if not parsed:
        return period.strip()
    return f"{formatMinutes(parsed['start'])}-{formatMinutes(parsed['end'])}"

def getDisplayPeriods(data, isExamTimetable):
    """Get periods for display, including breaks for course timetables"""
    uniquePeriods = set()
    for item in data:
        if item.get("period"):
            uniquePeriods.add(normalizePeriod(item["period"]))
    
    sortedPeriods = []
    for period in uniquePeriods:
        parsed = parsePeriod(period)
        if parsed:
            sortedPeriods.append({"period": period, "parsed": parsed})
    
    sortedPeriods.sort(key=lambda x: x["parsed"]["start"])
    sortedPeriods = [item["period"] for item in sortedPeriods]

    # For exam timetables, don't add breaks
    if isExamTimetable:
        return sortedPeriods

    # For course timetables, add breaks between gaps
    displayPeriods = []
    for i, current in enumerate(sortedPeriods):
        displayPeriods.append(current)

        currentParsed = parsePeriod(current)
        nextParsed = parsePeriod(sortedPeriods[i + 1]) if i + 1 < len(sortedPeriods) else None
        if currentParsed and nextParsed and nextParsed["start"] > currentParsed["end"]:
            displayPeriods.append(f"{formatMinutes(currentParsed['end'])}-{formatMinutes(nextParsed['start'])}")
    
    return displayPeriods

def isBreakRow(period: str, data):
    """Check if a period row should be a break"""
    normalized_period = normalizePeriod(period)
    for item in data:
        if normalizePeriod(item.get("period", "")) == normalized_period:
            return False
    return True

@export_bp.route("/", methods=["POST"])
def export():
    try:
        data = request.json.get("timetable", [])
        filename = request.json.get("filename", "timetable.xlsx")
        format_type = request.json.get("format", "xlsx")
        timetable_type = request.json.get("timetable_type", "course")  # Get timetable type
        
        print(f"EXPORT REQUEST: filename={filename}, format={format_type}, type={timetable_type}")
        print(f"DATA RECEIVED - Type: {type(data)}, Length: {len(data) if isinstance(data, list) else 'N/A'}")
        
        if isinstance(data, list) and len(data) > 0:
            print(f"First data item: {data[0]}")
        
        if not data or len(data) == 0:
            return {"error": "No timetable data provided"}, 400
        
        # Ensure exports directory exists
        os.makedirs("exports", exist_ok=True)
        
        # Determine file extension
        if format_type == "csv":
            if not filename.endswith(".csv"):
                filename = filename.replace(".csv", "").replace(".xlsx", "") + ".csv"
        else:
            if not filename.endswith(".xlsx"):
                filename = filename.replace(".xlsx", "").replace(".csv", "") + ".xlsx"
        
        filepath = os.path.join("exports", filename)
        
        # Create grid format like the dashboard
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        isExamTimetable = timetable_type == "exam"
        periods = getDisplayPeriods(data, isExamTimetable)
        
        print(f"Creating grid with {len(periods)} periods and {len(days)} days")
        
        # Calculate statistics
        total_classes = len(data)
        unique_courses = len(set(item.get("course", "") for item in data if item.get("course")))
        unique_lecturers = len(set(item.get("lecturer", "") for item in data if item.get("lecturer")))
        unique_rooms = len(set(item.get("room", "") for item in data if item.get("room")))
        
        # Create the grid data
        grid_data = []
        
        for period in periods:
            row = {"Time": period}
            
            for day in days:
                # Find classes for this day/period
                classes = []
                for item in data:
                    if (item.get("day") == day and 
                        normalizePeriod(item.get("period", "")) == normalizePeriod(period)):
                        classes.append(item)
                
                if classes:
                    # Format comprehensive class information
                    class_texts = []
                    for cls in classes:
                        course = cls.get("course", "N/A")
                        lecturer = cls.get("lecturer", "No lecturer")
                        room = cls.get("room", "No room")
                        group = cls.get("group", "")
                        students = cls.get("students", "")
                        capacity = cls.get("capacity", "")
                        
                        # Build class info with all available details
                        class_info = f"{course}\n{lecturer}\n{room}"
                        if group:
                            class_info += f"\nGroup: {group}"
                        if students:
                            class_info += f"\nStudents: {students}"
                        if capacity:
                            class_info += f"\nCapacity: {capacity}"
                        
                        class_texts.append(class_info)
                    
                    row[day] = "\n\n".join(class_texts)
                elif isBreakRow(period, data):
                    row[day] = "Break"
                else:
                    row[day] = ""
            
            grid_data.append(row)
        
        # Create DataFrame from grid
        df = pd.DataFrame(grid_data)
        
        print(f"Grid DataFrame created - Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Export based on format
        if format_type == "csv":
            # CSV export should include the timetable grid only
            df.to_csv(filepath, index=False)
            print(f"CSV export successful")
        else:
            # Excel export with formatting, visible sheet only for the generated timetable
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Timetable')

                # Set the active sheet to Timetable so Excel opens directly on the generated timetable
                workbook = writer.book
                worksheet = writer.sheets['Timetable']
                workbook.active = workbook.sheetnames.index('Timetable')
                worksheet.sheet_view.tabSelected = True

                # Auto-adjust column widths and enable text wrapping
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            cell.alignment = cell.alignment.copy(wrap_text=True)
                            cell_value = str(cell.value) if cell.value is not None else ""
                            lines = cell_value.split('\n')
                            for line in lines:
                                if len(line) > max_length:
                                    max_length = len(line)
                        except:
                            pass
                    adjusted_width = min(max(max_length + 2, 12), 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
                for row_idx, row in enumerate(worksheet.iter_rows(), 1):
                    max_lines = 1
                    for cell in row:
                        if cell.value:
                            lines = str(cell.value).split('\n')
                            if len(lines) > max_lines:
                                max_lines = len(lines)
                    row_height = max(20, max_lines * 15)
                    worksheet.row_dimensions[row_idx].height = row_height

                print(f"Excel export successful on the generated timetable sheet")
        
        print(f"File ready to send: {filepath}")
        return send_file(filepath, as_attachment=True)
    
    except Exception as err:
        print(f"Export error: {str(err)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Export failed: {str(err)}"}, 500