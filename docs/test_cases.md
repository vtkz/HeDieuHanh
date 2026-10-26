# TEST CASES - OS_SCH_01

## Quy ước chung

- Công thức theo `spec.md`: CT = ST + BT; TAT = CT - AT; WT = TAT - BT; RT = ST - AT.
- FCFS: AT tăng dần; nếu AT bằng nhau thì PID tăng dần.
- SJF không độc quyền (theo `spec.md`, tiến trình đang chạy không bị ngắt): chọn tiến trình đã đến có BT nhỏ nhất; nếu bằng nhau thì AT nhỏ hơn, rồi PID tăng dần.
- Các bảng kết quả sắp xếp theo PID để dễ đối chiếu. Thứ tự chạy được ghi riêng ở dòng "Thứ tự chạy".

## Tiêu chí đánh giá

- PASS: kết quả thực tế khớp kết quả mong đợi.
- FAIL: kết quả thực tế khác kết quả mong đợi.
- BLOCKED: chưa thể kiểm thử vì chức năng chưa có hoặc chưa tích hợp.

Chưa ghi PASS cho các trường hợp chưa chạy chương trình.

## Danh sách test case

| Mã | Trường hợp | File đầu vào |
|---|---|---|
| TC01 | Dữ liệu thông thường | data/normal.csv |
| TC02 | CPU Idle | data/cpu_idle.csv |
| TC03 | Dữ liệu không hợp lệ (AT âm, BT = 0, PID trùng) | data/invalid_data.csv |
| TC04 | Nhiều tiến trình đến cùng lúc | data/same_arrival.csv |
| TC05 | Chỉ có một tiến trình | data/single_process.csv |
| TC06 | Nhiều tiến trình có BurstTime bằng nhau | data/equal_burst.csv |
| TC07 | Tiến trình đến khi CPU đang bận | data/process_during_busy.csv |
| TC08 | CSV thiếu cột | data/missing_column.csv |
| TC09 | AT hoặc BT không phải số | data/non_numeric.csv |
| TC10 | PID trống | data/empty_pid.csv |
| TC11 | CSV chỉ có dòng tiêu đề | data/header_only.csv |
| TC12 | Hiệu năng với nhiều tiến trình | Xem `test_plan.md`, mục 8 |

---

## TC01 - Dữ liệu thông thường

File đầu vào: data/normal.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,5
P2,1,3
P3,2,2
P4,4,4
```

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

Trạng thái: BLOCKED (chờ code)

---

## TC02 - CPU Idle

File đầu vào: data/cpu_idle.csv

```csv
PID,ArrivalTime,BurstTime
P1,2,3
P2,8,2
```

### FCFS và SJF không độc quyền (kết quả giống nhau)

Thứ tự chạy: P1 -> P2

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 2 | 5 | 3 | 0 | 0 |
| P2 | 8 | 10 | 2 | 0 | 0 |

Khoảng Idle: 0-2 và 5-8.

Giải thích:
- CPU Idle từ 0 đến 2 vì chưa có tiến trình đến.
- P1 chạy từ 2 đến 5.
- CPU Idle từ 5 đến 8 vì P1 đã hoàn thành và P2 chưa đến.
- P2 chạy từ 8 đến 10.

Trạng thái: BLOCKED (chờ code)

---

## TC03 - Dữ liệu không hợp lệ

File đầu vào: data/invalid_data.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,5
P2,-1,3
P3,2,0
P1,4,2
```

Các lỗi cần phát hiện:
- P2 có ArrivalTime = -1.
- P3 có BurstTime = 0.
- PID P1 bị trùng.

Kết quả mong đợi:
- Dữ liệu bị từ chối, không chạy thuật toán.
- Ứng dụng hiển thị thông báo lỗi nêu rõ lý do, không bị dừng đột ngột.
- Nên báo đủ cả 3 lỗi (cần TV4 xác nhận: báo tất cả lỗi hay chỉ lỗi đầu tiên).

Trạng thái: BLOCKED (chờ code)

---

## TC04 - Nhiều tiến trình đến cùng lúc

File đầu vào: data/same_arrival.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,4
P2,0,2
P3,0,2
```

Ghi chú:
- FCFS: AT bằng nhau nên chọn theo PID tăng dần.
- SJF: P2 và P3 có BT nhỏ hơn P1 nên chạy trước; P2 và P3 bằng BT nên P2 chạy trước theo PID.

### FCFS

Thứ tự chạy: P1 -> P2 -> P3

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 4 | 4 | 0 | 0 |
| P2 | 4 | 6 | 6 | 4 | 4 |
| P3 | 6 | 8 | 8 | 6 | 6 |

### SJF không độc quyền

Thứ tự chạy: P2 -> P3 -> P1

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 4 | 8 | 8 | 4 | 4 |
| P2 | 0 | 2 | 2 | 0 | 0 |
| P3 | 2 | 4 | 4 | 2 | 2 |

Trạng thái: BLOCKED (chờ code)

---

## TC05 - Chỉ có một tiến trình

File đầu vào: data/single_process.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,5
```

### FCFS và SJF không độc quyền (kết quả giống nhau)

Thứ tự chạy: P1

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 5 | 5 | 0 | 0 |

Trạng thái: BLOCKED (chờ code)

---

## TC06 - Nhiều tiến trình có BurstTime bằng nhau

File đầu vào: data/equal_burst.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,3
P2,1,3
P3,2,3
```

Ghi chú: tại thời điểm 3, P2 và P3 đã đến và có BT bằng nhau, SJF chọn P2 vì AT nhỏ hơn.

### FCFS và SJF không độc quyền (kết quả giống nhau)

Thứ tự chạy: P1 -> P2 -> P3

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 3 | 3 | 0 | 0 |
| P2 | 3 | 6 | 5 | 2 | 2 |
| P3 | 6 | 9 | 7 | 4 | 4 |

Trạng thái: BLOCKED (chờ code)

---

## TC07 - Tiến trình đến khi CPU đang bận

File đầu vào: data/process_during_busy.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,6
P2,2,2
P3,3,1
```

Ghi chú: P2 và P3 đến khi P1 đang chạy. CPU không ngắt P1. Tại thời điểm 6, SJF chọn P3 vì BT = 1 nhỏ hơn P2.

### FCFS

Thứ tự chạy: P1 -> P2 -> P3

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 6 | 6 | 0 | 0 |
| P2 | 6 | 8 | 6 | 4 | 4 |
| P3 | 8 | 9 | 6 | 5 | 5 |

### SJF không độc quyền

Thứ tự chạy: P1 -> P3 -> P2

| PID | ST | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 6 | 6 | 0 | 0 |
| P2 | 7 | 9 | 7 | 5 | 5 |
| P3 | 6 | 7 | 4 | 3 | 3 |

Trạng thái: BLOCKED (chờ code)

---

## TC08 - CSV thiếu cột

File đầu vào: data/missing_column.csv

```csv
PID,ArrivalTime
P1,0
P2,1
```

Kết quả mong đợi:
- Báo lỗi thiếu cột `BurstTime`.
- Không chạy thuật toán, không làm ứng dụng dừng đột ngột.

Trạng thái: BLOCKED (chờ code)

---

## TC09 - AT hoặc BT không phải số

File đầu vào: data/non_numeric.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,5
P2,abc,3
```

Kết quả mong đợi:
- Báo lỗi P2 có ArrivalTime không phải số nguyên.
- Không chạy thuật toán, không làm ứng dụng dừng đột ngột.

Trạng thái: BLOCKED (chờ code)

---

## TC10 - PID trống

File đầu vào: data/empty_pid.csv

```csv
PID,ArrivalTime,BurstTime
P1,0,5
,1,3
```

Kết quả mong đợi:
- Báo lỗi dòng 3 có PID trống.
- Không chạy thuật toán, không làm ứng dụng dừng đột ngột.

Trạng thái: BLOCKED (chờ code)

---

## TC11 - CSV chỉ có dòng tiêu đề

File đầu vào: data/header_only.csv

```csv
PID,ArrivalTime,BurstTime
```

Kết quả mong đợi:
- Báo lỗi hoặc cảnh báo không có tiến trình nào để lập lịch.
- Không làm ứng dụng dừng đột ngột.

Trạng thái: BLOCKED (chờ code)

---

## TC12 - Hiệu năng với nhiều tiến trình

Dữ liệu và cách đo: xem `test_plan.md`, mục 8.

Kết quả mong đợi:
- FCFS và SJF hoàn thành với 10, 100, 1000 và 5000 tiến trình, không lỗi.
- Ghi nhận thời gian trung bình (ms) của ít nhất 5 lần đo cho mỗi cấu hình.

Trạng thái: BLOCKED (chờ code và dữ liệu hiệu năng)