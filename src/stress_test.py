# -*- coding: utf-8 -*-
"""
Module: Stress Test & Performance Comparison (Phase 6)
Author: TV2 (SJF & Test Oracle) & TV5 (QA/QC)
Description: Sinh ngẫu nhiên 100 - 10.000 tiến trình, stress test FCFS & SJF, 
             đánh giá Convoy Effect vs Starvation.
"""

import time
import random
import pandas as pd
from cpu_scheduler import Process, fcfs, sjf_non_preemptive, calculate_performance_metrics

def generate_random_processes(num_processes=1000):
    """Sinh ngẫu nhiên danh sách tiến trình với ArrivalTime và BurstTime"""
    processes = []
    for i in range(1, num_processes + 1):
        pid = f"P{i}"
        # Arrival time phân bố rải rác từ 0 đến num_processes * 2
        arrival_time = random.randint(0, num_processes * 2)
        # Burst time ngẫu nhiên từ 1 đến 50 (có thể có tiến trình rất dài để test Starvation)
        burst_time = random.randint(1, 50)
        processes.append(Process(pid, arrival_time, burst_time))
    return processes

def run_stress_test():
    print("=== BẮT ĐẦU CHẠY STRESS TEST (PHASE 6) ===")
    
    test_sizes = [100, 500, 1000, 5000, 10000]
    results = []
    
    for size in test_sizes:
        print(f"\nĐang kiểm thử với {size} tiến trình...")
        procs_fcfs = generate_random_processes(size)
        # Sao chép đúng bộ tiến trình đó cho SJF để so sánh công bằng
        procs_sjf = [Process(p.pid, p.arrival_time, p.burst_time) for p in procs_fcfs]
        
        # Đo thời gian FCFS
        start_time = time.time()
        res_fcfs = fcfs(procs_fcfs)
        time_fcfs = time.time() - start_time
        metrics_fcfs = calculate_performance_metrics(res_fcfs)
        
        # Đo thời gian SJF
        start_time = time.time()
        res_sjf = sjf_non_preemptive(procs_sjf)
        time_sjf = time.time() - start_time
        metrics_sjf = calculate_performance_metrics(res_sjf)
        
        results.append({
            "Num_Processes": size,
            "FCFS_Time(s)": round(time_fcfs, 4),
            "FCFS_Avg_WT": metrics_fcfs["Average_Waiting_Time"],
            "FCFS_Avg_TAT": metrics_fcfs["Average_Turnaround_Time"],
            "SJF_Time(s)": round(time_sjf, 4),
            "SJF_Avg_WT": metrics_sjf["Average_Waiting_Time"],
            "SJF_Avg_TAT": metrics_sjf["Average_Turnaround_Time"]
        })
        print(f"-> Hoàn thành! FCFS: {time_fcfs:.4f}s | SJF: {time_sjf:.4f}s")
        
    df_report = pd.DataFrame(results)
    print("\n================ BẢNG TỔNG KẾT KẾT QUẢ STRESS TEST ================")
    print(df_report.to_string(index=False))
    
    # Lưu báo cáo kết quả ra thư mục output
    import os
    os.makedirs('output', exist_ok=True)
    df_report.to_csv('output/stress_test_report.csv', index=False)
    print("\nĐã xuất báo cáo chi tiết ra file: output/stress_test_report.csv")

if __name__ == '__main__':
    run_stress_test()