"""Stress Test + đo hiệu năng FCFS / SJF Non-preemptive

Chạy từ thư mục gốc dự án:
    python test/stress_test.py                       # N = 100..10000, mặc định
    python test/stress_test.py --sizes 100 1000 5000 --repeats 5 --seed 42
    python test/stress_test.py --max-n 3000          
    python test/stress_test.py --no-plot

Mỗi lần chạy: sinh dữ liệu ngẫu nhiên (cố định seed -> tái lập được), chạy từng
thuật toán, đo thời gian thực (median của --repeats lần), thời gian CPU, RAM
(RSS qua psutil nếu có; đỉnh bộ nhớ Python qua tracemalloc), đồng thời KIỂM TRA
TÍNH ĐÚNG (bất biến) trên chính kết quả vừa sinh ra.

Đầu ra: output/stress_results.csv, output/stress_benchmark.png (nếu có matplotlib),
và bảng Markdown in ra màn hình để dán vào báo cáo.
"""
import argparse
import csv
import math
import os
import random
import statistics
import sys
import time
import tracemalloc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import helpers  # noqa: E402
from helpers import Process, norm  # noqa: E402

try:
    import psutil
except ImportError:  # tuỳ chọn
    psutil = None

DEFAULT_SIZES = [100, 500, 1000, 2000, 5000, 10000]
SCENARIOS = {
    # AT trải đều, BT nhỏ: tải "bình thường"
    "random": lambda rng, n: [(f"P{i:05d}", rng.randint(0, n * 3), rng.randint(1, 20)) for i in range(n)],
    # Toàn bộ đến cùng lúc: hàng đợi sẵn sàng dài nhất -> xấu nhất cho SJF
    "simultaneous": lambda rng, n: [(f"P{i:05d}", 0, rng.randint(1, 1000)) for i in range(n)],
    # Thưa: nhiều đoạn IDLE
    "sparse": lambda rng, n: [(f"P{i:05d}", rng.randint(0, n * 50), rng.randint(1, 5)) for i in range(n)],
}
ALGOS = {
    "FCFS": helpers.engine_fn("FCFS"),
    "SJF": helpers.engine_fn("SJF"),
}


def verify(rows, results, gantt):
    """Kiểm tra tính đúng O(n) - trả về chuỗi lỗi hoặc None."""
    at = {p: a for p, a, _ in rows}
    bt = {p: b for p, _, b in rows}
    if len(results) != len(rows):
        return f"số kết quả {len(results)} != {len(rows)}"
    for p in map(norm, results):
        a, b = at[p.process_id], bt[p.process_id]
        if (p.start_time < a or p.completion_time != p.start_time + b
                or p.turnaround_time != p.completion_time - a
                or p.waiting_time != p.turnaround_time - b or p.waiting_time < 0):
            return f"chỉ số sai ở {p.process_id}"
    prev = 0
    busy = 0
    for pid, s, e in gantt:
        if s != prev or e <= s:
            return f"Gantt đứt/chồng tại {(pid, s, e)}"
        prev = e
        if pid != "IDLE":
            busy += e - s
    if busy != sum(bt.values()):
        return "tổng thời gian chạy != tổng BT"
    return None


def rss_mb():
    if psutil:
        return psutil.Process().memory_info().rss / 1e6
    return float("nan")


def measure(fn, rows, repeats):
    times, cpus = [], []
    results = gantt = None
    for _ in range(repeats):
        procs = [Process(p, a, b) for p, a, b in rows]
        t0, c0 = time.perf_counter(), time.process_time()
        results, gantt = fn(procs)
        times.append((time.perf_counter() - t0) * 1000)
        cpus.append((time.process_time() - c0) * 1000)
    # đo đỉnh bộ nhớ Python ở một lượt riêng (tracemalloc làm chậm nên không lẫn vào thời gian)
    procs = [Process(p, a, b) for p, a, b in rows]
    rss_before = rss_mb()
    tracemalloc.start()
    fn(procs)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss_after = rss_mb()
    med_t, med_c = statistics.median(times), statistics.median(cpus)
    return {
        "time_ms": med_t,
        "time_mean_ms": statistics.fmean(times),
        "time_min_ms": min(times),
        "runs_ms": ";".join(f"{t:.3f}" for t in times),
        "cpu_ms": med_c,
        "cpu_pct": (100.0 * med_c / med_t) if med_t > 0 else float("nan"),
        "py_peak_mb": peak / 1e6,
        "rss_mb": rss_after,
        "rss_delta_mb": rss_after - rss_before,
    }, results, gantt


def slope(n1, t1, n2, t2):
    """Hệ số mũ thực nghiệm k trong t ~ n^k (log-log). ~1 => tuyến tính, ~2 => bậc hai."""
    if min(t1, t2) <= 0:
        return float("nan")
    return math.log(t2 / t1) / math.log(n2 / n1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES)
    ap.add_argument("--max-n", type=int, default=None)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--seed", type=int, default=2024)
    ap.add_argument("--scenarios", nargs="+", default=list(SCENARIOS), choices=list(SCENARIOS))
    ap.add_argument("--no-plot", action="store_true")
    ap.add_argument("--outdir", default=os.path.join(ROOT, "output"))
    args = ap.parse_args()
    sizes = [n for n in args.sizes if args.max_n is None or n <= args.max_n]
    os.makedirs(args.outdir, exist_ok=True)

    records, failures = [], []
    print(f"Python {sys.version.split()[0]} | seed={args.seed} | repeats={args.repeats} | "
          f"psutil={'có' if psutil else 'không (RSS = nan)'}")
    for scen in args.scenarios:
        for n in sizes:
            rows = SCENARIOS[scen](random.Random(f"{args.seed}-{scen}-{n}"), n)
            for algo, fn in ALGOS.items():
                m, results, gantt = measure(fn, rows, args.repeats)
                err = verify(rows, results, gantt)
                if err:
                    failures.append((scen, n, algo, err))
                rec = {"scenario": scen, "n": n, "algo": algo, "correct": err is None, **m}
                records.append(rec)
                print(f"[{scen:12}] N={n:<6} {algo:5} {m['time_ms']:10.2f} ms  "
                      f"cpu={m['cpu_ms']:9.2f} ms  pyPeak={m['py_peak_mb']:7.2f} MB  "
                      f"{'OK' if err is None else 'SAI: ' + err}")

    csv_path = os.path.join(args.outdir, "stress_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)

    # ---- bảng Markdown cho báo cáo ----
    print("\n### Bảng kết quả Stress Test (thời gian median, ms)\n")
    print("| Kịch bản | N | FCFS (ms) | SJF (ms) | FCFS Py-peak (MB) | SJF Py-peak (MB) | Đúng |")
    print("|---|---:|---:|---:|---:|---:|:--:|")
    for scen in args.scenarios:
        for n in sizes:
            a = next(r for r in records if r["scenario"] == scen and r["n"] == n and r["algo"] == "FCFS")
            b = next(r for r in records if r["scenario"] == scen and r["n"] == n and r["algo"] == "SJF")
            ok = "✓" if a["correct"] and b["correct"] else "✗"
            print(f"| {scen} | {n} | {a['time_ms']:.2f} | {b['time_ms']:.2f} | "
                  f"{a['py_peak_mb']:.2f} | {b['py_peak_mb']:.2f} | {ok} |")

    if len(sizes) >= 2:
        print("\n### Hệ số mũ thực nghiệm k (t ≈ N^k) giữa N nhỏ nhất và lớn nhất\n")
        print("| Kịch bản | Thuật toán | k | Nhận xét |")
        print("|---|---|---:|---|")
        for scen in args.scenarios:
            for algo in ALGOS:
                rs = sorted((r for r in records if r["scenario"] == scen and r["algo"] == algo),
                            key=lambda r: r["n"])
                k = slope(rs[0]["n"], rs[0]["time_ms"], rs[-1]["n"], rs[-1]["time_ms"])
                note = "≈ tuyến tính / N log N" if k < 1.4 else ("≈ bậc hai" if k > 1.7 else "giữa N log N và N²")
                print(f"| {scen} | {algo} | {k:.2f} | {note} |")

    # ---- bảng đúng định dạng mục 8 của test_plan.md ----
    scen8 = "random" if "random" in args.scenarios else args.scenarios[0]
    print(f"\n### Bảng đo cho mục 8 test_plan.md (kịch bản {scen8}, đơn vị ms)\n")
    print("| Số tiến trình | Thuật toán | Lần 1 (ms) | Lần 2 (ms) | Lần 3 (ms) | Lần 4 (ms) | Lần 5 (ms) | Trung bình (ms) |")
    print("|---:|---|---:|---:|---:|---:|---:|---:|")
    for n in sizes:
        for algo in ALGOS:
            r = next(x for x in records if x["scenario"] == scen8 and x["n"] == n and x["algo"] == algo)
            runs = [f"{float(v):.2f}" for v in r["runs_ms"].split(";")][:5]
            runs += [""] * (5 - len(runs))
            print(f"| {n} | {algo} | " + " | ".join(runs) + f" | {r['time_mean_ms']:.2f} |")

    # ---- tài nguyên CPU / RAM ----
    print("\n### Mức chiếm dụng CPU và RAM\n")
    print("| Kịch bản | N | Thuật toán | Thời gian CPU (ms) | CPU 1 nhân (%) | RAM Python đỉnh (MB) | RSS tiến trình (MB) |")
    print("|---|---:|---|---:|---:|---:|---:|")
    big = max(sizes)
    rows = [x for x in records if x["scenario"] == scen8 or x["n"] == big]
    for r in sorted(rows, key=lambda x: (x["scenario"] != scen8, x["scenario"], x["n"], x["algo"])):
        print(f"| {r['scenario']} | {r['n']} | {r['algo']} | {r['cpu_ms']:.2f} | {r['cpu_pct']:.0f} | "
              f"{r['py_peak_mb']:.2f} | {r['rss_mb']:.1f} |")
    ncpu = os.cpu_count() or 1
    print(f"\n(Ghi chú: thuật toán chạy trên 1 luồng nên CPU 1 nhân gần 100%, tương đương khoảng "
          f"{100.0 / ncpu:.1f}% tổng CPU của máy có {ncpu} luồng logic.)")

    print(f"\nĐã ghi {csv_path}")
    if failures:
        print("\n!!! PHÁT HIỆN KẾT QUẢ SAI:")
        for fl in failures:
            print("   ", fl)

    if not args.no_plot:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, len(args.scenarios), figsize=(5 * len(args.scenarios), 4), squeeze=False)
            for ax, scen in zip(axes[0], args.scenarios):
                for algo, style in (("FCFS", "o-"), ("SJF", "s-")):
                    rs = sorted((r for r in records if r["scenario"] == scen and r["algo"] == algo),
                                key=lambda r: r["n"])
                    ax.plot([r["n"] for r in rs], [r["time_ms"] for r in rs], style, label=algo)
                ax.set_title(f"Kịch bản: {scen}")
                ax.set_xlabel("Số tiến trình N")
                ax.set_ylabel("Thời gian (ms)")
                ax.grid(True, ls="--", alpha=.5)
                ax.legend()
            fig.tight_layout()
            png = os.path.join(args.outdir, "stress_benchmark.png")
            fig.savefig(png, dpi=140)
            print(f"Đã ghi {png}")
        except ImportError:
            print("(Bỏ qua biểu đồ: chưa cài matplotlib)")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()