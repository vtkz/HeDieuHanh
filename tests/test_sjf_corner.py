"""Unit test SJF Non-preemptive + corner cases (Giai đoạn 4, TV5 - Duy)."""
import random
import unittest

from helpers import run, by_pid, as_tuple, averages, check_invariants


class TestSJF(unittest.TestCase):
    def test_simultaneous_arrival_orders_by_burst(self):
        rows = [("P1", 0, 6), ("P2", 0, 2), ("P3", 0, 4), ("P4", 0, 1)]
        _, gantt = run("SJF", rows)
        self.assertEqual([g[0] for g in gantt], ["P4", "P2", "P3", "P1"])

    def test_burst_tie_then_pid(self):
        _, gantt = run("SJF", [("P3", 0, 4), ("P1", 0, 4), ("P2", 0, 4)])
        self.assertEqual([g[0] for g in gantt], ["P1", "P2", "P3"])

    def test_burst_tie_then_arrival_before_pid(self):
        """BT bằng nhau -> AT nhỏ hơn thắng, KỂ CẢ khi PID lớn hơn."""
        rows = [("P1", 0, 5),            # chiếm CPU 0-5
                ("P9", 1, 3), ("P0", 2, 3)]  # cùng BT; P9 đến sớm hơn dù PID lớn hơn
        _, gantt = run("SJF", rows)
        self.assertEqual([g[0] for g in gantt], ["P1", "P9", "P0"])

    def test_non_preemptive_short_job_waits(self):
        """Tiến trình ngắn đến giữa chừng KHÔNG được cướp CPU."""
        results, gantt = run("SJF", [("P1", 0, 8), ("P2", 1, 1)])
        self.assertEqual(gantt, [("P1", 0, 8), ("P2", 8, 9)])
        self.assertEqual(by_pid(results)["P2"].waiting_time, 7)

    def test_only_arrived_processes_are_candidates(self):
        """Tiến trình ngắn nhất nhưng CHƯA đến thì không được chọn."""
        rows = [("P1", 0, 3), ("P2", 1, 6), ("P3", 100, 1)]
        _, gantt = run("SJF", rows)
        self.assertEqual(gantt, [("P1", 0, 3), ("P2", 3, 9), ("IDLE", 9, 100), ("P3", 100, 101)])

    def test_huge_burst_gap(self):
        """Chênh lệch Burst Time cực lớn."""
        rows = [("P1", 0, 10**6), ("P2", 1, 1), ("P3", 1, 1), ("P4", 1, 1)]
        results, gantt = run("SJF", rows)
        got = by_pid(results)
        self.assertEqual(gantt[0], ("P1", 0, 10**6))      # P1 đến trước, không bị cướp
        self.assertEqual([g[0] for g in gantt[1:]], ["P2", "P3", "P4"])
        self.assertEqual(got["P2"].waiting_time, 10**6 - 1)
        check_invariants(self, rows, results, gantt)

    def test_huge_burst_gap_simultaneous(self):
        rows = [("P1", 0, 10**6), ("P2", 0, 1), ("P3", 0, 2)]
        _, gantt = run("SJF", rows)
        self.assertEqual([g[0] for g in gantt], ["P2", "P3", "P1"])

    def test_single_process_late(self):
        results, gantt = run("SJF", [("P1", 4, 2)])
        self.assertEqual(gantt, [("IDLE", 0, 4), ("P1", 4, 6)])
        self.assertEqual(as_tuple(results[0]), (4, 6, 2, 0))

    def test_starvation_long_job_runs_last(self):
        """Đói tài nguyên: dòng tiến trình ngắn liên tục khiến tiến trình dài chờ đến cuối."""
        rows = [("P0", 0, 2), ("LONG", 1, 50)] + [(f"S{k:02d}", k, 1) for k in range(2, 22)]
        results, gantt = run("SJF", rows)
        order = [g[0] for g in gantt if g[0] != "IDLE"]
        self.assertEqual(order[-1], "LONG")
        self.assertEqual(by_pid(results)["LONG"].waiting_time, 22 - 1)  # chạy lúc t=22
        check_invariants(self, rows, results, gantt)

    def test_equal_to_fcfs_when_only_one_ready_each_time(self):
        rows = [("P1", 0, 2), ("P2", 5, 9), ("P3", 20, 1)]
        _, g_sjf = run("SJF", rows)
        _, g_fcfs = run("FCFS", rows)
        self.assertEqual(g_sjf, g_fcfs)

    def test_many_simultaneous_sorted_by_burst_then_pid(self):
        rng = random.Random(7)
        rows = [(f"P{i:04d}", 0, rng.randint(1, 50)) for i in range(1000)]
        _, gantt = run("SJF", rows)
        expected = [p for p, _, b in sorted(rows, key=lambda r: (r[2], r[1], r[0]))]
        self.assertEqual([g[0] for g in gantt], expected)

    def test_sjf_never_worse_than_fcfs_when_all_arrive_at_zero(self):
        """Tính chất lý thuyết: khi AT đều = 0, SJF cho AWT tối ưu (<= FCFS).
        Lưu ý: KHÔNG đúng tổng quát khi AT khác nhau -> không test trường hợp đó."""
        for seed in range(50):
            rng = random.Random(seed)
            rows = [(f"P{i}", 0, rng.randint(1, 30)) for i in range(rng.randint(2, 15))]
            awt_sjf = averages(run("SJF", rows)[0])[0]
            awt_fcfs = averages(run("FCFS", rows)[0])[0]
            self.assertLessEqual(awt_sjf, awt_fcfs + 1e-9, f"seed={seed}")


if __name__ == "__main__":
    unittest.main()
