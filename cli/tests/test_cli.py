#!/usr/bin/env python3
import subprocess
import os
import sys
import json
import csv

class CLITester:
    def __init__(self, cli_script_path, valid_passes_csv):
        """
        Initialize the CLI tester with the path to the CLI script and the CSV file.
        
        :param cli_script_path: Path to the main CLI script
        :param valid_passes_csv: Path to the valid passes CSV file
        """
        self.cli_script_path = cli_script_path
        self.valid_passes_csv = valid_passes_csv
        
        # Validate file existence
        if not os.path.exists(cli_script_path):
            raise FileNotFoundError(f"CLI script not found at {cli_script_path}")
        if not os.path.exists(valid_passes_csv):
            raise FileNotFoundError(f"Valid passes CSV not found at {valid_passes_csv}")
    
    def run_command(self, command, format_type='csv'):
        """
        Run a CLI command and return the output.
        
        :param command: Command to run
        :param format_type: Output format (csv or json)
        :return: Command output
        """
        full_command = [sys.executable, self.cli_script_path] + command
        
        try:
            result = subprocess.run(
                full_command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e.stderr}")
            raise
    
    def test_healthcheck(self):
        """Test the healthcheck command"""
        print("Testing healthcheck...")
        result = self.run_command(['healthcheck'])
        print(result)
        return result is not None
    
    def test_resetpasses(self):
        """Test the resetpasses command"""
        print("Testing resetpasses...")
        result = self.run_command(['resetpasses'])
        print(result)
        return result is not None
    
    def test_resetstations(self):
        """Test the resetstations command"""
        print("Testing resetstations...")
        result = self.run_command(['resetstations'])
        print(result)
        return result is not None
    
    def test_addpasses(self):
        """Test adding passes from CSV file"""
        print("Testing addpasses...")
        result = self.run_command(['admin','--addpasses', '--source', self.valid_passes_csv])
        print(result)
        return result is not None
    
    def test_tollstationpasses(self):
        """Test retrieving toll station passes"""
        print("Testing tollstationpasses...")
        result = self.run_command([
            'tollstationpasses', 
            '--station', 'AO01', 
            '--from', '20230101', 
            '--to', '20230131'
        ])
        print(result)
        return result is not None
    
    def test_passanalysis(self):
        """Test pass analysis"""
        print("Testing passanalysis...")
        result = self.run_command([
            'passanalysis', 
            '--stationop', 'AO', 
            '--tagop', 'KB', 
            '--from', '20230101', 
            '--to', '20230131'
        ])
        print(result)
        return result is not None
    
    def test_passescost(self):
        """Test passes cost calculation"""
        print("Testing passescost...")
        result = self.run_command([
            'passescost', 
            '--stationop', 'AO', 
            '--tagop', 'KB', 
            '--from', '20230101', 
            '--to', '20230131'
        ])
        print(result)
        return result is not None
    
    def test_chargesby(self):
        """Test charges by operator"""
        print("Testing chargesby...")
        result = self.run_command([
            'chargesby', 
            '--opid', 'AO', 
            '--from', '20230101', 
            '--to', '20230131'
        ])
        print(result)
        return result is not None
    
    def run_all_tests(self):
        """Run all available tests"""
        tests = [
            self.test_healthcheck,
            self.test_resetpasses,
            self.test_resetstations,
            self.test_addpasses,
            self.test_tollstationpasses,
            self.test_passanalysis,
            self.test_passescost,
            self.test_chargesby
        ]
        
        results = {}
        for test in tests:
            try:
                results[test.__name__] = test()
            except Exception as e:
                print(f"Test {test.__name__} failed: {e}")
                results[test.__name__] = False
        
        return results

def main():
    # Adjust these paths as needed
    cli_script_path = '../se2410.py'  # Path to your CLI script
    valid_passes_csv = './valid_passes.csv'  # Path to your CSV file
    
    tester = CLITester(cli_script_path, valid_passes_csv)
    
    try:
        test_results = tester.run_all_tests()
        
        # Print summary
        print("\n--- Test Summary ---")
        for test, result in test_results.items():
            status = "PASS" if result else "FAIL"
            print(f"{test}: {status}")
        
        # Exit with non-zero status if any test fails
        if not all(test_results.values()):
            sys.exit(1)
    
    except Exception as e:
        print(f"Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
