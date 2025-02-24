#!/usr/bin/env python3
import argparse
import requests
import json
import csv
import sys
import os
from datetime import datetime
from utilities.read_cookie import read_cookie
from utilities.read_ip import read_ip

def format_output(data, format_type='csv'):
    """
    Διαμορφώνει τα δεδομένα εξόδου σύμφωνα με τον τύπο μορφοποίησης.
    """
    if format_type.lower() == 'json':
        return json.dumps(data, indent=4, ensure_ascii=False)
    else:  # csv format
        if not data:  # Check if data is None or empty
            return "No data or invalid data format"

        if isinstance(data, dict):  # Handle single dictionary case for CSV
            data = [data]  # Wrap single dictionary in a list

        if not isinstance(data, list):  # Check again after potentially wrapping in a list
            return "No data or invalid data format"

        output = []
        if data:
            headers = data[0].keys()
            output.append(','.join(headers))

            for item in data:
                row = [str(item.get(header, '')) for header in headers]
                output.append(','.join(row))

        return '\n'.join(output)

def healthcheck():
    """
    Λειτουργία ελέγχου υγείας.
    """
    url = f'https://{read_ip()}:9115/api/admin/healthcheck'
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def resetpasses():
    """
    Λειτουργία για επαναφορά διελεύσεων.
    """
    url = f'https://{read_ip()}:9115/api/admin/resetpasses'
    cookie = {'jwt': read_cookie()}
    try:
        response = requests.post(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def resetstations():
    """
    Λειτουργία για επαναφορά σταθμών.
    """
    url = f'https://{read_ip()}:9115/api/admin/resetstations'
    cookie = {'jwt': read_cookie()}
    try:
        response = requests.post(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def tollstationpasses(station, date_from, date_to):
    """
    Επιστροφή διελεύσεων για σταθμό.
    """
    cookie = {'jwt': read_cookie()}
    url = f'https://{read_ip()}:9115/api/tollStationPasses/{station}/{date_from}/{date_to}'
    try:
        response = requests.get(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def passanalysis(stationop, tagop, date_from, date_to):
    """
    Ανάλυση διελεύσεων.
    """
    cookie = {'jwt': read_cookie()}
    url = f'https://{read_ip()}:9115/api/passAnalysis/{stationop}/{tagop}/{date_from}/{date_to}'
    try:
        response = requests.get(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def passescost(stationop, tagop, date_from, date_to):
    """
    Υπολογισμός κόστους διελεύσεων.
    """
    cookie = {'jwt': read_cookie()}
    url = f'https://{read_ip()}:9115/api/passesCost/{stationop}/{tagop}/{date_from}/{date_to}'
    try:
        response = requests.get(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def chargesby(opid, date_from, date_to):
    """
    Επιστροφή χρεώσεων χειριστή.
    """
    cookie = {'jwt': read_cookie()}
    url = f'https://{read_ip()}:9115/api/chargesBy/{opid}/{date_from}/{date_to}'
    try:
        response = requests.get(url, cookies=cookie, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error connecting to backend: {e}")

def addpasses(file_path):
    """
    Λειτουργία για προσθήκη διελεύσεων από CSV αρχείο.
    """
    url = f'https://{read_ip()}:9115/api/admin/addpasses'
    cookie = {'jwt': read_cookie()}

    try:
        with open(file_path, 'rb') as f:  # Open the file in binary read mode
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}  # Prepare file for upload
            response = requests.post(url, cookies=cookie, files=files, verify=False)  # Use 'files' parameter for file upload
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except FileNotFoundError:
        raise ValueError(f"Το αρχείο CSV δεν βρέθηκε: {file_path}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Σφάλμα σύνδεσης με το backend: {e}")


def main():
    """
    Κύρια συνάρτηση για τη διαχείριση των ορισμάτων CLI και την εκτέλεση εντολών.
    """
    parser = argparse.ArgumentParser(
        description="SE2410 CLI tool για αλληλεπίδραση με το interoperability API."
    )

    subparsers = parser.add_subparsers(dest="scope", help="Scopes commands")

    # Δημιουργία ενός parent parser με το format argument
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--format', choices=['json', 'csv'], default='csv',
                                help='Μορφή εξόδου (default: csv)')

    # healthcheck
    subparsers.add_parser('healthcheck', help='Ελέγχει την υγεία του API',
                            parents=[parent_parser])

    # resetpasses
    subparsers.add_parser('resetpasses', help='Επαναφέρει τις διελεύσεις',
                            parents=[parent_parser])

    # resetstations
    subparsers.add_parser('resetstations', help='Επαναφέρει τους σταθμούς',
                            parents=[parent_parser])

    # tollstationpasses
    tollstation_parser = subparsers.add_parser('tollstationpasses',
                                            help='Επιστροφή διελεύσεων για σταθμό',
                                            parents=[parent_parser])
    tollstation_parser.add_argument('--station', required=True, help='Station ID')
    tollstation_parser.add_argument('--from', dest='date_from', required=True,
                                    help='Ημερομηνία έναρξης (YYYYMMDD)')
    tollstation_parser.add_argument('--to', dest='date_to', required=True,
                                    help='Ημερομηνία λήξης (YYYYMMDD)')

    # passanalysis
    passanalysis_parser = subparsers.add_parser('passanalysis',
                                                help='Ανάλυση διελεύσεων',
                                                parents=[parent_parser])
    passanalysis_parser.add_argument('--stationop', required=True, help='Station Operator')
    passanalysis_parser.add_argument('--tagop', required=True, help='Tag Operator')
    passanalysis_parser.add_argument('--from', dest='date_from', required=True,
                                    help='Ημερομηνία έναρξης (YYYYMMDD)')
    passanalysis_parser.add_argument('--to', dest='date_to', required=True,
                                    help='Ημερομηνία λήξης (YYYYMMDD)')

    # passescost
    passescost_parser = subparsers.add_parser('passescost',
                                            help='Υπολογισμός κόστους διελεύσεων',
                                            parents=[parent_parser])
    passescost_parser.add_argument('--stationop', required=True, help='Station Operator')
    passescost_parser.add_argument('--tagop', required=True, help='Tag Operator')
    passescost_parser.add_argument('--from', dest='date_from', required=True,
                                    help='Ημερομηνία έναρξης (YYYYMMDD)')
    passescost_parser.add_argument('--to', dest='date_to', required=True,
                                    help='Ημερομηνία λήξης (YYYYMMDD)')

    # chargesby
    chargesby_parser = subparsers.add_parser('chargesby',
                                            help='Επιστροφή χρεώσεων χειριστή',
                                            parents=[parent_parser])
    chargesby_parser.add_argument('--opid', required=True, help='Operator ID')
    chargesby_parser.add_argument('--from', dest='date_from', required=True,
                                    help='Ημερομηνία έναρξης (YYYYMMDD)')
    chargesby_parser.add_argument('--to', dest='date_to', required=True,
                                    help='Ημερομηνία λήξης (YYYYMMDD)')

    # admin scope (Modified)
    admin_parser = subparsers.add_parser('admin', help='Admin operations', parents=[parent_parser])
    admin_parser.add_argument('--addpasses', action='store_true', help='Add passes from CSV file')  # Make addpasses a boolean option
    admin_parser.add_argument('--source', dest='file_path', help='Path to the CSV file')  # Source is now an option for addpasses
    
    args = parser.parse_args()

    try:
        response = None
        date_from = None
        date_to = None
        file_path = None  # Initialize file_path

        if not args.scope:
            parser.print_help()
            return

        if hasattr(args, 'date_from') and args.date_from:
            date_from = f"{args.date_from[:4]}-{args.date_from[4:6]}-{args.date_from[6:]}"
        if hasattr(args, 'date_to') and args.date_to:
            date_to = f"{args.date_to[:4]}-{args.date_to[4:6]}-{args.date_to[6:]}"

        # Handling admin scope (Modified)
        if args.scope == 'admin':
            if args.addpasses:  # Check if the --addpasses flag is present
                if args.file_path: # Check if --source is provided
                    file_path = args.file_path
                    response = addpasses(file_path)
                    formatted_output = format_output(response, getattr(args, 'format', 'csv'))
                    print(formatted_output)
                    return
                else:
                    print("Error: --source argument is required when --addpasses is used", file=sys.stderr)
                    sys.exit(1)
            else:
                 # Handle other admin operations if needed
                 print("No admin operation specified.")
                 admin_parser.print_help()
                 return

        # Existing command handling
        if args.scope == 'healthcheck':
            response = healthcheck()
        elif args.scope == 'resetpasses':
            response = resetpasses()
        elif args.scope == 'resetstations':
            response = resetstations()
        elif args.scope == 'tollstationpasses':
            response = tollstationpasses(args.station, date_from, date_to)
        elif args.scope == 'passanalysis':
            response = passanalysis(args.stationop, args.tagop, date_from, date_to)
        elif args.scope == 'passescost':
            response = passescost(args.stationop, args.tagop, date_from, date_to)
        elif args.scope == 'chargesby':
            response = chargesby(args.opid, date_from, date_to)
        else:
            print(f"Άγνωστο scope: {args.scope}")
            parser.print_help()
            return

        if response:
            if isinstance(response, list) and response and 'timestamp' in response[0]:
                response.sort(key=lambda x: x['timestamp'])
            formatted_output = format_output(response, args.format)
            print(formatted_output)

    except ValueError as ve:
        print(f"Σφάλμα στα ορίσματα: {ve}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    except Exception as e:
        print(f"Σφάλμα: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
