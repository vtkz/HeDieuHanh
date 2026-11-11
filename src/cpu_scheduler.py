# -*- coding: utf-8 -*-
"""
Module: CPU Scheduler Core Engine
Author: TV2 (SJF & Test Oracle)
Description: Hiện thực giải thuật lập lịch SJF Non-preemptive và FCFS chuẩn theo spec.md
"""

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def sjf_non_preemptive(processes):
    """
    Thuật toán SJF Không độc quyền (Non-preemptive)
    - Sắp xếp ban đầu theo Arrival Time, sau đó đến PID.
    - Tại mỗi thời điểm currentTime, chọn tiến trình trong Ready Queue có BurstTime nhỏ nhất.
    - Áp dụng luật Tie-break:
        1. BurstTime nhỏ nhất.
        2. Nếu trùng BurstTime: ưu tiên ArrivalTime nhỏ hơn.
        3. Nếu trùng cả ArrivalTime: ưu tiên PID nhỏ hơn (xử lý số/chuỗi).
    - Xử lý trạng thái CPU Idle nếu Ready Queue rỗng.
    """
    procs = sorted(processes, key=lambda x: (x.arrival_time, x.pid))
    n = len(procs)
    
    completed = 0
    current_time = 0
    remaining = procs.copy()
    result = []
    
    while completed < n:
        # Lấy các tiến trình đã đến tại thời điểm hiện tại
        ready_queue = [p for p in remaining if p.arrival_time <= current_time]
        
        if not ready_queue:
            # CPU Idle: Nhảy thời gian đến mốc ArrivalTime tiếp theo
            current_time = remaining[0].arrival_time
            continue
            
        def tie_break_key(p):
            # Trích xuất phần số từ PID (ví dụ P1 -> 1, P2 -> 2) để so sánh chuẩn xác
            pid_num = int(''.join(filter(str.isdigit, p.pid))) if any(char.isdigit() for char in p.pid) else p.pid
            return (p.burst_time, p.arrival_time, pid_num)
            
        # Chọn tiến trình tối ưu theo thuật toán SJF và Tie-break
        selected = min(ready_queue, key=tie_break_key)
        remaining.remove(selected)
        
        selected.start_time = current_time
        selected.completion_time = current_time + selected.burst_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.start_time - selected.arrival_time
        
        current_time = selected.completion_time
        completed += 1
        result.append(selected)
        
    return result

def fcfs(processes):
    """Thuật toán FCFS (Đến trước phục vụ trước)"""
    procs = sorted(processes, key=lambda x: (x.arrival_time, x.pid))
    n = len(procs)
    
    completed = 0
    current_time = 0
    remaining = procs.copy()
    result = []
    
    while completed < n:
        ready_queue = [p for p in remaining if p.arrival_time <= current_time]
        
        if not ready_queue:
            current_time = remaining[0].arrival_time
            continue
            
        def tie_break_key(p):
            pid_num = int(''.join(filter(str.isdigit, p.pid))) if any(char.isdigit() for char in p.pid) else p.pid
            return (p.arrival_time, pid_num)
            
        selected = min(ready_queue, key=tie_break_key)
        remaining.remove(selected)
        
        selected.start_time = current_time
        selected.completion_time = current_time + selected.burst_time
        selected.turnaround_time = selected.completion_time - selected.arrival_time
        selected.waiting_time = selected.start_time - selected.arrival_time
        
        current_time = selected.completion_time
        completed += 1
        result.append(selected)
        
    return result

def calculate_performance_metrics(result_processes):
    """Tính toán các chỉ số trung bình phục vụ báo cáo và giao diện (TV1 & TV3)"""
    total_wt = sum(p.waiting_time for p in result_processes)
    total_tat = sum(p.turnaround_time for p in result_processes)
    n = len(result_processes)
    
    avg_wt = total_wt / n if n > 0 else 0
    avg_tat = total_tat / n if n > 0 else 0
    
    return {
        "Average_Waiting_Time": round(avg_wt, 2),
        "Average_Turnaround_Time": round(avg_tat, 2)
    }