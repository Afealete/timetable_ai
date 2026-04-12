from flask import Blueprint, request, jsonify
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/", methods=["OPTIONS"])
def options_upload():
    return '', 200

@upload_bp.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    print("FILE SAVED AT:", filepath)

    return jsonify({"path": filepath})