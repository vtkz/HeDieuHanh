"""Unit test FCFS (Giai đoạn 3, TV5 - Duy)."""
import random
import unittest

from helpers import run, by_pid, as_tuple, averages, check_invariants


class TestFCFS(unittest.TestCase):
    def test_single_process_at_zero(self):
        results, gantt = run("FCFS", [("P1", 0, 7)])
        self.assertEqual(as_tuple(results[0]), (0, 7, 7, 0))
        self.assertEqual(gantt, [("P1", 0, 7)])

    def test_single_process_starts_late_has_idle(self):
        results, gantt = run("FCFS", [("P1", 5, 3)])
        self.assertEqual(as_tuple(results[0]), (5, 8, 3, 0))
        self.assertEqual(gantt, [("IDLE", 0, 5), ("P1", 5, 8)])

    def test_input_order_does_not_matter(self):
        rows = [("P1", 0, 4), ("P2", 2, 3), ("P3", 3, 1), ("P4", 9, 2)]
        base, base_g = run("FCFS", rows)
        for seed in range(10):
            shuffled = rows[:]
            random.Random(seed).shuffle(shuffled)
            res, g = run("FCFS", shuffled)
            self.assertEqual({k: as_tuple(v) for k, v in by_pid(res).items()},
                             {k: as_tuple(v) for k, v in by_pid(base).items()})
            self.assertEqual(g, base_g)

    def test_same_arrival_tiebreak_by_pid(self):
        """AT bằng nhau -> PID nhỏ nhất (từ điển) chạy trước."""
        rows = [("P3", 0, 1), ("P1", 0, 9), ("P2", 0, 5)]
        _, gantt = run("FCFS", rows)
        self.assertEqual([g[0] for g in gantt], ["P1", "P2", "P3"])

    def test_pid_ordering_is_lexicographic_not_numeric(self):
        """README: 'theo thứ tự từ điển' -> 'P10' < 'P2'. Test ghi nhận hành vi này."""
        _, gantt = run("FCFS", [("P2", 0, 1), ("P10", 0, 1)])
        self.assertEqual([g[0] for g in gantt], ["P10", "P2"])

    def test_burst_time_ignored_by_fcfs(self):
        """FCFS không được ưu tiên tiến trình ngắn."""
        _, gantt = run("FCFS", [("P1", 0, 100), ("P2", 1, 1)])
        self.assertEqual([g[0] for g in gantt], ["P1", "P2"])

    def test_convoy_effect_numbers(self):
        """1 tiến trình dài đến trước kéo theo các tiến trình ngắn chờ lâu."""
        rows = [("P1", 0, 100), ("P2", 1, 1), ("P3", 1, 1), ("P4", 1, 1)]
        results, _ = run("FCFS", rows)
        got = by_pid(results)
        self.assertEqual(got["P2"].waiting_time, 99)
        self.assertEqual(got["P3"].waiting_time, 100)
        self.assertEqual(got["P4"].waiting_time, 101)
        self.assertEqual(averages(results)[0], 75.0)

    def test_idle_between_processes(self):
        results, gantt = run("FCFS", [("P1", 0, 2), ("P2", 10, 2)])
        self.assertEqual(gantt, [("P1", 0, 2), ("IDLE", 2, 10), ("P2", 10, 12)])
        self.assertEqual(by_pid(results)["P2"].waiting_time, 0)

    def test_no_idle_when_back_to_back(self):
        """AT đúng bằng thời điểm CPU rảnh thì KHÔNG sinh đoạn IDLE rỗng."""
        _, gantt = run("FCFS", [("P1", 0, 3), ("P2", 3, 3)])
        self.assertEqual(gantt, [("P1", 0, 3), ("P2", 3, 6)])

    def test_large_values(self):
        rows = [("P1", 0, 10**9), ("P2", 10**9 + 5, 10**9)]
        results, _ = run("FCFS", rows)
        self.assertEqual(by_pid(results)["P2"].completion_time, 2 * 10**9 + 5)

    def test_all_identical_processes(self):
        rows = [(f"P{i}", 0, 2) for i in range(1, 6)]
        results, gantt = run("FCFS", rows)
        self.assertEqual([g[0] for g in gantt], ["P1", "P2", "P3", "P4", "P5"])
        check_invariants(self, rows, results, gantt)

    def test_rerun_same_list_is_stable(self):
        """GUI chạy nhiều lần trên cùng một list: kết quả không được 'dính' trạng thái cũ."""
        from helpers import make, engine_fn, norm
        procs = make([("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 8)])
        r1, g1 = engine_fn("FCFS")(procs)
        engine_fn("SJF")(procs)
        r2, g2 = engine_fn("FCFS")(procs)
        key = lambda p: p.process_id
        self.assertEqual([as_tuple(norm(p)) for p in sorted(r1, key=lambda p: norm(p).process_id)],
                         [as_tuple(norm(p)) for p in sorted(r2, key=lambda p: norm(p).process_id)])
        self.assertEqual([tuple(x) for x in g1], [tuple(x) for x in g2])

    def test_empty_input_does_not_crash_badly(self):
        """Chưa có đặc tả: chấp nhận trả về rỗng HOẶC ném ValueError (không được ném lỗi khác)."""
        try:
            results, gantt = run("FCFS", [])
            self.assertEqual(len(results), 0)
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
