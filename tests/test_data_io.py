
import csv
import tempfile
import unittest
from pathlib import Path

from data_io import read_processes_csv, export_results_csv


class TestDataIO(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        self.input_file = self.folder / "processes.csv"

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, content):
        self.input_file.write_text(content, encoding="utf-8")

    def test_read_valid_csv(self):
        self.write_csv(
            "ProcessID,ArrivalTime,BurstTime\n"
            "P1,0,5\n"
            "P2,1,3\n"
        )

        result = read_processes_csv(self.input_file)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["ProcessID"], "P1")
        self.assertEqual(result[1]["BurstTime"], 3)

    def test_reject_duplicate_process_id(self):
        self.write_csv(
            "ProcessID,ArrivalTime,BurstTime\n"
            "P1,0,5\n"
            "P1,1,3\n"
        )

        with self.assertRaisesRegex(ValueError, "bi trung"):
            read_processes_csv(self.input_file)

    def test_reject_negative_arrival_time(self):
        self.write_csv(
            "ProcessID,ArrivalTime,BurstTime\n"
            "P1,-1,5\n"
        )

        with self.assertRaisesRegex(ValueError, "ArrivalTime"):
            read_processes_csv(self.input_file)

    def test_reject_zero_burst_time(self):
        self.write_csv(
            "ProcessID,ArrivalTime,BurstTime\n"
            "P1,0,0\n"
        )

        with self.assertRaisesRegex(ValueError, "BurstTime"):
            read_processes_csv(self.input_file)

    def test_reject_wrong_headers(self):
        self.write_csv(
            "ProcessID,ArrivalTime\n"
            "P1,0\n"
        )

        with self.assertRaisesRegex(ValueError, "Tieu de CSV"):
            read_processes_csv(self.input_file)

    def test_export_results_csv(self):
        results = [
            {
                "ProcessID": "P1",
                "ArrivalTime": 0,
                "BurstTime": 5,
                "WaitingTime": 0
            }
        ]
        output_file = self.folder / "results.csv"

        returned_path = export_results_csv(results, output_file)

        self.assertTrue(returned_path.exists())

        with open(returned_path, encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["ProcessID"], "P1")
        self.assertEqual(rows[0]["WaitingTime"], "0")


if __name__ == "__main__":
    unittest.main()
