from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from routes.upload import upload_bp
from routes.generate import generate_bp
from routes.export import export_bp
from routes.data import data_bp
from models import db

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Database configuration

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(generate_bp, url_prefix="/timetable")
app.register_blueprint(export_bp, url_prefix="/export")
app.register_blueprint(data_bp, url_prefix="/data")

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    allowed_origins = {
        'http://localhost:5173',
        'http://localhost:5174',
        'http://localhost:5175',
        'http://localhost:5176',
    }

    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'

    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

if __name__ == "__main__":
    app.run(debug=True)