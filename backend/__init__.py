from flask import Flask, request
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configuration of database
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'softeng')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '402b7ce7d6c664dcc73b3ee2846ef2e28845d62162a4e38dc28bd8637424d688')
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY', 'a061704d56a7310493da4e8472afc0c0b6b2dd007c360ff74f9d3f804335e61c')

# Initialize database connection object
db = MySQL(app)

# Import and register blueprints or routes here
from backend.controllers.admin_controllers import admin
from backend.controllers.analysis_controllers import analysis

app.register_blueprint(admin, url_prefix='/api/admin')
app.register_blueprint(analysis, url_prefix='/api')

CORS(app)
@app.before_request
def before_request():
    if request.method == "OPTIONS":
        # Επιστρέφει τα κατάλληλα CORS headers για OPTIONS request
        return '', 200  # Στέλνει 200 OK χωρίς περιεχόμενο, για να απαντήσει στο OPTIONS request.



