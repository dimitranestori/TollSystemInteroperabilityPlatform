from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from backend import db, app
from backend.controllers import analysis

# Helper to get current timestamp
def get_current_timestamp():
    return datetime.now().isoformat()

# 1. Toll Station Passes
@analysis.route('/tollStationPasses/<tollStationID>/<date_from>/<date_to>', methods=['GET'])
def toll_station_passes(tollStationID, date_from, date_to):
    request_timestamp = get_current_timestamp()

    try:
        # Create the appropriate query
        query = """
            SELECT 
                c.transaction_ID,
                c.date AS timestamp,
                o.operator AS operator,  -- station operator
                t.toll_ID,
                c.tagRef,
                c.amount,
                c.op_ID,
                tg.tagHomeID
            FROM Charges c
            JOIN Toll t      ON c.toll_ID = t.toll_ID
            JOIN Operator o  ON t.operator_id = o.op_ID
            JOIN Tags tg     ON c.tagRef = tg.tagRef
            WHERE t.toll_ID = %s
              AND c.date BETWEEN %s AND %s
            ORDER BY c.date
        """
        cursor = db.connection.cursor()
        cursor.execute(
            query,
            (tollStationID, date_from, date_to)
        )
        results_data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        # print executed query
        # print(cursor._executed)
        
        rows = [dict(zip(column_names, entry)) for entry in results_data]
        cursor.close()
        print(rows)

        # If no rows are returned, you might want to handle that gracefully
        if not rows:
            return jsonify({
                'stationID': tollStationID,
                'stationOperator': None,
                'requestTimestamp': request_timestamp,
                'periodFrom': date_from,
                'periodTo': date_to,
                'nPasses': 0,
                'passList': []
            }), 200
        
        response = {
            'stationID': tollStationID,
            'stationOperator': rows[0]['operator'],  # from the first record
            'requestTimestamp': request_timestamp,
            'periodFrom': date_from,
            'periodTo': date_to,
            'nPasses': len(rows),
            'passList': [
                {
                    'passIndex': index + 1,
                    'passID': row['transaction_ID'],
                    'timestamp': row['timestamp'],
                    'tagID': row['tagRef'],
                    'tagProvider': row['tagHomeID'],
                    'passType': 'visitor' if row['op_ID'] != row['tagHomeID'] else 'home',
                    'passCharge': row['amount']
                } for index, row in enumerate(rows)
            ]
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500

@analysis.route('/passAnalysis/<stationOpID>/<tagOpID>/<date_from>/<date_to>', methods=['GET'])
def pass_analysis(stationOpID, tagOpID, date_from, date_to):
    request_timestamp = get_current_timestamp()

    try:
        # Adjust the query so it selects exactly the columns
        # you use below in the JSON response
        query = """
            SELECT 
                c.transaction_ID,
                c.date AS timestamp,
                t.operator_id AS op_id,  -- station operator
                t.toll_ID,
                c.tagRef,
                c.amount,
                c.op_ID,
                tg.tagHomeID
            FROM Charges c
            JOIN Toll t      ON c.toll_ID = t.toll_ID
            JOIN Tags tg     ON c.tagRef = tg.tagRef
            WHERE t.operator_id = %s
                AND c.tagRef = %s
                AND c.date BETWEEN %s AND %s
            ORDER BY c.date
        """
        cursor = db.connection.cursor()
        cursor.execute(
            query,
            (stationOpID, tagOpID, date_from, date_to)
        )
        results_data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        # print executed query
        # print(cursor._executed)
        
        rows = [dict(zip(column_names, entry)) for entry in results_data]
        cursor.close()
        print(rows)

        # If no rows are returned, you might want to handle that gracefully
        if not rows:
            return jsonify({
                'stationOpID': stationOpID,
                'tagOpID': tagOpID,
                'requestTimestamp': request_timestamp,
                'periodFrom': date_from,
                'periodTo': date_to,
                'nPasses': 0,
                'passList': []
            }), 200
        
        response = {
            'stationOpID': stationOpID,
            'tagOpID': tagOpID,  # from the first record
            'requestTimestamp': request_timestamp,
            'periodFrom': date_from,
            'periodTo': date_to,
            'nPasses': len(rows),
            'passList': [
                {
                    'passIndex': index + 1,
                    'passID': row['transaction_ID'],
                    'stationID': row['toll_ID'],
                    'timestamp': row['timestamp'],
                    'tagID': row['tagRef'],
                    'passCharge': row['amount']
                } for index, row in enumerate(rows)
            ]
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500

@analysis.route('/passesCost/<tollOpID>/<tagOpID>/<date_from>/<date_to>', methods=['GET'])
def passes_cost(tollOpID, tagOpID, date_from, date_to):
    request_timestamp = get_current_timestamp()

    try:
        # Adjust the query so it selects exactly the columns
        # you use below in the JSON response
        query = """
            SELECT 
                t.operator_id AS op_id,  -- station operator
                t.toll_ID,
                c.tagRef,
                c.amount,
                c.op_ID,
                tg.tagHomeID
            FROM Charges c
            JOIN Toll t      ON c.toll_ID = t.toll_ID
            JOIN Tags tg     ON c.tagRef = tg.tagRef
            WHERE t.operator_id = %s
                AND c.tagRef = %s
                AND c.date BETWEEN %s AND %s
            ORDER BY c.date
        """
        cursor = db.connection.cursor()
        cursor.execute(
            query,
            (tollOpID, tagOpID, date_from, date_to)
        )
        results_data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        # print executed query
        # print(cursor._executed)
        
        rows = [dict(zip(column_names, entry)) for entry in results_data]
        cursor.close()
        print(rows)

        # If no rows are returned, you might want to handle that gracefully
        if not rows:
            return jsonify({
                'stationOpID': tollOpID,
                'tagOpID': tagOpID,
                'requestTimestamp': request_timestamp,
                'periodFrom': date_from,
                'periodTo': date_to,
                'nPasses': 0,
                'passesCost': 0
            }), 200
        
        response = {
            'stationOpID': tollOpID,
            'tagOpID': tagOpID,  # from the first record
            'requestTimestamp': request_timestamp,
            'periodFrom': date_from,
            'periodTo': date_to,
            'nPasses': len(rows),
            'passesCost': sum(row['amount'] for row in rows)
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500

@analysis.route('/chargesBy/<tollOpID>/<date_from>/<date_to>', methods=['GET'])
def charges_by(tollOpID, date_from, date_to):
    request_timestamp = get_current_timestamp()

    try:
        # Adjust the query so it selects exactly the columns
        # you use below in the JSON response
        query = """
            SELECT 
                tg.tagHomeID AS op_id,
                COUNT(*)     AS n_passes,
                SUM(c.amount) AS debt
            FROM Charges AS c
            JOIN Toll AS t       ON c.toll_ID = t.toll_ID
            JOIN Operator AS st  ON t.operator_id = st.op_ID
            JOIN Tags AS tg      ON c.tagRef = tg.tagRef
            WHERE st.op_ID = %s
                AND c.date BETWEEN %s AND %s
                -- exclude the same op_ID:
                AND tg.tagHomeID <> st.op_ID
            GROUP BY tg.tagHomeID
            ORDER BY tg.tagHomeID;
            """

        cursor = db.connection.cursor()
        cursor.execute(
            query,
            (tollOpID, date_from, date_to)
        )
        results_data = cursor.fetchall()
        column_names = [i[0] for i in cursor.description]
        # print executed query
        # print(cursor._executed)
        
        rows = [dict(zip(column_names, entry)) for entry in results_data]
        cursor.close()
        print(rows)

        # If no rows are returned, you might want to handle that gracefully
        if not rows:
            return jsonify({
                'tollOpID': tollOpID,
                'requestTimestamp': request_timestamp,
                'periodFrom': date_from,
                'periodTo': date_to,
                'vOpList': []
            }), 200
        
        response = {
            'tollOpID': tollOpID,
            'requestTimestamp': request_timestamp,
            'periodFrom': date_from,
            'periodTo': date_to,
            'vOpList': [
                {
                    'visitingOpID': row['op_id'],
                    'nPasses': row['n_passes'],
                    'passesCost': row['debt'],
                } for index, row in enumerate(rows)
            ]
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'status': 'failed', 'info': str(e)}), 500
