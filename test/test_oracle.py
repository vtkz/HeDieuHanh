import csv
import os

def load_oracle_results(filename="test_oracle.csv"):
    """
    Đọc dữ liệu kết quả chuẩn (oracle) từ file CSV.
    Cấu trúc file CSV dự kiến: process_id,waiting_time,turnaround_time
    """
    oracle_data = {}
    if not os.path.exists(filename):
        return oracle_data
    
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pid = row['process_id']
            oracle_data[pid] = {
                'waiting_time': int(row['waiting_time']),
                'turnaround_time': int(row['turnaround_time'])
            }
    return oracle_data

def verify_results(actual_results, oracle_filename="test_oracle.csv"):
    """
    So sánh kết quả thực tế từ bộ mô phỏng với kết quả chuẩn từ oracle.
    """
    oracle_data = load_oracle_results(oracle_filename)
    if not oracle_data:
        print("[Thông báo] Không tìm thấy file test_oracle.py/.csv chuẩn hoặc file trống. Bỏ qua bước đối chiếu Oracle.")
        return True

    mismatch_count = 0
    for pid, actual in actual_results.items():
        if pid in oracle_data:
            expected = oracle_data[pid]
            if (actual['waiting_time'] != expected['waiting_time'] or 
                actual['turnaround_time'] != expected['turnaround_time']):
                print(f"[Sai lệch] Tiến trình {pid}: Thực tế (WT={actual['waiting_time']}, TAT={actual['turnaround_time']}) "
                      f"khác với chuẩn (WT={expected['waiting_time']}, TAT={expected['turnaround_time']})")
                mismatch_count += 1
        else:
            print(f"[Cảnh báo] Tiến trình {pid} không có trong dữ liệu Oracle.")

    if mismatch_count == 0:
        print("[Thành công] Tất cả kết quả khớp hoàn toàn với Test Oracle!")
        return True
    else:
        print(f"[Thất bại] Có {mismatch_count} tiến trình bị lệch kết quả so với Oracle.")
        return False

if __name__ == "__main__":
    # Kiểm tra nhanh khi chạy trực tiếp file
    print("Đang kiểm tra module Test Oracle...")
    data = load_oracle_results()
    print(f"Đã tải {len(data)} bản ghi chuẩn từ Oracle.")
