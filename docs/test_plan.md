# KẾ HOẠCH KIỂM THỬ - OS_SCH_01

## 1. Thông tin dự án

- Mã đề tài: OS_SCH_01
- Tên đề tài: Mô phỏng lập lịch CPU bằng FCFS và SJF không độc quyền
- Ngôn ngữ: Python
- Công cụ: Visual Studio Code
- Người phụ trách: TV5 - QA/QC và Hiệu năng

## 2. Mục tiêu kiểm thử

- Kiểm tra tính đúng đắn của thuật toán FCFS.
- Kiểm tra tính đúng đắn của thuật toán SJF không độc quyền.
- Kiểm tra các chỉ số ST, CT, WT, TAT và RT.
- Kiểm tra xử lý CPU Idle và các trường hợp bằng nhau.
- Kiểm tra dữ liệu CSV hợp lệ và không hợp lệ.
- Đánh giá thời gian chạy khi số lượng tiến trình tăng.

## 3. Phạm vi kiểm thử

Trong phạm vi:
- Kiểm tra dữ liệu đầu vào.
- Kiểm tra thứ tự thực thi tiến trình.
- Kiểm tra Gantt chart.
- Kiểm tra các chỉ số thời gian.
- Kiểm tra đọc và xuất CSV.
- Kiểm tra hiệu năng của FCFS và SJF.

Ngoài phạm vi:
- Không kiểm thử hành vi của hệ điều hành thật hoặc chuyển đổi tiến trình thực tế trên CPU.
- Không kiểm thử các thuật toán lập lịch khác ngoài FCFS và SJF không độc quyền.

## 4. Quy tắc kiểm thử

- ProcessID không được trống hoặc trùng.
- AT phải là số nguyên không âm.
- BT phải là số nguyên dương.
- FCFS ưu tiên AT nhỏ hơn; nếu bằng nhau thì ProcessID tăng dần.
- SJF chọn tiến trình đã đến có BT nhỏ nhất.
- Nếu BT bằng nhau, ưu tiên AT nhỏ hơn rồi ProcessID tăng dần.
- Tiến trình đang chạy không bị ngắt.
- Nếu chưa có tiến trình sẵn sàng, CPU ở trạng thái Idle.

## 5. Dữ liệu kiểm thử

| File | Mục đích | Test case |
|---|---|---|
| data/normal.csv | Dữ liệu thông thường, 4 tiến trình | TC01 |
| data/cpu_idle.csv | CPU rỗi lúc bắt đầu và giữa các tiến trình | TC02 |
| data/invalid_data.csv | AT âm, BT bằng 0, ProcessID trùng | TC03 |
| data/same_arrival.csv | Các tiến trình đến cùng lúc | TC04 |
| data/single_process.csv | Chỉ một tiến trình | TC05 |
| data/equal_burst.csv | BT bằng nhau, AT khác nhau | TC06 |
| data/process_during_busy.csv | Tiến trình đến khi CPU đang bận | TC07 |
| data/missing_column.csv | CSV thiếu cột BurstTime | TC08 |
| data/non_numeric.csv | AT không phải số | TC09 |
| data/empty_pid.csv | ProcessID trống | TC10 |
| data/header_only.csv | Chỉ có dòng tiêu đề | TC11 |
| data/perf_10.csv, perf_100.csv, perf_1000.csv, perf_5000.csv | Đo hiệu năng (sinh bằng script với seed cố định, tạo khi có code) | TC12 |

Yêu cầu định dạng file: dòng đầu tiên phải là dòng tiêu đề `ProcessID,ArrivalTime,BurstTime`, không có dòng trống ở đầu file.

## 6. Danh sách test case

Chi tiết dữ liệu, kết quả mong đợi và bảng số liệu nằm trong `docs/test_cases.md`.

| Mã | Trường hợp | Kết quả mong đợi |
|---|---|---|
| TC01 | Dữ liệu thông thường | Kết quả đúng tính tay |
| TC02 | CPU rỗi lúc bắt đầu và giữa các tiến trình | Ghi nhận đúng các khoảng Idle (0-2 và 5-8) |
| TC03 | AT âm, BT bằng 0, ProcessID trùng | Báo lỗi, không crash |
| TC04 | Các tiến trình đến cùng lúc | Đúng quy tắc phá hòa |
| TC05 | Một tiến trình | Các chỉ số thời gian chính xác |
| TC06 | Các tiến trình có BT bằng nhau | SJF chọn đúng tiến trình theo AT rồi ProcessID |
| TC07 | Tiến trình đến khi CPU bận | Không ngắt tiến trình đang chạy |
| TC08 | CSV thiếu cột | Báo lỗi thiếu cột, không crash |
| TC09 | AT hoặc BT không phải số | Báo lỗi, không crash |
| TC10 | ProcessID trống | Báo lỗi, không crash |
| TC11 | CSV chỉ có tiêu đề | Báo lỗi hoặc cảnh báo, không crash |
| TC12 | Nhiều tiến trình | Hoàn thành và ghi nhận thời gian chạy |

## 7. Giả định và phụ thuộc

- Quy tắc phá hòa ở mục 4 đã được ghi trong `spec.md` mục 7, nhưng cần cả nhóm xác nhận. Nếu nhóm đổi quy tắc, TC04 và TC06 phải tính lại.
- Tên "SJF không độc quyền": trong nhiều giáo trình tiếng Việt, thuật ngữ này chỉ SJF có ngắt (preemptive, còn gọi SRTF). Tuy nhiên `spec.md` mục 6 và 7 quy định tiến trình đang chạy không bị ngắt, nên toàn bộ test case trong tài liệu này tính theo quy định của `spec.md`. Cần TV1 hoặc giảng viên xác nhận; nếu đổi sang có ngắt thì TC01, TC04 và TC07 phải tính lại.
- Chính sách báo lỗi dữ liệu (báo tất cả lỗi hay chỉ lỗi đầu tiên) cần TV4 xác nhận; ảnh hưởng đến kết quả mong đợi của TC03.
- Các test case TC01 đến TC12 ở trạng thái BLOCKED cho đến khi thuật toán FCFS, SJF và phần đọc CSV được tích hợp.
- Kết quả chuẩn (tính tay) cần được TV2 đối chiếu với `test_oracle.csv`.

## 8. Kế hoạch kiểm tra hiệu năng

- Sử dụng cùng bộ dữ liệu khi so sánh FCFS và SJF.
- Dự kiến thử với 10, 100, 1000 và 5000 tiến trình.
- Dữ liệu sinh bằng script với seed cố định để có thể tái lập kết quả.
- Dùng time.perf_counter() để đo thời gian thực thi.
- Chạy thử một lần trước khi đo và đo ít nhất 5 lần cho mỗi cấu hình.
- Tính thời gian trung bình theo mili giây.
- Tách thời gian thuật toán khỏi thời gian đọc CSV và vẽ giao diện.
- Ghi rõ cấu hình máy đo (CPU, RAM, phiên bản Python).

Bảng ghi kết quả đo (điền khi có code):

| Số tiến trình | Thuật toán | Lần 1 (ms) | Lần 2 (ms) | Lần 3 (ms) | Lần 4 (ms) | Lần 5 (ms) | Trung bình (ms) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 10 | FCFS | | | | | | |
| 10 | SJF | | | | | | |
| 100 | FCFS | | | | | | |
| 100 | SJF | | | | | | |
| 1000 | FCFS | | | | | | |
| 1000 | SJF | | | | | | |
| 5000 | FCFS | | | | | | |
| 5000 | SJF | | | | | | |

## 9. Đối chiếu kết quả

- So sánh kết quả chương trình với kết quả tính tay.
- Kiểm tra CT = ST + BT.
- Kiểm tra TAT = CT - AT.
- Kiểm tra WT = TAT - BT.
- Kiểm tra RT = ST - AT.
- Ghi nhận kết quả PASS hoặc FAIL và mô tả lỗi.

## 10. Tiêu chí nghiệm thu

- Dữ liệu hợp lệ được xử lý mà không phát sinh lỗi ngoài dự kiến.
- Dữ liệu không hợp lệ phải được thông báo lỗi rõ ràng.
- FCFS và SJF phải tuân thủ quy tắc lập lịch trong spec.md.
- Kết quả CT, WT, TAT và RT phải đúng theo công thức trong đặc tả.
- Các khoảng CPU Idle phải được ghi nhận chính xác khi chưa có tiến trình sẵn sàng.
- Kết quả chương trình phải khớp với kết quả tính tay hoặc bộ kết quả chuẩn đã thống nhất.
- Kết quả kiểm thử phải được ghi lại với trạng thái PASS hoặc FAIL.
- Kết quả đo hiệu năng phải ghi rõ số lượng tiến trình, số lần chạy và thời gian trung bình.
- Mọi lỗi phát hiện được phải có mô tả và kết quả kiểm tra lại sau khi sửa.
- Nghiệm thu chức năng khi tất cả test case TC01 đến TC11 có trạng thái PASS. Nếu còn FAIL hoặc BLOCKED thì chưa nghiệm thu.

## 11. Sản phẩm kiểm thử

- Kế hoạch kiểm thử (tài liệu này).
- Danh sách test case (`docs/test_cases.md`).
- Bộ dữ liệu CSV mẫu (thư mục `data/`).
- Mã nguồn Unit Test.
- Kết quả kiểm thử (mục 13).
- Bảng đo hiệu năng (mục 8).
- Báo cáo lỗi (mục 14) và minh chứng chạy chương trình.

## 12. Phân công trách nhiệm kiểm thử

- TV5 phụ trách lập kế hoạch, xây dựng ca kiểm thử, chạy kiểm thử, ghi nhận lỗi và đo hiệu năng.
- TV1 và TV2 phụ trách thuật toán FCFS và SJF, phối hợp sửa lỗi thuật toán khi TV5 phát hiện sai lệch.
- TV3 phối hợp kiểm thử giao diện và Gantt chart.
- TV4 phối hợp kiểm thử đọc, kiểm tra và xuất dữ liệu CSV.

## 13. Bảng ghi kết quả kiểm thử

Cập nhật sau mỗi lần chạy. Trạng thái: PASS, FAIL hoặc BLOCKED.

| Mã TC | Dữ liệu vào | Thuật toán | Kết quả mong đợi (tóm tắt) | Kết quả thực tế | Trạng thái | Người chạy | Ngày | Ghi chú |
|---|---|---|---|---|---|---|---|---|
| TC01 | normal.csv | FCFS | P1 -> P2 -> P3 -> P4 | Khớp bảng TC01 | PASS | TV5 | 27/10/2026 | Unit test |
| TC01 | normal.csv | SJF | P1 -> P3 -> P2 -> P4 | | BLOCKED | | | Chờ code |
| TC02 | cpu_idle.csv | FCFS, SJF | P1 -> P2; Idle 0-2 và 5-8 | FCFS khớp; SJF chưa chạy | FCFS: PASS; SJF: BLOCKED | TV5 | 27/10/2026 | Chờ SJF |
| TC03 | invalid_data.csv | Đọc CSV | Từ chối, báo 3 lỗi, không crash | Không báo lỗi | FAIL | TV5 | 27/10/2026 | BUG01, BUG03 |
| TC04 | same_arrival.csv | FCFS | P1 -> P2 -> P3 | Khớp bảng TC04 | PASS | TV5 | 27/10/2026 | Unit test |
| TC04 | same_arrival.csv | SJF | P2 -> P3 -> P1 | | BLOCKED | | | Chờ code |
| TC05 | single_process.csv | FCFS, SJF | P1; CT = 5, TAT = 5, WT = 0, RT = 0 | | BLOCKED | | | Chờ code |
| TC06 | equal_burst.csv | FCFS, SJF | FCFS: P1 -> P2 -> P3; SJF: P2 -> P3 -> P1 | | BLOCKED | | | Chờ code |
| TC07 | process_during_busy.csv | FCFS | P1 -> P2 -> P3 | | BLOCKED | | | Chờ code |
| TC07 | process_during_busy.csv | SJF | P1 -> P3 -> P2 | | BLOCKED | | | Chờ code |
| TC08 | missing_column.csv | Đọc CSV | Báo thiếu cột BurstTime | Không báo lỗi | FAIL | TV5 | 27/10/2026 | BUG02 |
| TC09 | non_numeric.csv | Đọc CSV | Báo AT không phải số | Không báo lỗi | FAIL | TV5 | 27/10/2026 | BUG01 |
| TC10 | empty_pid.csv | Đọc CSV | Báo ProcessID trống | Không báo lỗi | FAIL | TV5 | 27/10/2026 | BUG02 |
| TC11 | header_only.csv | Đọc CSV | Báo không có tiến trình | | BLOCKED | | | Chờ code |
| TC12 | perf_*.csv | FCFS, SJF | Hoàn thành, ghi thời gian | | BLOCKED | | | Chờ code và dữ liệu |

## 14. Bảng ghi lỗi

| Mã lỗi | Test case | Mô tả lỗi | Mức độ | Người phụ trách sửa | Trạng thái | Kết quả kiểm tra lại |
|---|---|---|---|---|---|---|
| BUG01 | TC03, TC09 | CSVHandler đọc cột `Arrival_Time` và `Burst_Time`, trong khi spec dùng `ArrivalTime` và `BurstTime`; file CSV theo spec bị bỏ qua mọi dòng mà không báo lỗi | Cao | TV1 | Mở | |
| BUG02 | TC08, TC10 | Thiếu cột hoặc ProcessID trống: code `continue` bỏ qua dòng thay vì báo lỗi (spec mục 9 yêu cầu từ chối); lỗi này còn nguyên kể cả khi sửa tên cột | Cao | TV1 | Mở | |
| BUG03 | TC03 | Không kiểm tra ProcessID trùng (spec mục 9) | Trung bình | TV1 | Mở | |

## 15. Kết quả Unit Test FCFS

File test: `tests/test_fcfs.py`

Lệnh chạy: `python -m unittest discover -s tests -v`

Tổng: 12 test, 8 PASS, 4 FAIL.

| Test | Nội dung | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|
| test_tc01_du_lieu_thong_thuong | normal.csv | Khớp bảng TC01 | Khớp | PASS |
| test_tc02_cpu_idle | cpu_idle.csv | Khớp TC02, Idle 0-2 và 5-8 | Khớp | PASS |
| test_tc04_tien_trinh_den_cung_luc | same_arrival.csv | Khớp bảng TC04 | Khớp | PASS |
| test_oracle_Test1_Basic | Oracle của TV2 | Khớp oracle | Khớp | PASS |
| test_oracle_Test2_Idle | Oracle của TV2 | Khớp oracle | Khớp | PASS |
| test_tc03_at_am_bt_bang_0_pid_trung | invalid_data.csv | Báo lỗi ValueError | Không báo lỗi | FAIL (BUG01, BUG03) |
| test_tc08_thieu_cot | missing_column.csv | Báo lỗi ValueError | Không báo lỗi | FAIL (BUG02) |
| test_tc09_at_khong_phai_so | non_numeric.csv | Báo lỗi ValueError | Không báo lỗi | FAIL (BUG01) |
| test_tc10_pid_trong | empty_pid.csv | Báo lỗi ValueError | Không báo lỗi | FAIL (BUG02) |

Các test oracle chạy 2 lần (đầu vào giữ nguyên và đảo ngược thứ tự), cả hai đều đạt.