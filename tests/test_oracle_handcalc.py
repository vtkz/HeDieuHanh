"""Đối chiếu kết quả của engine với Test Oracle tính tay (TV5 - Duy).

Chạy:  python -m unittest discover -s test -v
"""
import unittest

import helpers
from helpers import ALGOS, run, by_pid, as_tuple, averages
from oracle_data import ORACLE


class TestOracle(unittest.TestCase):
    def _each(self):
        for name, data in ORACLE.items():
            for algo in ALGOS:
                with self.subTest(dataset=name, algo=algo):
                    yield name, algo, data["rows"], data[algo]

    def test_per_process_metrics(self):
        """ST, CT, TAT, WT của từng tiến trình khớp bảng tính tay."""
        for name, algo, rows, exp in self._each():
            results, _ = run(algo, rows)
            got = by_pid(results)
            self.assertEqual(set(got), set(exp["procs"]))
            for pid, expected in exp["procs"].items():
                self.assertEqual(as_tuple(got[pid]), expected, f"{name}/{algo}/{pid}")

    def test_response_time_equals_waiting_time(self):
        """Non-preemptive: RT = ST - AT = WT."""
        for name, algo, rows, exp in self._each():
            results, _ = run(algo, rows)
            at = {p: a for p, a, _ in rows}
            for p in results:
                self.assertEqual(p.response_time, p.start_time - at[p.process_id])
                self.assertEqual(p.response_time, p.waiting_time)

    def test_gantt_including_idle(self):
        """Biểu đồ Gantt (kể cả đoạn IDLE) khớp bảng tính tay."""
        for name, algo, rows, exp in self._each():
            _, gantt = run(algo, rows)
            self.assertEqual(gantt, exp["gantt"], f"{name}/{algo}")

    def test_averages(self):
        for name, algo, rows, exp in self._each():
            results, _ = run(algo, rows)
            awt, atat = averages(results)
            self.assertAlmostEqual(awt, exp["avg_wt"], places=6)
            self.assertAlmostEqual(atat, exp["avg_tat"], places=6)

    def test_oracle_is_self_consistent(self):
        """Tự kiểm: bảng tính tay phải khớp bộ mô phỏng tham chiếu độc lập."""
        from reference_sim import simulate
        for name, algo, rows, exp in self._each():
            ref, ref_gantt = simulate(rows, algo)
            self.assertEqual(ref, exp["procs"], f"Oracle tính tay sai? {name}/{algo}")
            self.assertEqual(ref_gantt, exp["gantt"])


if __name__ == "__main__":
    unittest.main()
