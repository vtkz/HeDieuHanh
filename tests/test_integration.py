"""Integration test: CSV -> engine -> CSV, và (tuỳ chọn) logic GUI (Giai đoạn 5, TV5 - Duy).

Ghi chú: định dạng cột của file output CHƯA có đặc tả -> test chỉ kiểm tra những
điều chắc chắn (tồn tại, có header, có đủ PID, có đủ giá trị CT).
"""
import csv
import glob
import os
import tempfile
import unittest

import helpers
from helpers import CSVHandler, engine_fn, norm, by_pid, as_tuple
from oracle_data import ORACLE

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_csv")           # file CSV do QA tạo
REPO_DATA = os.path.join(os.path.dirname(HERE), "data")  # 11 file CSV của nhóm (TC01-TC11)


def data(name):
    return os.path.join(DATA, name)


class TestCSVImport(unittest.TestCase):
    def test_valid_files_load(self):
        for fname, key in [("valid_basic.csv", "A_basic"), ("valid_idle.csv", "B_idle"),
                           ("valid_tie.csv", "C_tie")]:
            with self.subTest(file=fname):
                procs = CSVHandler.read_input_csv(data(fname))
                got = sorted((norm(p).process_id, norm(p).arrival_time, norm(p).burst_time) for p in procs)
                self.assertEqual(got, sorted(ORACLE[key]["rows"]))

    def test_invalid_files_are_rejected_cleanly(self):
        """File sai phải ném ValueError/OSError (GUI bắt 2 loại này để hiện Error Dialog)."""
        for path in sorted(glob.glob(data("bad_*.csv"))):
            with self.subTest(file=os.path.basename(path)):
                with self.assertRaises((ValueError, OSError)):
                    CSVHandler.read_input_csv(path)

    def test_missing_file(self):
        with self.assertRaises((ValueError, OSError)):
            CSVHandler.read_input_csv(data("khong_ton_tai.csv"))

    def test_extra_whitespace_and_crlf(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "ws.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("ProcessID,ArrivalTime,BurstTime\r\n P1 , 0 , 5 \r\nP2,1,3\r\n")
            procs = CSVHandler.read_input_csv(path)
            self.assertEqual(sorted(norm(p).process_id for p in procs), ["P1", "P2"])

    def test_utf8_bom_header(self):
        """File CSV lưu từ Excel thường có BOM ở đầu."""
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bom.csv")
            with open(path, "w", encoding="utf-8-sig") as f:
                f.write("ProcessID,ArrivalTime,BurstTime\nP1,0,5\n")
            procs = CSVHandler.read_input_csv(path)
            self.assertEqual(len(procs), 1)


class TestRepoDataFiles(unittest.TestCase):
    """11 file CSV trong data/ của nhóm (TC01-TC11 trong docs/test_cases.md)."""
    VALID = ["normal", "cpu_idle", "same_arrival", "single_process", "equal_burst", "process_during_busy"]
    INVALID = ["invalid_data", "missing_column", "non_numeric", "empty_pid", "header_only"]

    def test_valid_files_load_and_run(self):
        for name in self.VALID:
            with self.subTest(file=name):
                procs = CSVHandler.read_input_csv(os.path.join(REPO_DATA, name + ".csv"))
                self.assertGreater(len(procs), 0)
                for algo in ("FCFS", "SJF"):
                    results, gantt = engine_fn(algo)(procs)
                    rows = [(norm(p).process_id, norm(p).arrival_time, norm(p).burst_time) for p in procs]
                    helpers.check_invariants(self, rows, [norm(p) for p in results], [tuple(g) for g in gantt])

    def test_invalid_files_are_rejected(self):
        for name in self.INVALID:
            with self.subTest(file=name):
                with self.assertRaises((ValueError, OSError)):
                    CSVHandler.read_input_csv(os.path.join(REPO_DATA, name + ".csv"))


class TestPipeline(unittest.TestCase):
    def _pipeline(self, fname, key):
        procs = CSVHandler.read_input_csv(data(fname))
        for algo in ("FCFS", "SJF"):
            with self.subTest(file=fname, algo=algo):
                results, gantt = engine_fn(algo)(procs)
                exp = ORACLE[key][algo]
                self.assertEqual({k: as_tuple(v) for k, v in by_pid([norm(p) for p in results]).items()}, exp["procs"])
                self.assertEqual([tuple(g) for g in gantt], exp["gantt"])
                with tempfile.TemporaryDirectory() as d:
                    out = os.path.join(d, f"out_{algo}.csv")
                    CSVHandler.write_output_csv(out, results, gantt, algo)
                    self.assertTrue(os.path.getsize(out) > 0)
                    with open(out, encoding="utf-8-sig", newline="") as f:
                        rows = list(csv.reader(f))
                        text = "\n".join(",".join(r) for r in rows)
                    self.assertGreaterEqual(len(rows), len(results) + 1, "thiếu dòng dữ liệu/header")
                    for pid, (_, ct, _, _) in exp["procs"].items():
                        self.assertIn(pid, text)
                        self.assertIn(str(ct), text)

    def test_basic(self):
        self._pipeline("valid_basic.csv", "A_basic")

    def test_idle(self):
        self._pipeline("valid_idle.csv", "B_idle")

    def test_tie(self):
        self._pipeline("valid_tie.csv", "C_tie")

    def test_export_unwritable_path_raises_cleanly(self):
        """Đường dẫn mà 'thư mục cha' thực ra là một file -> không thể ghi, phải ném OSError/ValueError
        (GUI bắt đúng 2 loại này để hiện hộp thoại lỗi thay vì văng ứng dụng)."""
        procs = CSVHandler.read_input_csv(data("valid_basic.csv"))
        results, gantt = engine_fn("FCFS")(procs)
        with tempfile.TemporaryDirectory() as d:
            blocker = os.path.join(d, "la_mot_file.txt")
            open(blocker, "w").close()
            bad = os.path.join(blocker, "out.csv")
            with self.assertRaises((ValueError, OSError)):
                CSVHandler.write_output_csv(bad, results, gantt, "FCFS")


# ---------------------------------------------------------------------------
# GUI logic tests - tự bỏ qua nếu máy không có tkinter hoặc không có màn hình.
# (Chưa được chạy xác minh trong môi trường soạn thảo vì thiếu tkinter.)
# ---------------------------------------------------------------------------
try:
    import tkinter as tk
    from unittest import mock
    _root = tk.Tk()
    _root.destroy()
    HAVE_GUI = True
except Exception:  # không có tkinter / DISPLAY
    HAVE_GUI = False


@unittest.skipUnless(HAVE_GUI, "Không có tkinter/DISPLAY - chạy test GUI trên máy có màn hình")
class TestGUILogic(unittest.TestCase):
    def setUp(self):
        import gui
        self.gui = gui
        self.root = tk.Tk()
        self.app = gui.SchedulerGUIApp(self.root)
        self.errors = []
        patches = [
            mock.patch.object(gui.messagebox, "showerror", side_effect=lambda *a, **k: self.errors.append(a)),
            mock.patch.object(gui.messagebox, "showwarning", side_effect=lambda *a, **k: self.errors.append(a)),
            mock.patch.object(gui.messagebox, "showinfo"),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.root.destroy)

    def _add(self, pid, at, bt):
        for entry, v in ((self.app.entry_process_id, pid), (self.app.entry_arrival_time, at),
                         (self.app.entry_burst_time, bt)):
            entry.delete(0, tk.END)
            entry.insert(0, v)
        self.app.add_process()

    def test_rejects_bad_input(self):
        for pid, at, bt in [("", "0", "5"), ("P1", "", "5"), ("P1", "abc", "5"), ("P1", "1.5", "5"),
                            ("P1", "-1", "5"), ("P1", "0", "0"), ("P1", "0", "-2")]:
            with self.subTest(row=(pid, at, bt)):
                before = len(self.errors)
                self._add(pid, at, bt)
                self.assertEqual(len(self.errors), before + 1)
                self.assertEqual(len(self.app.processes), 0)

    def test_rejects_duplicate_pid(self):
        self._add("P1", "0", "5")
        self._add("P1", "1", "2")
        self.assertEqual(len(self.app.processes), 1)
        self.assertEqual(len(self.errors), 1)

    def test_run_fills_table_and_gantt_state(self):
        for row in (("P1", "0", "5"), ("P2", "1", "3")):
            self._add(*row)
        for algo in ("FCFS", "SJF"):
            self.app.algorithm_var.set(algo)
            self.app.run_simulation()
            self.assertEqual(len(self.app.last_results), 2)
            self.assertEqual(self.app.last_algorithm, algo)
            self.assertEqual(len(self.app.tree.get_children()), 2)

    @unittest.expectedFailure
    def test_BUG_add_after_run_leaves_stale_results(self):
        """BUG GUI-01: thêm tiến trình sau khi chạy -> last_results/Gantt cũ vẫn còn,
        nên 'Xuất CSV' xuất kết quả thiếu tiến trình mới. Bỏ @expectedFailure khi đã sửa."""
        self._add("P1", "0", "5")
        self.app.run_simulation()
        self._add("P2", "1", "3")
        self.assertEqual(self.app.last_results, [])

    @unittest.expectedFailure
    def test_BUG_clear_all_keeps_old_gantt(self):
        """BUG GUI-02: 'Xóa danh sách' không xóa vùng vẽ Gantt."""
        self._add("P1", "0", "5")
        self.app.run_simulation()
        self.app.clear_all()
        self.assertEqual(len(self.app.gantt_canvas.find_all()), 0)


if __name__ == "__main__":
    unittest.main()
