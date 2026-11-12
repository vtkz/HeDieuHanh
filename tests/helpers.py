"""Tiện ích dùng chung cho bộ test của TV5 (Phạm Minh Duy - QA/QC).

Repo hiện có 3 kiểu main.py khác nhau giữa các nhánh (tên thuộc tính và tên hàm khác
nhau). Module này đưa tất cả về MỘT dạng chuẩn để test không phụ thuộc kiểu nào:

  thuộc tính chuẩn : process_id, arrival_time, burst_time, start_time, completion_time,
                     turnaround_time, waiting_time, response_time
  chấp nhận alias  : pid/at/bt/st/ft/tat/wt/rt, finish_time
  hàm engine       : run_fcfs | run_first_come_first_served
                     run_sjf_non_preemptive | run_shortest_job_first_non_preemptive

Khi cả nhóm chốt 1 API duy nhất, có thể giữ nguyên file này (vẫn chạy đúng).
"""
import os
import sys
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    import main as _main  # noqa: E402
    Process = _main.Process
    SchedulerEngine = _main.SchedulerEngine
    CSVHandler = _main.CSVHandler
except (ImportError, AttributeError) as exc:  # pragma: no cover
    raise ImportError(
        "main.py chưa có Process / SchedulerEngine / CSVHandler. "
        f"Hãy merge code lõi vào main.py rồi chạy lại. Chi tiết: {exc}"
    ) from exc

ALGOS = ("FCFS", "SJF")

ALIASES = {
    "process_id": ("process_id", "pid"),
    "arrival_time": ("arrival_time", "at"),
    "burst_time": ("burst_time", "bt"),
    "start_time": ("start_time", "st"),
    "completion_time": ("completion_time", "finish_time", "ft"),
    "turnaround_time": ("turnaround_time", "tat"),
    "waiting_time": ("waiting_time", "wt"),
    "response_time": ("response_time", "rt"),
}
ENGINE_NAMES = {
    "FCFS": ("run_fcfs", "run_first_come_first_served"),
    "SJF": ("run_sjf_non_preemptive", "run_shortest_job_first_non_preemptive"),
}


def attr(p, name):
    for a in ALIASES[name]:
        if hasattr(p, a):
            return getattr(p, a)
    raise AttributeError(f"Process thiếu thuộc tính '{name}' (đã thử {ALIASES[name]})")


def norm(p):
    """Process (kiểu bất kỳ) -> đối tượng chuẩn chỉ đọc."""
    return SimpleNamespace(**{k: attr(p, k) for k in ALIASES})


def engine_fn(algo):
    for name in ENGINE_NAMES[algo]:
        fn = getattr(SchedulerEngine, name, None)
        if fn:
            return fn
    raise AttributeError(f"SchedulerEngine không có hàm nào trong {ENGINE_NAMES[algo]}")


def make(rows):
    """rows: iterable[(pid, at, bt)] -> list[Process]"""
    return [Process(p, a, b) for p, a, b in rows]


def run(algo, rows):
    """Chạy thuật toán; trả về (results chuẩn hoá, gantt list[tuple])."""
    results, gantt = engine_fn(algo)(make(rows))
    return [norm(p) for p in results], [tuple(g) for g in gantt]


def by_pid(results):
    return {p.process_id: p for p in results}


def as_tuple(p):
    """(start, completion, turnaround, waiting)"""
    return (p.start_time, p.completion_time, p.turnaround_time, p.waiting_time)


def averages(results):
    n = len(results)
    return (
        sum(p.waiting_time for p in results) / n,
        sum(p.turnaround_time for p in results) / n,
    )


def check_invariants(test, rows, results, gantt):
    """Các bất biến phải đúng với MỌI đầu vào hợp lệ."""
    at = {p: a for p, a, _ in rows}
    bt = {p: b for p, _, b in rows}
    got = by_pid(results)
    test.assertEqual(set(got), set(at), "Kết quả thiếu/thừa tiến trình")
    test.assertEqual(len(results), len(rows), "Số dòng kết quả khác số tiến trình")
    for pid, p in got.items():
        test.assertGreaterEqual(p.start_time, at[pid], f"{pid}: start < arrival")
        test.assertEqual(p.completion_time, p.start_time + bt[pid], f"{pid}: CT != ST+BT")
        test.assertEqual(p.turnaround_time, p.completion_time - at[pid], f"{pid}: TAT sai")
        test.assertEqual(p.waiting_time, p.turnaround_time - bt[pid], f"{pid}: WT sai")
        test.assertEqual(p.response_time, p.start_time - at[pid], f"{pid}: RT sai")
        test.assertGreaterEqual(p.waiting_time, 0, f"{pid}: WT âm")
    prev_end = None
    busy = 0
    for pid, s, e in gantt:
        test.assertLess(s, e, f"Đoạn Gantt rỗng/ngược: {(pid, s, e)}")
        if prev_end is not None:
            test.assertEqual(s, prev_end, f"Gantt không liên tục tại {(pid, s, e)}")
        prev_end = e
        if pid != "IDLE":
            busy += e - s
            test.assertEqual((s, e), (got[pid].start_time, got[pid].completion_time))
    test.assertEqual(busy, sum(bt.values()), "Tổng thời gian chạy trên Gantt != tổng BT")
    first_at = min(at.values())
    test.assertEqual(gantt[0][1], 0, "Gantt phải bắt đầu từ t=0")
    if first_at > 0:
        test.assertEqual(gantt[0][0], "IDLE", "Chưa có tiến trình đến -> phải là IDLE")
    ids = [g[0] for g in gantt if g[0] != "IDLE"]
    test.assertEqual(len(ids), len(set(ids)), "Một tiến trình xuất hiện >1 đoạn (có cướp quyền?)")
