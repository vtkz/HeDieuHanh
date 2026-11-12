"""Sinh file CSV lớn cho TC12 / UI test:  python tests/make_big_csv.py 200   ->  data/perf_200.csv"""
import os
import random
import sys

n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
rng = random.Random(2026)
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", f"perf_{n}.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", newline="", encoding="utf-8") as f:
    f.write("ProcessID,ArrivalTime,BurstTime\n")
    for i in range(1, n + 1):
        f.write(f"P{i:05d},{rng.randint(0, n * 2)},{rng.randint(1, 20)}\n")
print("Đã tạo", out)
