
import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from main import CSVHandler


class TestCSVReport(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_file = Path(self.temp_dir.name) / "sjf_results.csv"

        self.processes = [
            SimpleNamespace(
                process_id="P1",
                arrival_time=0,
                burst_time=5,
                start_time=0,
                completion_time=5,
                turnaround_time=5,
                waiting_time=0,
                response_time=0
            ),
            SimpleNamespace(
                process_id="P2",
                arrival_time=1,
                burst_time=3,
                start_time=5,
                completion_time=8,
                turnaround_time=7,
                waiting_time=4,
                response_time=4
            )
        ]

        self.gantt_chart = [
            ("P1", 0, 5),
            ("P2", 5, 8)
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_export_csv_creates_file(self):
        CSVHandler.write_output_csv(
            str(self.output_file),
            self.processes,
            self.gantt_chart,
            "SJF Non-Preemptive"
        )

        self.assertTrue(self.output_file.exists())

    def test_export_csv_contains_correct_header(self):
        CSVHandler.write_output_csv(
            str(self.output_file),
            self.processes,
            self.gantt_chart,
            "SJF Non-Preemptive"
        )

        with open(self.output_file, "r", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))

        expected_header = [
            "ProcessID",
            "ArrivalTime",
            "BurstTime",
            "StartTime",
            "CompletionTime",
            "TurnaroundTime",
            "WaitingTime",
            "ResponseTime"
        ]

        self.assertEqual(rows[1], expected_header)

    def test_export_csv_contains_correct_process_data(self):
        CSVHandler.write_output_csv(
            str(self.output_file),
            self.processes,
            self.gantt_chart,
            "SJF Non-Preemptive"
        )

        with open(self.output_file, "r", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))

        self.assertEqual(
            rows[2],
            ["P1", "0", "5", "0", "5", "5", "0", "0"]
        )

        self.assertEqual(
            rows[3],
            ["P2", "1", "3", "5", "8", "7", "4", "4"]
        )

    def test_export_csv_contains_average_metrics(self):
        CSVHandler.write_output_csv(
            str(self.output_file),
            self.processes,
            self.gantt_chart,
            "SJF Non-Preemptive"
        )

        with open(self.output_file, "r", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))

        metrics = {
            row[0]: row[1]
            for row in rows
            if len(row) == 2 and row[0].startswith("Average")
        }

        self.assertEqual(metrics["AverageTurnaroundTime"], "6.00")
        self.assertEqual(metrics["AverageWaitingTime"], "2.00")
        self.assertEqual(metrics["AverageResponseTime"], "2.00")

    def test_export_csv_contains_gantt_chart_log(self):
        CSVHandler.write_output_csv(
            str(self.output_file),
            self.processes,
            self.gantt_chart,
            "SJF Non-Preemptive"
        )

        with open(self.output_file, "r", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))

        gantt_index = rows.index(["Gantt Chart Trace Log"])

        self.assertEqual(
            rows[gantt_index + 1],
            ["ProcessID", "StartTime", "CompletionTime", "Duration"]
        )

        self.assertEqual(
            rows[gantt_index + 2],
            ["P1", "0", "5", "5"]
        )

        self.assertEqual(
            rows[gantt_index + 3],
            ["P2", "5", "8", "3"]
        )


if __name__ == "__main__":
    unittest.main()
