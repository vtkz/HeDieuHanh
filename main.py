import os
import csv
import time
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = str(process_id).strip()
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.start_time = 0
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0

class SchedulerEngine:
    @staticmethod
    def run_first_come_first_served(processes):
        process_list = [Process(p.process_id, p.arrival_time, p.burst_time) for p in processes]
        process_list.sort(key=lambda p: (p.arrival_time, p.process_id))
        
        current_time = 0
        gantt_chart = []
        
        for process in process_list:
            if current_time < process.arrival_time:
                gantt_chart.append(("IDLE", current_time, process.arrival_time))
                current_time = process.arrival_time
                
            process.start_time = current_time
            process.finish_time = process.start_time + process.burst_time
            process.turnaround_time = process.finish_time - process.arrival_time
            process.waiting_time = process.start_time - process.arrival_time
            process.response_time = process.waiting_time
            
            gantt_chart.append((process.process_id, process.start_time, process.finish_time))
            current_time = process.finish_time
            
        return process_list, gantt_chart

    @staticmethod
    def run_shortest_job_first_non_preemptive(processes):
        unprocessed_processes = [Process(p.process_id, p.arrival_time, p.burst_time) for p in processes]
        current_time = 0
        completed_processes = []
        gantt_chart = []
        
        while unprocessed_processes:
            ready_queue = [p for p in unprocessed_processes if p.arrival_time <= current_time]
            
            if not ready_queue:
                next_arrival_time = min(p.arrival_time for p in unprocessed_processes)
                gantt_chart.append(("IDLE", current_time, next_arrival_time))
                current_time = next_arrival_time
                ready_queue = [p for p in unprocessed_processes if p.arrival_time <= current_time]
                
            selected_process = min(ready_queue, key=lambda p: (p.burst_time, p.arrival_time, p.process_id))
            
            selected_process.start_time = current_time
            selected_process.finish_time = selected_process.start_time + selected_process.burst_time
            selected_process.turnaround_time = selected_process.finish_time - selected_process.arrival_time
            selected_process.waiting_time = selected_process.start_time - selected_process.arrival_time
            selected_process.response_time = selected_process.waiting_time
            
            gantt_chart.append((selected_process.process_id, selected_process.start_time, selected_process.finish_time))
            current_time = selected_process.finish_time
            
            completed_processes.append(selected_process)
            unprocessed_processes.remove(selected_process)
            
        return completed_processes, gantt_chart

class CSVHandler:
    @staticmethod
    def read_input_csv(filepath):
        processes = []
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist!")
            
        with open(filepath, 'r', encoding='utf-8') as file_handle:
            reader = csv.DictReader(file_handle)
            for row_index, row in enumerate(reader, start=1):
                process_id_key = next((k for k in row.keys() if k in ['ProcessID', 'PID', 'process_id']), None)
                arrival_time_key = next((k for k in row.keys() if k in ['ArrivalTime', 'Arrival_Time', 'AT', 'arrival_time']), None)
                burst_time_key = next((k for k in row.keys() if k in ['BurstTime', 'Burst_Time', 'BT', 'burst_time']), None)
                
                if not process_id_key or not arrival_time_key or not burst_time_key:
                    continue
                    
                process_id = row[process_id_key].strip()
                try:
                    arrival_time = int(row[arrival_time_key].strip())
                    burst_time = int(row[burst_time_key].strip())
                except ValueError:
                    raise ValueError(f"Row {row_index}: ArrivalTime and BurstTime must be integers!")
                    
                if arrival_time < 0:
                    raise ValueError(f"Row {row_index} ({process_id}): ArrivalTime must be >= 0!")
                if burst_time <= 0:
                    raise ValueError(f"Row {row_index} ({process_id}): BurstTime must be > 0!")
                    
                processes.append(Process(process_id, arrival_time, burst_time))
        return processes

    @staticmethod
    def write_output_csv(filepath, processes, gantt_chart, algorithm_name):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', newline='', encoding='utf-8') as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow([f"=== SCHEDULING REPORT: {algorithm_name} ==="])
            writer.writerow(["ProcessID", "ArrivalTime", "BurstTime", "StartTime", "FinishTime", "TurnaroundTime", "WaitingTime", "ResponseTime"])
            
            total_turnaround_time = 0
            total_waiting_time = 0
            total_response_time = 0
            
            for process in processes:
                writer.writerow([
                    process.process_id,
                    process.arrival_time,
                    process.burst_time,
                    process.start_time,
                    process.finish_time,
                    process.turnaround_time,
                    process.waiting_time,
                    process.response_time
                ])
                total_turnaround_time += process.turnaround_time
                total_waiting_time += process.waiting_time
                total_response_time += process.response_time
                
            count = len(processes) if processes else 1
            writer.writerow([])
            writer.writerow(["SUMMARY METRICS"])
            writer.writerow(["Average Turnaround Time", f"{total_turnaround_time / count:.2f}"])
            writer.writerow(["Average Waiting Time", f"{total_waiting_time / count:.2f}"])
            writer.writerow(["Average Response Time", f"{total_response_time / count:.2f}"])
            writer.writerow([])
            writer.writerow(["GANTT CHART TRACE LOG"])
            writer.writerow(["ProcessID", "StartTime", "FinishTime", "Duration"])
            for process_id, start_time, finish_time in gantt_chart:
                writer.writerow([process_id, start_time, finish_time, finish_time - start_time])

class Visualizer:
    @staticmethod
    def draw_gantt_comparison(gantt_fcfs, gantt_sjf, output_image_path):
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5.5), sharex=True)
        palette = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
        color_map = {'IDLE': '#95a5a6'}
        
        def get_color(process_id):
            if process_id not in color_map:
                color_map[process_id] = palette[(len(color_map) - 1) % len(palette)]
            return color_map[process_id]

        for item in gantt_fcfs:
            process_id, start_time, finish_time = item
            color = get_color(process_id)
            ax1.barh('First-Come, First-Served', finish_time - start_time, left=start_time, color=color, edgecolor='black', height=0.5)
            ax1.text((start_time + finish_time) / 2, 0, f"{process_id}\n({start_time}-{finish_time})", ha='center', va='center', 
                     color='white' if process_id != 'IDLE' else 'black', fontweight='bold', fontsize=8.5)
            
        ax1.set_title("Gantt Chart: First-Come, First-Served Scheduling Algorithm", fontsize=11, fontweight='bold', pad=8)
        ax1.grid(axis='x', linestyle='--', alpha=0.6)

        for item in gantt_sjf:
            process_id, start_time, finish_time = item
            color = get_color(process_id)
            ax2.barh('Shortest Job First Non-Preemptive', finish_time - start_time, left=start_time, color=color, edgecolor='black', height=0.5)
            ax2.text((start_time + finish_time) / 2, 0, f"{process_id}\n({start_time}-{finish_time})", ha='center', va='center', 
                     color='white' if process_id != 'IDLE' else 'black', fontweight='bold', fontsize=8.5)
            
        ax2.set_title("Gantt Chart: Shortest Job First Non-Preemptive Scheduling Algorithm", fontsize=11, fontweight='bold', pad=8)
        ax2.set_xlabel("Time Units (ms)", fontsize=10, fontweight='bold')
        ax2.grid(axis='x', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_image_path, dpi=150)
        plt.close()

    @staticmethod
    def draw_performance_benchmark(output_image_path):
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        sizes = [10, 50, 100, 200, 500, 1000, 2000, 3000]
        fcfs_times = []
        sjf_times = []
        
        for sample_size in sizes:
            random.seed(42)
            processes = [Process(f"P{i}", random.randint(0, sample_size), random.randint(1, 50)) for i in range(sample_size)]
            
            timer_start = time.perf_counter()
            SchedulerEngine.run_first_come_first_served(processes)
            timer_end = time.perf_counter()
            fcfs_times.append((timer_end - timer_start) * 1000)
            
            timer_start = time.perf_counter()
            SchedulerEngine.run_shortest_job_first_non_preemptive(processes)
            timer_end = time.perf_counter()
            sjf_times.append((timer_end - timer_start) * 1000)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(sizes, fcfs_times, marker='o', linewidth=2, color='#27ae60', label='First-Come, First-Served - O(N log N)')
        ax.plot(sizes, sjf_times, marker='s', linewidth=2, color='#e74c3c', label='Shortest Job First Non-Preemptive - O(N^2)')
        
        ax.set_title("Performance Benchmark & Stress Test (N = 10 to 3000 Processes)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Number of Processes (N)", fontsize=11, fontweight='bold')
        ax.set_ylabel("Execution Time (ms)", fontsize=11, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_image_path, dpi=150)
        plt.close()


