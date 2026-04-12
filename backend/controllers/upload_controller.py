from flask import Blueprint, request, jsonify
import os

upload_bp = Blueprint("upload", __name__)
UPLOAD_FOLDER = "uploads"

@upload_bp.route("/", methods=["OPTIONS"])
def options_upload():
    return '', 200

@upload_bp.route("/", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    file.save(filepath)

    return jsonify({"path": filepath})