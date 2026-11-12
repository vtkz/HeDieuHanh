"""Bộ mô phỏng THAM CHIẾU độc lập của QA (Test Oracle tự động).

Viết theo cách ngây thơ nhất có thể (mô phỏng từng bước đồng hồ, O(n^2), không
dùng heap/sort tinh vi) để giảm khả năng trùng lỗi với code của nhóm.
Chỉ dùng để đối chiếu, KHÔNG phải mã nguồn sản phẩm.

rows: list[(pid, arrival, burst)]
trả về: (dict pid -> (start, completion, turnaround, waiting), gantt list[(pid, s, e)])
"""

def simulate(rows, algo):
    remaining = list(rows)
    clock = 0
    out, gantt = {}, []
    while remaining:
        ready = [r for r in remaining if r[1] <= clock]
        if not ready:
            nxt = min(r[1] for r in remaining)
            gantt.append(("IDLE", clock, nxt))
            clock = nxt
            continue
        if algo == "FCFS":
            pick = min(ready, key=lambda r: (r[1], r[0]))
        else:  # SJF non-preemptive: BT, rồi AT, rồi PID
            pick = min(ready, key=lambda r: (r[2], r[1], r[0]))
        pid, at, bt = pick
        start, end = clock, clock + bt
        out[pid] = (start, end, end - at, end - at - bt)
        gantt.append((pid, start, end))
        clock = end
        remaining.remove(pick)
    return out, gantt
