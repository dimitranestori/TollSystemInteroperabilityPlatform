import unittest
import requests
import json
from datetime import datetime, timedelta

class TollSystemAPITest(unittest.TestCase):
    BASE_URL = "https://localhost:9115/api"  # Adjust if your server runs on a different port

    def test_1_health_check(self):
        """Test the healthcheck endpoint"""
        response = requests.get(f"{self.BASE_URL}/admin/healthcheck", verify=False)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'OK')
        self.assertIn('dbconnection', data)
        self.assertIn('n_stations', data)
        self.assertIn('n_passes', data)

    def test_2_reset_stations(self):
        """Test the resetstations endpoint"""
        response = requests.post(f"{self.BASE_URL}/admin/resetstations", verify=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')

    def test_3_reset_passes(self):
        """Test the resetpasses endpoint"""
        response = requests.post(f"{self.BASE_URL}/admin/resetpasses", verify=False)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'OK')

    # Commented out file upload since the file might not exist
    def test_4_add_passes(self):
         """Test the addpasses endpoint"""
         files = {'file': ('test_passes.csv', open('test_passes.csv', 'rb'))}
         response = requests.post(f"{self.BASE_URL}/admin/addpasses", files=files, verify=False)
         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.json()['status'], 'OK')

    def test_5_toll_station_passes(self):
        """Test the tollStationPasses endpoint"""
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{self.BASE_URL}/tollStationPasses/AO01/{date_from}/{date_to}", verify=False)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('stationID', data)
        self.assertIn('passList', data)

    def test_6_pass_analysis(self):
        """Test the passAnalysis endpoint"""
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{self.BASE_URL}/passAnalysis/AM/AO01/{date_from}/{date_to}", verify=False)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('stationOpID', data)
        self.assertIn('passList', data)

    def test_7_passes_cost(self):
        """Test the passesCost endpoint"""
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{self.BASE_URL}/passesCost/AM/AO01/{date_from}/{date_to}", verify=False)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('passesCost', data)
        self.assertIn('nPasses', data)

    def test_8_charges_by(self):
        """Test the chargesBy endpoint"""
        date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')
        response = requests.get(f"{self.BASE_URL}/chargesBy/AM/{date_from}/{date_to}", verify=False)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('vOpList', data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
