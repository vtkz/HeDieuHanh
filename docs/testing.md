# BÁO CÁO KIỂM THỬ VÀ ĐÁNH GIÁ HIỆU NĂNG

**Dự án:** OS_SCH_01 – FCFS và SJF không độc quyền  
**Người phụ trách:** Phạm Minh Duy (QA & Stress Test)  
**Phạm vi:** Kiểm thử FCFS, SJF; kiểm thử hiệu năng và tổng hợp kết quả đo.

## 1. Kết quả Unit Test

Theo lần chạy `python -m unittest discover -s tests -v` 

- Tổng số test được chạy: **83**.
- Kết quả cuối: `OK (expected failures=2)`.
- Có **2 expected failures** được unittest ghi nhận; đây không phải kết quả `FAILED` ngoài dự kiến.
- Cần giữ nguyên trạng thái expected failure và giải thích mục đích của từng trường hợp trong bộ test nếu báo cáo chi tiết yêu cầu.

## 2. Phương pháp Stress Test

Stress Test được thực hiện bằng script `tests/stress_test.py`.

```bash
python tests/stress_test.py --sizes 10 100 500 1000 2000 3000 --repeats 5
```

Thông số của lần chạy:

- Số lượng tiến trình: 10, 100, 500, 1.000, 2.000 và 3.000.
- Số lần đo cho mỗi cấu hình: 5.
- Kịch bản dữ liệu: `random`, `simultaneous`, `sparse`.
- Thuật toán: FCFS và SJF.
- Seed mặc định của script: 2024.
- Thời gian trong cột `time_ms` là **trung vị (median)** của 5 lần đo; `time_mean_ms` là giá trị trung bình.
- Thời gian đo thuật toán không bao gồm thời gian đọc CSV và vẽ giao diện. Việc tạo đối tượng tiến trình diễn ra trước vùng bấm giờ trong hàm đo.

## 3. Kết quả kiểm tra tính đúng

- Tổng số cấu hình: **36**.
- Cấu hình có `correct = True`: **36/36**.
- Cấu hình có `correct = False`: **0/36**.

Script kiểm tra số lượng kết quả, các công thức thời gian (CompletionTime, TurnaroundTime, WaitingTime), tính liên tục của biểu đồ Gantt và tổng thời gian CPU bận so với tổng BurstTime.

## 4. Bảng kết quả thời gian thực thi

Đơn vị: mili giây (ms). Các giá trị dưới đây lấy từ cột `time_ms` trong `output/stress_results.csv`.

| Kịch bản | Số tiến trình (N) | FCFS (ms) | SJF (ms) |
|---|---:|---:|---:|
| random | 10 | 0.010 | 0.022 |
| random | 100 | 0.079 | 0.671 |
| random | 500 | 0.605 | 14.236 |
| random | 1,000 | 1.109 | 52.260 |
| random | 2,000 | 2.052 | 217.443 |
| random | 3,000 | 3.428 | 476.823 |
| simultaneous | 10 | 0.019 | 0.026 |
| simultaneous | 100 | 0.077 | 0.953 |
| simultaneous | 500 | 0.535 | 21.617 |
| simultaneous | 1,000 | 0.714 | 88.549 |
| simultaneous | 2,000 | 2.089 | 409.302 |
| simultaneous | 3,000 | 2.757 | 882.100 |
| sparse | 10 | 0.012 | 0.038 |
| sparse | 100 | 0.084 | 0.957 |
| sparse | 500 | 0.622 | 15.293 |
| sparse | 1,000 | 0.977 | 60.562 |
| sparse | 2,000 | 2.123 | 229.555 |
| sparse | 3,000 | 4.166 | 554.253 |

## 5. Kết quả tại N = 3.000

Đây là mức dữ liệu lớn nhất trong lần chạy được báo cáo.

| Kịch bản | Thuật toán | Trung vị (ms) | Trung bình (ms) | Nhỏ nhất (ms) |
|---|---|---:|---:|---:|
| random | FCFS | 3.428 | 3.552 | 3.326 |
| random | SJF | 476.823 | 478.373 | 447.935 |
| simultaneous | FCFS | 2.757 | 3.761 | 2.361 |
| simultaneous | SJF | 882.100 | 902.945 | 826.402 |
| sparse | FCFS | 4.166 | 4.127 | 3.318 |
| sparse | SJF | 554.253 | 588.025 | 532.910 |

## 6. Ghi nhận bộ nhớ và giới hạn diễn giải CPU

Ở N = 3.000, `py_peak_mb` là bộ nhớ Python đỉnh được đo riêng bằng `tracemalloc`; `rss_mb` là RSS của tiến trình sau lượt đo bộ nhớ. Các số liệu được ghi dưới đây là số liệu của từng cấu hình trong CSV.

| Kịch bản | Thuật toán | Python peak (MB) | RSS (MB) |
|---|---|---:|---:|
| random | FCFS | 0.869 | 71.930 |
| random | SJF | 0.740 | 71.070 |
| simultaneous | FCFS | 0.836 | 72.057 |
| simultaneous | SJF | 0.833 | 70.988 |
| sparse | FCFS | 0.878 | 72.458 |
| sparse | SJF | 0.843 | 72.360 |

**Lưu ý khi diễn giải CPU:** Script lấy `cpu_ms` bằng `time.process_time()` và `time_ms` bằng `time.perf_counter()`, sau đó tính `cpu_pct = 100 × cpu_ms / time_ms`. Hai giá trị thời gian được tổng hợp riêng qua các lần đo, vì vậy tỷ lệ này có thể dao động hoặc vượt 100%. Với thời gian rất ngắn, độ phân giải của bộ đếm cũng có thể làm `cpu_ms` bằng 0. Do đó không dùng `cpu_pct` trong CSV để khẳng định mức sử dụng CPU thực tế từ Task Manager.

`py_peak_mb` được đo trong một lượt chạy riêng có bật `tracemalloc`, không phải mức RAM toàn hệ thống. `rss_mb` là RSS của tiến trình tại thời điểm lấy mẫu, không phải bộ nhớ đỉnh.

## 7. Nhận xét

- Trong cả ba kịch bản, thời gian thực thi của hai thuật toán tăng khi số lượng tiến trình tăng.
- FCFS có thời gian thực thi thấp hơn SJF rõ rệt ở các mức N lớn trong lần đo này.
- Ở N = 3.000, SJF có thời gian trung vị cao nhất trong kịch bản `simultaneous` (882,100 ms); đây là kịch bản tất cả tiến trình cùng đến tại thời điểm 0, tạo ra tập tiến trình sẵn sàng lớn.
- Kết quả kiểm tra tính đúng của script cho thấy cả 36 cấu hình đều có `correct = True`.


## 8. Kết luận và kiến nghị

Trong lần chạy được ghi nhận, Stress Test hoàn thành 36/36 cấu hình và script xác nhận kết quả đúng theo các bất biến đã cài đặt. FCFS có thời gian thực thi thấp hơn SJF trong các cấu hình đã đo, đặc biệt khi N tăng.

Có thể xem xét tối ưu cách chọn tiến trình của SJF nếu yêu cầu xử lý tập dữ liệu lớn hơn. Việc thay đổi thuật toán cần được thực hiện bởi thành viên phụ trách SJF và phải chạy lại toàn bộ bộ kiểm thử sau khi tích hợp.

## 9. Tệp minh chứng

- `tests/stress_test.py`: script sinh dữ liệu, đo thời gian, kiểm tra tính đúng và tạo biểu đồ.
- `output/stress_results.csv`: dữ liệu đo chi tiết của lần chạy này (được Git bỏ qua theo quy tắc `output/*.csv` trong `.gitignore`, trừ khi nhóm quyết định thay đổi quy tắc).
- `output/stress_benchmark.png`: biểu đồ được sinh từ lần chạy này.
- `output/benchmark.png`: bản sao biểu đồ theo tên tệp trong phân công.

**Ghi chú:** Báo cáo này tổng hợp kết quả Stress Test mới từ CSV được cung cấp và kết quả Unit Test hiển thị trên Terminal. Không thay thế nội dung `docs/test_plan.md` hoặc `docs/test_cases.md`; cần cập nhật trạng thái các tài liệu đó đồng bộ sau khi nhóm xác nhận.