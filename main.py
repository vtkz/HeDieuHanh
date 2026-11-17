import os
import csv
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from data_io import read_processes_csv


class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = str(process_id).strip()
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = 0


class SchedulerEngine:
    @staticmethod
    def run_fcfs(processes):
        procs = [
            Process(p.process_id, p.arrival_time, p.burst_time)
            for p in processes
        ]
        procs.sort(key=lambda p: (p.arrival_time, p.process_id))
        
        current_time = 0
        gantt_chart = []
        
        for process in procs:
            if current_time < process.arrival_time:
                gantt_chart.append(
                    ("IDLE", current_time, process.arrival_time)
                )
                current_time = process.arrival_time
                
            process.start_time = current_time
            process.completion_time = (
                process.start_time + process.burst_time
            )
            process.turnaround_time = (
                process.completion_time - process.arrival_time
            )
            process.waiting_time = (
                process.start_time - process.arrival_time
            )
            process.response_time = process.waiting_time
            
            gantt_chart.append((
                process.process_id,
                process.start_time,
                process.completion_time
            ))
            current_time = process.completion_time
            
        return procs, gantt_chart

    @staticmethod
    def run_sjf_non_preemptive(processes):
        unarrived = [
            Process(p.process_id, p.arrival_time, p.burst_time)
            for p in processes
        ]
        current_time = 0
        completed = []
        gantt_chart = []
        
        while unarrived:
            ready_queue = [
                process for process in unarrived
                if process.arrival_time <= current_time
            ]
            
            if not ready_queue:
                next_arrival = min(
                    process.arrival_time for process in unarrived
                )
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
                ready_queue = [
                    process for process in unarrived
                    if process.arrival_time <= current_time
                ]
                
            selected_process = min(
                ready_queue,
                key=lambda process: (
                    process.burst_time,
                    process.arrival_time,
                    process.process_id
                )
            )
            
            selected_process.start_time = current_time
            selected_process.completion_time = (
                selected_process.start_time + selected_process.burst_time
            )
            selected_process.turnaround_time = (
                selected_process.completion_time
                - selected_process.arrival_time
            )
            selected_process.waiting_time = (
                selected_process.start_time
                - selected_process.arrival_time
            )
            selected_process.response_time = selected_process.waiting_time
            
            gantt_chart.append((
                selected_process.process_id,
                selected_process.start_time,
                selected_process.completion_time
            ))
            current_time = selected_process.completion_time
            
            completed.append(selected_process)
            unarrived.remove(selected_process)
            
        return completed, gantt_chart


class CSVHandler:
    @staticmethod
    def read_input_csv(filepath):
        processes_data = read_processes_csv(filepath)

        processes = [
            Process(
                item["ProcessID"],
                item["ArrivalTime"],
                item["BurstTime"]
            )
            for item in processes_data
        ]

        return processes

    @staticmethod
    def write_output_csv(filepath, processes, gantt_chart, algorithm_name):
        with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            writer.writerow([f"Scheduling Report: {algorithm_name}"])
            writer.writerow([
                "ProcessID",
                "ArrivalTime",
                "BurstTime",
                "StartTime",
                "CompletionTime",
                "TurnaroundTime",
                "WaitingTime",
                "ResponseTime"
            ])
            
            total_turnaround_time = 0
            total_waiting_time = 0
            total_response_time = 0
            
            for process in processes:
                writer.writerow([
                    process.process_id,
                    process.arrival_time,
                    process.burst_time,
                    process.start_time,
                    process.completion_time,
                    process.turnaround_time,
                    process.waiting_time,
                    process.response_time
                ])

                total_turnaround_time += process.turnaround_time
                total_waiting_time += process.waiting_time
                total_response_time += process.response_time
                
            number_of_processes = len(processes) if processes else 1

            writer.writerow([])
            writer.writerow(["Summary Metrics"])
            writer.writerow([
                "AverageTurnaroundTime",
                f"{total_turnaround_time / number_of_processes:.2f}"
            ])
            writer.writerow([
                "AverageWaitingTime",
                f"{total_waiting_time / number_of_processes:.2f}"
            ])
            writer.writerow([
                "AverageResponseTime",
                f"{total_response_time / number_of_processes:.2f}"
            ])

            writer.writerow([])
            writer.writerow(["Gantt Chart Trace Log"])
            writer.writerow([
                "ProcessID",
                "StartTime",
                "CompletionTime",
                "Duration"
            ])

            for process_id, start_time, completion_time in gantt_chart:
                writer.writerow([
                    process_id,
                    start_time,
                    completion_time,
                    completion_time - start_time
                ])