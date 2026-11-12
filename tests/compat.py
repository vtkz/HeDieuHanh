"""Lớp tương thích cho test cũ của Duy (test_fcfs.py, test_sjf.py).

Hai file đó viết cho main.py kiểu cũ (p.pid, p.at, p.bt, p.st, p.ft, p.tat, p.wt, p.rt).
Lớp này bọc SchedulerEngine thật và trả về đối tượng có ĐẦY ĐỦ cả tên cũ lẫn tên mới,
nên các test cũ chạy được trên mọi kiểu main.py mà không phải sửa nội dung.
"""
from types import SimpleNamespace

import helpers
from helpers import Process, CSVHandler, ALIASES, norm  # noqa: F401


def _wide(p):
    n = norm(p)
    d = dict(vars(n))
    for canon, names in ALIASES.items():
        for alias in names:
            d[alias] = getattr(n, canon)
    return SimpleNamespace(**d)


class SchedulerEngine:
    @staticmethod
    def run_fcfs(processes):
        res, gantt = helpers.engine_fn("FCFS")(processes)
        return [_wide(p) for p in res], gantt

    @staticmethod
    def run_sjf_non_preemptive(processes):
        res, gantt = helpers.engine_fn("SJF")(processes)
        return [_wide(p) for p in res], gantt
