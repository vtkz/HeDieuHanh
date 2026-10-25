
# TEST CASES - OS_SCH_01

## TC01 - Dữ liệu thông thường

File đầu vào: data/normal.csv

### FCFS

Thứ tự chạy: P1 -> P2 -> P3 -> P4

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 5 | 5 | 0 | 0 |
| P2 | 5 | 8 | 7 | 4 | 4 |
| P3 | 8 | 10 | 8 | 6 | 6 |
| P4 | 10 | 14 | 10 | 6 | 6 |

### SJF không độc quyền

Thứ tự chạy: P1 -> P3 -> P2 -> P4

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 5 | 5 | 0 | 0 |
| P2 | 7 | 10 | 9 | 6 | 6 |
| P3 | 5 | 7 | 5 | 3 | 3 |
| P4 | 10 | 14 | 10 | 6 | 6 |

## TC02 - CPU Idle

File đầu vào: data/cpu_idle.csv

Thứ tự chạy của cả hai thuật toán: P1 -> P2

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 2 | 5 | 3 | 0 | 0 |
| P2 | 8 | 10 | 2 | 0 | 0 |

Khoảng Idle: 0-2 và 5-8.

## TC03 - Dữ liệu không hợp lệ

File đầu vào: data/invalid_data.csv

Các lỗi cần phát hiện:
- P2 có ArrivalTime = -1.
- P3 có BurstTime = 0.
- PID P1 bị trùng.

Kết quả mong đợi: dữ liệu bị từ chối và chương trình
hiển thị thông báo lỗi phù hợp, không bị dừng đột ngột.

## Tiêu chí đánh giá

- PASS: kết quả thực tế khớp kết quả mong đợi.
- FAIL: kết quả thực tế khác kết quả mong đợi.
- BLOCKED: chưa thể kiểm thử vì chức năng chưa có hoặc chưa tích hợp.

Chưa ghi PASS cho các trường hợp chưa chạy chương trình.
