"""Unit test cho FCFS (SchedulerEngine.run_fcfs trong main.py) - TV5, tuần 3.

Nội dung kiểm thử:
  1. Dữ liệu thông thường (TC01), CPU Idle (TC02), tiến trình đến cùng lúc (TC04):
     đọc file trong data/, so sánh với bảng tính tay trong docs/test_cases.md.
  2. So sánh kết quả FCFS với bảng Test Oracle (test_oracle.csv) của TV2.
  3. Dữ liệu không hợp lệ (TC03, TC08, TC09, TC10): CSVHandler.read_input_csv
     phải báo lỗi ValueError, không được đọc âm thầm hay dừng đột ngột.

Chạy từ thư mục gốc dự án:
    python -m unittest discover -s tests -v
"""
import csv
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import Process, SchedulerEngine, CSVHandler  # noqa: E402

DATA_DIR = os.path.join(ROOT, "data")

# Nơi có thể đặt test_oracle.csv; lấy file đầu tiên tìm thấy.
ORACLE_CANDIDATES = [
    os.path.join(ROOT, "test_oracle.csv"),
    os.path.join(ROOT, "data", "test_oracle.csv"),
    os.path.join(ROOT, "tests", "test_oracle.csv"),
    os.path.join(ROOT, "test", "test_oracle.csv"),
    os.path.join(ROOT, "docs", "test_oracle.csv"),
]


# ---------------------------------------------------------------- tiện ích
def doc_csv_theo_spec(duong_dan):
    """Đọc file CSV theo đúng định dạng spec (ProcessID,ArrivalTime,BurstTime).
    Dùng riêng cho test, không phụ thuộc CSVHandler để test FCFS độc lập."""
    tien_trinh = []
    with open(duong_dan, newline="", encoding="utf-8") as f:
        for dong in csv.DictReader(f):
            tien_trinh.append(
                Process(dong["ProcessID"], dong["ArrivalTime"], dong["BurstTime"]))
    return tien_trinh


def tim_oracle():
    for duong_dan in ORACLE_CANDIDATES:
        if os.path.exists(duong_dan):
            return duong_dan
    return None


def doc_oracle(duong_dan, thuat_toan="FCFS"):
    """Trả về {TestCase: [các dòng theo đúng thứ tự chạy trong oracle]}."""
    ket_qua = {}
    with open(duong_dan, newline="", encoding="utf-8") as f:
        for dong in csv.DictReader(f):
            if dong["Algorithm"].strip() != thuat_toan:
                continue
            ket_qua.setdefault(dong["TestCase"].strip(), []).append({
                "ProcessID": dong["ProcessID"].strip(),
                "AT": int(dong["ArrivalTime"]),
                "BT": int(dong["BurstTime"]),
                "ST": int(dong["StartTime"]),
                "CT": int(dong["CompletionTime"]),
                "TAT": int(dong["TurnaroundTime"]),
                "WT": int(dong["WaitingTime"]),
            })
    return ket_qua


def gantt_mong_doi(rows):
    """Dựng Gantt mong đợi từ oracle: khoảng trống giữa các tiến trình là IDLE."""
    gantt, hien_tai = [], 0
    for r in rows:
        if hien_tai < r["ST"]:
            gantt.append(("IDLE", hien_tai, r["ST"]))
        gantt.append((r["ProcessID"], r["ST"], r["CT"]))
        hien_tai = r["CT"]
    return gantt


# ------------------------------------------- 1. Dữ liệu mẫu (test_cases.md)
class TestFCFSDuLieuMau(unittest.TestCase):

    def so_sanh(self, ket_qua, bang):
        """bang: danh sách (ProcessID, ST, CT, TAT, WT, RT) theo thứ tự chạy."""
        self.assertEqual([p.pid for p in ket_qua], [b[0] for b in bang],
                         "Sai thứ tự chạy")
        for p, (pid, st, ct, tat, wt, rt) in zip(ket_qua, bang):
            with self.subTest(pid=pid):
                self.assertEqual(
                    (p.st, p.ft, p.tat, p.wt, p.rt), (st, ct, tat, wt, rt),
                    "Lệch (ST, CT, TAT, WT, RT)")

    def test_tc01_du_lieu_thong_thuong(self):
        dau_vao = doc_csv_theo_spec(os.path.join(DATA_DIR, "normal.csv"))
        ket_qua, _ = SchedulerEngine.run_fcfs(dau_vao)
        self.so_sanh(ket_qua, [
            ("P1", 0, 5, 5, 0, 0),
            ("P2", 5, 8, 7, 4, 4),
            ("P3", 8, 10, 8, 6, 6),
            ("P4", 10, 14, 10, 6, 6),
        ])

    def test_tc02_cpu_idle(self):
        dau_vao = doc_csv_theo_spec(os.path.join(DATA_DIR, "cpu_idle.csv"))
        ket_qua, gantt = SchedulerEngine.run_fcfs(dau_vao)
        self.so_sanh(ket_qua, [
            ("P1", 2, 5, 3, 0, 0),
            ("P2", 8, 10, 2, 0, 0),
        ])
        self.assertEqual(gantt, [("IDLE", 0, 2), ("P1", 2, 5),
                                 ("IDLE", 5, 8), ("P2", 8, 10)],
                         "Khoảng Idle hoặc Gantt chart sai")

    def test_tc04_tien_trinh_den_cung_luc(self):
        dau_vao = doc_csv_theo_spec(os.path.join(DATA_DIR, "same_arrival.csv"))
        ket_qua, _ = SchedulerEngine.run_fcfs(dau_vao)
        self.so_sanh(ket_qua, [
            ("P1", 0, 4, 4, 0, 0),
            ("P2", 4, 6, 6, 4, 4),
            ("P3", 6, 8, 8, 6, 6),
        ])


# ----------------------------------------------------- 2. Đối chiếu oracle
ORACLE_PATH = tim_oracle()
ORACLE = doc_oracle(ORACLE_PATH) if ORACLE_PATH else {}


class TestFCFSOracle(unittest.TestCase):

    def kiem_tra(self, rows, dao_thu_tu_dau_vao=False):
        dau_vao = [Process(r["ProcessID"], r["AT"], r["BT"]) for r in rows]
        if dao_thu_tu_dau_vao:
            dau_vao.reverse()
        ket_qua, gantt = SchedulerEngine.run_fcfs(dau_vao)

        self.assertEqual([p.pid for p in ket_qua], [r["ProcessID"] for r in rows],
                         "Sai thứ tự chạy")
        for p, r in zip(ket_qua, rows):
            with self.subTest(pid=r["ProcessID"]):
                self.assertEqual(p.st, r["ST"], "StartTime lệch")
                self.assertEqual(p.ft, r["CT"], "CompletionTime lệch")
                self.assertEqual(p.tat, r["TAT"], "TurnaroundTime lệch")
                self.assertEqual(p.wt, r["WT"], "WaitingTime lệch")
                # Oracle không có cột RT; theo spec RT = ST - AT
                self.assertEqual(p.rt, r["ST"] - r["AT"], "ResponseTime lệch")
        self.assertEqual(gantt, gantt_mong_doi(rows), "Gantt chart lệch")

    def test_co_file_oracle_va_co_du_lieu_fcfs(self):
        self.assertIsNotNone(
            ORACLE_PATH,
            "Không tìm thấy test_oracle.csv. Đặt file vào một trong: "
            + ", ".join(ORACLE_CANDIDATES))
        self.assertTrue(ORACLE, "test_oracle.csv không có dòng FCFS nào")


def _tao_test(rows):
    def test_dau_vao_giu_nguyen(self):
        self.kiem_tra(rows)

    def test_dau_vao_dao_nguoc(self):
        self.kiem_tra(rows, dao_thu_tu_dau_vao=True)

    return test_dau_vao_giu_nguyen, test_dau_vao_dao_nguoc


for _ten, _rows in ORACLE.items():
    _t1, _t2 = _tao_test(_rows)
    setattr(TestFCFSOracle, f"test_oracle_{_ten}", _t1)
    setattr(TestFCFSOracle, f"test_oracle_{_ten}_dau_vao_dao_nguoc", _t2)


# ------------------------------------------------ 3. Dữ liệu không hợp lệ
class TestDuLieuKhongHopLe(unittest.TestCase):
    """Theo spec mục 9: dữ liệu sai phải bị từ chối bằng thông báo lỗi."""

    def phai_bao_loi(self, ten_file):
        duong_dan = os.path.join(DATA_DIR, ten_file)
        with self.assertRaises(
                ValueError,
                msg=f"{ten_file}: không báo lỗi ValueError cho dữ liệu không hợp lệ"):
            CSVHandler.read_input_csv(duong_dan)

    def test_tc03_at_am_bt_bang_0_pid_trung(self):
        self.phai_bao_loi("invalid_data.csv")

    def test_tc08_thieu_cot(self):
        self.phai_bao_loi("missing_column.csv")

    def test_tc09_at_khong_phai_so(self):
        self.phai_bao_loi("non_numeric.csv")

    def test_tc10_pid_trong(self):
        self.phai_bao_loi("empty_pid.csv")


if __name__ == "__main__":
    unittest.main(verbosity=2)
