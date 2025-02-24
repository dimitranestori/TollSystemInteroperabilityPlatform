from flask import Flask, Blueprint, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import csv
import os
from datetime import datetime
from flask import request


app = Flask(__name__)

admin = Blueprint('admin', __name__)

# Database configuration
app.config['MYSQL_HOST'] = '<host>'
app.config['MYSQL_USER'] = '<user>'
app.config['MYSQL_PASSWORD'] = '<password>'
app.config['MYSQL_DB'] = '<database>'
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mysql = MySQL(app)

# Healthcheck: Verifies database connection and returns system status
@admin.route('/healthcheck', methods=['GET'])
def health_check():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT COUNT(*) AS count FROM Toll')
        stations_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) AS count FROM Charges')
        passes_count = cursor.fetchone()[0]
        cursor.close()

        return jsonify({
            'status': 'OK',
            'dbconnection': f"MySQL on {app.config['MYSQL_HOST']}",
            'n_stations': stations_count,
            'n_passes': passes_count
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'dbconnection': f"MySQL on {app.config['MYSQL_HOST']}",
            'error': str(e)
        }), 500
# Reset stations: Clears toll station data and repopulates from CSV
@admin.route('/resetstations', methods=['POST'])
def reset_stations():
    try:
        csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'tollstations2024.csv')
        if not os.path.exists(csv_file_path):
            return jsonify({'status': 'failed', 'info': 'CSV file not found'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Operator')
        cursor.execute('DELETE FROM Toll')

        # Insert predefined operators
        operators = [
            ('AM', 'aegeanmotorway'),
            ('EG', 'egnatia'),
            ('GE', 'gefyra'),
            ('KO', 'kentrikiodos'),
            ('MO', 'moreas'),
            ('NAO', 'naodos'),
            ('NO', 'neaodos'),
            ('OO', 'olympiaodos')
        ]
        cursor.executemany('INSERT INTO Operator (op_ID, operator) VALUES (%s, %s)', operators)

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
    
            for row in reader:
                row = {key.strip(): value for key, value in row.items()}  # Strip whitespace
                cursor.execute(
                    'INSERT INTO Toll (toll_ID, operator_id, name, locality, PM, road, price1, price2, price3, price4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (row['TollID'], row['\ufeffOpID'], row['Name'], row['Locality'], row['PM'], row['Road'], float(row['Price1']), float(row['Price2']), float(row['Price3']), float(row['Price4']))
                )
        mysql.connection.commit()
        cursor.close()

        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500


# Reset passes: Clears pass-related data and resets admin account
@admin.route('/resetpasses', methods=['POST'])
def reset_passes():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Tags')
        cursor.execute('DELETE FROM Charges')
       
        mysql.connection.commit()
        cursor.close()

        return jsonify({'status': 'OK'}), 200
    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500

# Add passes: Upload new passes from CSV
# Add passes: Upload new passes from CSV
@admin.route('/addpasses', methods=['POST'])
def add_passes():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'failed', 'info': 'CSV file is required'}), 400

        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        cursor = mysql.connection.cursor()

        # Read CSV data into memory first
        with open(filepath, newline='', encoding='utf-8-sig') as csvfile:  # Handle BOM
            reader = csv.DictReader(csvfile)
            data = list(reader)  # Read the entire CSV into a list

        tags_inserted = set()  # Track already inserted tags to avoid duplicates

        # First, populate the Tags table
        for row in data:
            tag_ref = row.get('tagRef')
            tag_home_id = row.get('tagHomeID')

            if not tag_ref or not tag_home_id:
                continue  # Skip rows with missing values

            if tag_ref not in tags_inserted:
                cursor.execute(
                    'INSERT IGNORE INTO Tags (tagRef, tagHomeID) VALUES (%s, %s)',
                    (tag_ref, tag_home_id)
                )
                tags_inserted.add(tag_ref)

        # Populate the Charges table
        for row in data:
            try:
                charge_amount = float(row.get('charge', 0))  # Default to 0 if missing
                timestamp_key = next((k for k in row.keys() if 'timestamp' in k.lower()), None)  # Find correct timestamp key
                charge_date = datetime.strptime(row[timestamp_key], '%Y-%m-%d %H:%M')

                toll_id = row.get('tollID')
                tag_ref = row.get('tagRef')
                tag_home_id = row.get('tagHomeID')

                if not (toll_id and tag_ref and tag_home_id):
                    continue  # Skip if any required field is missing

                # Ensure Toll ID exists
                cursor.execute("SELECT COUNT(*) FROM Toll WHERE toll_ID = %s", (toll_id,))
                if cursor.fetchone()[0] == 0:
                    return jsonify({'status': 'failed', 'info': f"Toll ID {toll_id} not found"}), 400

                # Ensure Operator ID exists
                cursor.execute("SELECT COUNT(*) FROM Operator WHERE op_ID = %s", (tag_home_id,))
                if cursor.fetchone()[0] == 0:
                    return jsonify({'status': 'failed', 'info': f"Operator ID {tag_home_id} not found"}), 400

                # Insert into Charges table
                cursor.execute(
                    'INSERT INTO Charges (amount, date, toll_ID, tagRef, op_ID) VALUES (%s, %s, %s, %s, %s)',
                    (charge_amount, charge_date, toll_id, tag_ref, tag_home_id)
                )

            except Exception as e:
                return jsonify({'status': 'failed', 'info': f"Error processing row: {row}, {str(e)}"}), 500

        # Commit changes and close the cursor
        mysql.connection.commit()
        cursor.close()

        return jsonify({'status': 'OK'}), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

