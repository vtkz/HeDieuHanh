import pandas as pd
from src.cpu_scheduler import Process, sjf_non_preemptive, fcfs, calculate_performance_metrics

def run_tests():
    # Đọc file dữ liệu Test Oracle chuẩn
    df = pd.read_csv('test_oracle.csv')
    print(f"=== Đã tải thành công Test Oracle với {len(df)} dòng dữ liệu ===")
    
    # Nhóm theo từng trường hợp test và giải thuật
    grouped = df.groupby(['TestCase', 'Algorithm'])
    
    for (test_case, algo), group in grouped:
        # Tạo danh sách các tiến trình từ file test oracle
        procs = [Process(row['PID'], row['ArrivalTime'], row['BurstTime']) for _, row in group.iterrows()]
        
        # Chạy giải thuật tương ứng
        if algo == 'FCFS':
            res = fcfs(procs)
        elif algo == 'SJF':
            res = sjf_non_preemptive(procs)
        else:
            continue
            
        print(f"\n--- Đang kiểm tra: {test_case} [{algo}] ---")
        for p in res:
            expected = group[group['PID'] == p.pid].iloc[0]
            # So sánh kết quả thực tế với kỳ vọng trong Test Oracle
            print(f"PID: {p.pid} | Start: {p.start_time} (Kỳ vọng: {expected['StartTime']}) | "
                  f"Comp: {p.completion_time} (Kỳ vọng: {expected['CompletionTime']}) | "
                  f"TAT: {p.turnaround_time} (Kỳ vọng: {expected['TurnaroundTime']}) | "
                  f"WT: {p.waiting_time} (Kỳ vọng: {expected['WaitingTime']})")
        
        # In thêm thông số hiệu năng trung bình
        metrics = calculate_performance_metrics(res)
        print(f"-> Chỉ số TB: Waiting Time = {metrics['Average_Waiting_Time']}, Turnaround Time = {metrics['Average_Turnaround_Time']}")

if __name__ == '__main__':
    run_tests()