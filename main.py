import os
import csv
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = str(pid).strip()
        self.at = int(arrival_time)
        self.bt = int(burst_time)
        
        self.st = 0   # Start Time
        self.ft = 0   # Finish Time
        self.tat = 0  # Turnaround Time = FT - AT
        self.wt = 0   # Waiting Time = ST - AT
        self.rt = 0   # Response Time = ST - AT

class SchedulerEngine:
    @staticmethod
    def run_fcfs(processes):
        """
        First-Come, First-Served (FCFS)
        Tie-breaking rule: Priority 1: Arrival Time (AT) -> Priority 2: ProcessID (alphanumeric)
        """
        procs = [Process(p.pid, p.at, p.bt) for p in processes]
        procs.sort(key=lambda p: (p.at, p.pid))
        
        current_time = 0
        gantt_chart = []
        
        for p in procs:
            if current_time < p.at:
                gantt_chart.append(("IDLE", current_time, p.at))
                current_time = p.at
                
            p.st = current_time
            p.ft = p.st + p.bt
            p.tat = p.ft - p.at
            p.wt = p.st - p.at
            p.rt = p.wt
            
            gantt_chart.append((p.pid, p.st, p.ft))
            current_time = p.ft
            
        return procs, gantt_chart

    @staticmethod
    def run_sjf_non_preemptive(processes):
       
        unarrived = [Process(p.pid, p.at, p.bt) for p in processes]
        current_time = 0
        completed = []
        gantt_chart = []
        
        while unarrived:
            ready_queue = [p for p in unarrived if p.at <= current_time]
            
            if not ready_queue:
                next_arrival = min(p.at for p in unarrived)
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                ready_queue = [p for p in unarrived if p.at <= current_time]
                
            selected = min(ready_queue, key=lambda p: (p.bt, p.at, p.pid))
            
            selected.st = current_time
            selected.ft = selected.st + selected.bt
            selected.tat = selected.ft - selected.at
            selected.wt = selected.st - selected.at
            selected.rt = selected.wt
            
            gantt_chart.append((selected.pid, selected.st, selected.ft))
            current_time = selected.ft
            
            completed.append(selected)
            unarrived.remove(selected)
            
        return completed, gantt_chart

class CSVHandler:
    @staticmethod
    def read_input_csv(filepath):
        processes = []
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} không tồn tại!")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=1):
                pid_val = row.get('ProcessID') or row.get('PID')
                at_val = row.get('ArrivalTime') or row.get('Arrival_Time')
                bt_val = row.get('BurstTime') or row.get('Burst_Time')
                
                if not pid_val or not at_val or not bt_val:
                    continue
                
                pid = str(pid_val).strip()
                try:
                    at = int(str(at_val).strip())
                    bt = int(str(bt_val).strip())
                except ValueError:
                    raise ValueError(f"Dòng {row_idx}: ArrivalTime và BurstTime phải là số nguyên!")
                    
                if at < 0:
                    raise ValueError(f"Dòng {row_idx} ({pid}): ArrivalTime phải >= 0!")
                if bt <= 0:
                    raise ValueError(f"Dòng {row_idx} ({pid}): BurstTime phải > 0!")
                processes.append(Process(pid, at, bt))
        return processes

    @staticmethod
    def write_output_csv(filepath, processes, gantt_chart, algo_name):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([f"=== SCHEDULING REPORT: {algo_name} ==="])
            writer.writerow(["ProcessID", "ArrivalTime", "BurstTime", "Start_Time", "Finish_Time", "Turnaround_Time", "Waiting_Time", "Response_Time"])
            
            tot_tat, tot_wt, tot_rt = 0, 0, 0
            for p in processes:
                writer.writerow([p.pid, p.at, p.bt, p.st, p.ft, p.tat, p.wt, p.rt])
                tot_tat += p.tat
                tot_wt += p.wt
                tot_rt += p.rt
                
            n = len(processes) if processes else 1
            writer.writerow([])
            writer.writerow(["SUMMARY METRICS"])
            writer.writerow(["Average Turnaround Time (Avg TAT)", f"{tot_tat / n:.2f}"])
            writer.writerow(["Average Waiting Time (Avg WT)", f"{tot_wt / n:.2f}"])
            writer.writerow(["Average Response Time (Avg RT)", f"{tot_rt / n:.2f}"])
            writer.writerow([])
            writer.writerow(["GANTT CHART TRACE LOG"])
            writer.writerow(["Task_ProcessID", "Start_Time", "Finish_Time", "Duration"])
            for pid, st, ft in gantt_chart:
                writer.writerow([pid, st, ft, ft - st])

class Visualizer:
    @staticmethod
    def draw_gantt_comparison(gantt_fcfs, gantt_sjf, output_image_path):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
        palette = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        pid_colors = {'IDLE': '#95a5a6'}
        
        def get_color(pid):
            if pid not in pid_colors:
                pid_colors[pid] = palette[(len(pid_colors) - 1) % len(palette)]
            return pid_colors[pid]

        for item in gantt_fcfs:
            pid, st, ft = item
            color = get_color(pid)
            ax1.barh('FCFS', ft - st, left=st, color=color, edgecolor='black', height=0.5)
            ax1.text((st + ft) / 2, 0, f"{pid}\n({st}-{ft})", ha='center', va='center', 
                     color='white' if pid != 'IDLE' else 'black', fontweight='bold', fontsize=8.5)
            
        ax1.set_title("Sơ đồ Gantt: Thuật toán FCFS (First-Come, First-Served)", fontsize=11, fontweight='bold', pad=8)
        ax1.grid(axis='x', linestyle='--', alpha=0.6)

        for item in gantt_sjf:
            pid, st, ft = item
            color = get_color(pid)
            ax2.barh('SJF Non-Preemptive', ft - st, left=st, color=color, edgecolor='black', height=0.5)
            ax2.text((st + ft) / 2, 0, f"{pid}\n({st}-{ft})", ha='center', va='center', 
                     color='white' if pid != 'IDLE' else 'black', fontweight='bold', fontsize=8.5)
            
        ax2.set_title("Sơ đồ Gantt: Thuật toán SJF Không Cướp Quyền", fontsize=11, fontweight='bold', pad=8)
        ax2.set_xlabel("Thời gian (ms)", fontsize=10, fontweight='bold')
        ax2.grid(axis='x', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_image_path, dpi=150)
        plt.close()

    @staticmethod
    def draw_performance_benchmark(output_image_path):
        import random
        sizes = [10, 50, 100, 200, 500, 1000, 2000, 3000]
        fcfs_times = []
        sjf_times = []
        
        for n in sizes:
            random.seed(42)
            procs = [Process(f"P{i}", random.randint(0, n), random.randint(1, 50)) for i in range(n)]
            
            # Measure FCFS
            t0 = time.perf_counter()
            SchedulerEngine.run_fcfs(procs)
            t1 = time.perf_counter()
            fcfs_times.append((t1 - t0) * 1000) # ms
            
            # Measure SJF
            t0 = time.perf_counter()
            SchedulerEngine.run_sjf_non_preemptive(procs)
            t1 = time.perf_counter()
            sjf_times.append((t1 - t0) * 1000) # ms

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(sizes, fcfs_times, marker='o', linewidth=2, color='#27ae60', label='FCFS - O(N log N)')
        ax.plot(sizes, sjf_times, marker='s', linewidth=2, color='#e74c3c', label='SJF Non-Preemptive - O(N^2)')
        
        ax.set_title("Đánh giá Hiệu năng & Stress Test (N = 10 đến 3000 tiến trình)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Số lượng tiến trình (N)", fontsize=11, fontweight='bold')
        ax.set_ylabel("Thời gian thực thi (ms)", fontsize=11, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_image_path, dpi=150)
        plt.close()
