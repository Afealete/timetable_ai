from flask import Blueprint, request, jsonify
from services.parser import parse_file
from services.ga import run_ga
from services.database_service import get_courses_dataframe
import os

generate_bp = Blueprint("generate", __name__)

@generate_bp.route("/generate", methods=["OPTIONS"])
def options_generate():
    return '', 200

@generate_bp.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        print("REQUEST DATA:", data)

        use_database = data.get("use_database", False)
        path = data.get("path")

        if use_database:
            df = get_courses_dataframe()
            print("USING DATABASE DATA")
        else:
            if not path or path.strip() == "":
                return jsonify({"error": "Invalid file path"}), 400

            # Ensure absolute path
            path = os.path.abspath(path)

            print("ABSOLUTE PATH:", path)

            df = parse_file(path)

        print("DATAFRAME HEAD:\n", df.head())
        print("COLUMNS:", df.columns)

        result = run_ga(df)

        print("GA SUCCESS")
        print("RESULT TYPE:", type(result))
        print("RESULT LENGTH:", len(result) if hasattr(result, '__len__') else 'N/A')
        if hasattr(result, '__len__') and len(result) > 0:
            print("FIRST RESULT ITEM:", result[0])
            print("RESULT SAMPLE:", result[:3])  # First 3 items
        else:
            print("RESULT IS EMPTY OR NOT A SEQUENCE")

        # Clean the result to handle NaN values
        import math
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(item) for item in obj]
            elif isinstance(obj, float) and math.isnan(obj):
                return None
            else:
                return obj

        cleaned_result = clean_for_json(result)
        
        response_data = {"timetable": cleaned_result}
        print("FINAL RESPONSE DATA KEYS:", list(response_data.keys()))
        print("TIMETABLE FIELD TYPE:", type(response_data["timetable"]))
        print("TIMETABLE FIELD LENGTH:", len(response_data["timetable"]) if hasattr(response_data["timetable"], '__len__') else 'N/A')
        
        response = jsonify(response_data)
        print("JSONIFY RESPONSE:", response)
        print("JSONIFY RESPONSE DATA:", response.get_data())
        print("JSONIFY RESPONSE HEADERS:", dict(response.headers))
        return response
        
    except Exception as e:
        print("ERROR IN GENERATE:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500