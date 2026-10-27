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
        """
        Shortest Job First (SJF) Non-Preemptive
        Tie-breaking rule: Priority 1: Burst Time (BT) -> Priority 2: Arrival Time (AT) -> Priority 3: ProcessID
        """
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
                if not row.get('ProcessID') or not row.get('Arrival_Time') or not row.get('Burst_Time'):
                    continue
                pid = row['ProcessID'].strip()
                try:
                    at = int(row['Arrival_Time'].strip())
                    bt = int(row['Burst_Time'].strip())
                except ValueError:
                    raise ValueError(f"Dòng {row_idx}: AT và BT phải là số nguyên!")
                    
                if at < 0:
                    raise ValueError(f"Dòng {row_idx} ({pid}): Arrival Time phải >= 0!")
                if bt <= 0:
                    raise ValueError(f"Dòng {row_idx} ({pid}): Burst Time phải > 0!")
                processes.append(Process(pid, at, bt))
        return processes

    @staticmethod
    def write_output_csv(filepath, processes, gantt_chart, algo_name):
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([f"=== SCHEDULING REPORT: {algo_name} ==="])
            writer.writerow(["ProcessID", "Arrival_Time", "Burst_Time", "Start_Time", "Finish_Time", "Turnaround_Time", "Waiting_Time", "Response_Time"])
            
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
