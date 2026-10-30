"""Unit test cho SJF không độc quyền (SchedulerEngine.run_sjf_non_preemptive) - TV5, tuần 4.

Nội dung kiểm thử:
  1. Góc chết (corner cases): đến đồng thời, BT bằng nhau, chênh lệch BT rất lớn,
     đến đúng lúc CPU rảnh, CPU Idle, một tiến trình, danh sách rỗng, ngẫu nhiên.
     Dữ liệu viết thẳng trong test nên không phụ thuộc file CSV hay tên cột.
  2. Dữ liệu mẫu trong data/ (TC01, TC02, TC04, TC05, TC06, TC07),
     so với bảng SJF tính tay trong docs/test_cases.md.
  3. So sánh kết quả SJF với bảng Test Oracle (test_oracle.csv) của TV2.

Mỗi ca chạy 2 lần: đầu vào giữ nguyên và đầu vào đảo ngược thứ tự.
Mọi kết quả đều được kiểm tra thêm các tính chất bắt buộc: công thức thời gian,
không chồng lấn, đúng quy tắc chọn SJF, không để CPU rảnh khi có tiến trình sẵn sàng.

Chạy từ thư mục gốc dự án:
    python -m unittest discover -s tests -v
"""
import csv
import os
import random
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import Process, SchedulerEngine  # noqa: E402

DATA_DIR = os.path.join(ROOT, "data")

ORACLE_CANDIDATES = [
    os.path.join(ROOT, "test_oracle.csv"),
    os.path.join(ROOT, "data", "test_oracle.csv"),
    os.path.join(ROOT, "tests", "test_oracle.csv"),
    os.path.join(ROOT, "test", "test_oracle.csv"),
    os.path.join(ROOT, "docs", "test_oracle.csv"),
]


# ---------------------------------------------------------------- tiện ích
def tao_tien_trinh(rows):
    return [Process(pid, at, bt) for pid, at, bt in rows]


def doc_csv_theo_vi_tri(duong_dan):
    """Đọc CSV theo vị trí cột (ProcessID, AT, BT), bỏ dòng tiêu đề.
    Không phụ thuộc tên cột nên không bị ảnh hưởng nếu nhóm đổi tên tiêu đề."""
    rows = []
    with open(duong_dan, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for dong in reader:
            if not dong or not any(c.strip() for c in dong):
                continue
            rows.append((dong[0].strip(), int(dong[1]), int(dong[2])))
    return rows


def tim_oracle():
    for duong_dan in ORACLE_CANDIDATES:
        if os.path.exists(duong_dan):
            return duong_dan
    return None


def doc_oracle(duong_dan, thuat_toan="SJF"):
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
    gantt, hien_tai = [], 0
    for r in rows:
        if hien_tai < r["ST"]:
            gantt.append(("IDLE", hien_tai, r["ST"]))
        gantt.append((r["ProcessID"], r["ST"], r["CT"]))
        hien_tai = r["CT"]
    return gantt


class SJFTestBase(unittest.TestCase):

    def chay_sjf(self, rows, dao_nguoc=False):
        dau_vao = tao_tien_trinh(rows)
        if dao_nguoc:
            dau_vao.reverse()
        return SchedulerEngine.run_sjf_non_preemptive(dau_vao)

    def kiem_tra_bat_bien(self, rows, ket_qua, gantt):
        """Các tính chất mà mọi kết quả SJF không độc quyền đều phải thỏa."""
        self.assertEqual(sorted(p.pid for p in ket_qua), sorted(r[0] for r in rows),
                         "Mỗi tiến trình phải chạy đúng 1 lần")
        for p in ket_qua:
            with self.subTest(tinh_chat="cong_thuc", pid=p.pid):
                self.assertGreaterEqual(p.st, p.at, "Chạy trước khi đến")
                self.assertEqual(p.ft, p.st + p.bt, "CT != ST + BT")
                self.assertEqual(p.tat, p.ft - p.at, "TAT != CT - AT")
                self.assertEqual(p.wt, p.tat - p.bt, "WT != TAT - BT")
                self.assertEqual(p.rt, p.st - p.at, "RT != ST - AT")

        # Quy tắc chọn SJF, không chồng lấn, không để CPU rảnh khi có việc
        con_lai = list(ket_qua)
        ft_truoc = 0
        for p in ket_qua:
            with self.subTest(tinh_chat="quy_tac_chon", pid=p.pid):
                self.assertGreaterEqual(p.st, ft_truoc, "Hai tiến trình chồng lấn")
                san_sang = [q for q in con_lai if q.at <= p.st]
                self.assertTrue(any(q is p for q in san_sang), "Chọn tiến trình chưa đến")
                chon_dung = min(san_sang, key=lambda q: (q.bt, q.at, q.pid))
                self.assertIs(chon_dung, p, "Không chọn tiến trình theo (BT, AT, ProcessID)")
                self.assertEqual(p.st, max(ft_truoc, min(q.at for q in con_lai)),
                                 "CPU rảnh trong khi có tiến trình sẵn sàng")
            con_lai.remove(p)
            ft_truoc = p.ft

        # Gantt chart liền mạch từ 0 và khớp với kết quả
        if ket_qua:
            self.assertEqual(gantt[0][1], 0, "Gantt phải bắt đầu từ 0")
            for a, b in zip(gantt, gantt[1:]):
                self.assertEqual(a[2], b[1], "Gantt bị hở hoặc chồng")
            for ten, st, ft in gantt:
                self.assertGreater(ft, st, "Đoạn Gantt có độ dài <= 0")
            self.assertEqual(
                sorted((t, s, f) for t, s, f in gantt if t != "IDLE"),
                sorted((p.pid, p.st, p.ft) for p in ket_qua),
                "Gantt không khớp kết quả từng tiến trình")

    def so_sanh(self, rows, bang, gantt_dung=None):
        """bang: danh sách (ProcessID, ST, CT, TAT, WT, RT) theo thứ tự chạy."""
        ket_qua_giu, ket_qua_dao = None, None
        for dao_nguoc in (False, True):
            with self.subTest(dau_vao="dao_nguoc" if dao_nguoc else "giu_nguyen"):
                ket_qua, gantt = self.chay_sjf(rows, dao_nguoc)
                self.assertEqual([p.pid for p in ket_qua], [b[0] for b in bang],
                                 "Sai thứ tự chạy")
                for p, (pid, st, ct, tat, wt, rt) in zip(ket_qua, bang):
                    with self.subTest(pid=pid):
                        self.assertEqual(
                            (p.st, p.ft, p.tat, p.wt, p.rt), (st, ct, tat, wt, rt),
                            "Lệch (ST, CT, TAT, WT, RT)")
                if gantt_dung is not None:
                    self.assertEqual(gantt, gantt_dung, "Gantt chart lệch")
                self.kiem_tra_bat_bien(rows, ket_qua, gantt)


# ------------------------------------------------------------ 1. Góc chết
class TestSJFGocChet(SJFTestBase):

    def test_gc01_den_cung_luc_bt_khac_nhau(self):
        self.so_sanh(
            [("P1", 0, 6), ("P2", 0, 2), ("P3", 0, 4)],
            [("P2", 0, 2, 2, 0, 0),
             ("P3", 2, 6, 6, 2, 2),
             ("P1", 6, 12, 12, 6, 6)])

    def test_gc02_den_cung_luc_bt_bang_nhau_phan_hoa_theo_pid(self):
        # Đầu vào cố tình xếp lộn ProcessID
        self.so_sanh(
            [("P3", 0, 3), ("P1", 0, 3), ("P2", 0, 3)],
            [("P1", 0, 3, 3, 0, 0),
             ("P2", 3, 6, 6, 3, 3),
             ("P3", 6, 9, 9, 6, 6)])

    def test_gc03_bt_bang_nhau_phan_hoa_theo_at_truoc_pid(self):
        # P2 và P3 cùng BT = 3, P3 đến sớm hơn (AT = 1) nên phải chạy trước P2
        # dù ProcessID của P2 nhỏ hơn.
        self.so_sanh(
            [("P1", 0, 5), ("P2", 2, 3), ("P3", 1, 3)],
            [("P1", 0, 5, 5, 0, 0),
             ("P3", 5, 8, 7, 4, 4),
             ("P2", 8, 11, 9, 6, 6)])

    def test_gc04_chenh_lech_bt_lon_khong_ngat_tien_trinh_dang_chay(self):
        # P1 rất dài đến trước; các tiến trình ngắn đến sau không được ngắt P1.
        self.so_sanh(
            [("P1", 0, 1000), ("P2", 1, 1), ("P3", 2, 1), ("P4", 3, 2)],
            [("P1", 0, 1000, 1000, 0, 0),
             ("P2", 1000, 1001, 1000, 999, 999),
             ("P3", 1001, 1002, 1000, 999, 999),
             ("P4", 1002, 1004, 1001, 999, 999)])

    def test_gc05_chenh_lech_bt_cuc_lon(self):
        # BT = 10^9: thuật toán không được chạy từng đơn vị thời gian.
        self.so_sanh(
            [("P1", 0, 1000000000), ("P2", 0, 1)],
            [("P2", 0, 1, 1, 0, 0),
             ("P1", 1, 1000000001, 1000000001, 1, 1)])

    def test_gc06_den_dung_luc_cpu_ranh(self):
        # P2, P3 đến đúng lúc P1 xong (t = 4): phải tính là đã đến, chọn P3 (BT nhỏ hơn).
        self.so_sanh(
            [("P1", 0, 4), ("P2", 4, 2), ("P3", 4, 1)],
            [("P1", 0, 4, 4, 0, 0),
             ("P3", 4, 5, 1, 0, 0),
             ("P2", 5, 7, 3, 1, 1)],
            [("P1", 0, 4), ("P3", 4, 5), ("P2", 5, 7)])

    def test_gc07_den_sau_cpu_ranh_mot_don_vi(self):
        # P2 đến ở t = 5, trong khi P1 xong ở t = 4: phải có Idle 4-5.
        self.so_sanh(
            [("P1", 0, 4), ("P2", 5, 1)],
            [("P1", 0, 4, 4, 0, 0),
             ("P2", 5, 6, 1, 0, 0)],
            [("P1", 0, 4), ("IDLE", 4, 5), ("P2", 5, 6)])

    def test_gc08_cpu_idle_dau_va_giua(self):
        self.so_sanh(
            [("P1", 3, 2), ("P2", 10, 1)],
            [("P1", 3, 5, 2, 0, 0),
             ("P2", 10, 11, 1, 0, 0)],
            [("IDLE", 0, 3), ("P1", 3, 5), ("IDLE", 5, 10), ("P2", 10, 11)])

    def test_gc09_mot_tien_trinh(self):
        self.so_sanh(
            [("P1", 0, 5)],
            [("P1", 0, 5, 5, 0, 0)],
            [("P1", 0, 5)])

    def test_gc10_danh_sach_rong(self):
        ket_qua, gantt = SchedulerEngine.run_sjf_non_preemptive([])
        self.assertEqual(ket_qua, [])
        self.assertEqual(gantt, [])

    def test_gc11_nhieu_tien_trinh_cung_luc_bt_giam_dan(self):
        self.so_sanh(
            [("P1", 0, 5), ("P2", 0, 4), ("P3", 0, 3), ("P4", 0, 2), ("P5", 0, 1)],
            [("P5", 0, 1, 1, 0, 0),
             ("P4", 1, 3, 3, 1, 1),
             ("P3", 3, 6, 6, 3, 3),
             ("P2", 6, 10, 10, 6, 6),
             ("P1", 10, 15, 15, 10, 10)])

    def test_gc12_ngau_nhien_chenh_lech_bt_lon(self):
        # Seed cố định nên kết quả tái lập được. Tối đa 9 tiến trình (P1..P9)
        # để không vướng việc so sánh ProcessID theo chuỗi (P10 < P2).
        rng = random.Random(2026)
        for lan in range(300):
            n = rng.randint(1, 9)
            rows = [(f"P{i}", rng.randint(0, 20),
                     rng.choice([1, 1, 2, 3, 5, 50, 500, 5000]))
                    for i in range(1, n + 1)]
            with self.subTest(lan=lan, rows=rows):
                kq_giu, gantt_giu = self.chay_sjf(rows)
                kq_dao, gantt_dao = self.chay_sjf(rows, dao_nguoc=True)
                self.kiem_tra_bat_bien(rows, kq_giu, gantt_giu)
                self.kiem_tra_bat_bien(rows, kq_dao, gantt_dao)
                self.assertEqual([(p.pid, p.st, p.ft) for p in kq_giu],
                                 [(p.pid, p.st, p.ft) for p in kq_dao],
                                 "Kết quả phụ thuộc thứ tự đầu vào")


# ------------------------------------------- 2. Dữ liệu mẫu (test_cases.md)
class TestSJFDuLieuMau(SJFTestBase):

    def doc(self, ten_file):
        return doc_csv_theo_vi_tri(os.path.join(DATA_DIR, ten_file))

    def test_tc01_du_lieu_thong_thuong(self):
        self.so_sanh(self.doc("normal.csv"), [
            ("P1", 0, 5, 5, 0, 0),
            ("P3", 5, 7, 5, 3, 3),
            ("P2", 7, 10, 9, 6, 6),
            ("P4", 10, 14, 10, 6, 6)])

    def test_tc02_cpu_idle(self):
        self.so_sanh(self.doc("cpu_idle.csv"), [
            ("P1", 2, 5, 3, 0, 0),
            ("P2", 8, 10, 2, 0, 0)],
            [("IDLE", 0, 2), ("P1", 2, 5), ("IDLE", 5, 8), ("P2", 8, 10)])

    def test_tc04_den_cung_luc(self):
        self.so_sanh(self.doc("same_arrival.csv"), [
            ("P2", 0, 2, 2, 0, 0),
            ("P3", 2, 4, 4, 2, 2),
            ("P1", 4, 8, 8, 4, 4)])

    def test_tc05_mot_tien_trinh(self):
        self.so_sanh(self.doc("single_process.csv"), [
            ("P1", 0, 5, 5, 0, 0)])

    def test_tc06_bt_bang_nhau(self):
        self.so_sanh(self.doc("equal_burst.csv"), [
            ("P2", 0, 2, 2, 0, 0),
            ("P3", 2, 4, 4, 2, 2),
            ("P1", 4, 8, 8, 4, 4)])

    def test_tc07_den_khi_cpu_ban(self):
        self.so_sanh(self.doc("process_during_busy.csv"), [
            ("P1", 0, 6, 6, 0, 0),
            ("P3", 6, 7, 4, 3, 3),
            ("P2", 7, 9, 7, 5, 5)])


# ----------------------------------------------------- 3. Đối chiếu oracle
ORACLE_PATH = tim_oracle()
ORACLE = doc_oracle(ORACLE_PATH) if ORACLE_PATH else {}


class TestSJFOracle(SJFTestBase):

    def kiem_tra_oracle(self, rows):
        dau_vao = [(r["ProcessID"], r["AT"], r["BT"]) for r in rows]
        bang = [(r["ProcessID"], r["ST"], r["CT"], r["TAT"], r["WT"], r["ST"] - r["AT"])
                for r in rows]
        self.so_sanh(dau_vao, bang, gantt_mong_doi(rows))

    def test_co_file_oracle_va_co_du_lieu_sjf(self):
        self.assertIsNotNone(
            ORACLE_PATH,
            "Không tìm thấy test_oracle.csv. Đặt file vào một trong: "
            + ", ".join(ORACLE_CANDIDATES))
        self.assertTrue(ORACLE, "test_oracle.csv không có dòng SJF nào")


def _tao_test_oracle(rows):
    def test(self):
        self.kiem_tra_oracle(rows)
    return test


for _ten, _rows in ORACLE.items():
    setattr(TestSJFOracle, f"test_oracle_{_ten}", _tao_test_oracle(_rows))


if __name__ == "__main__":
    unittest.main(verbosity=2)
