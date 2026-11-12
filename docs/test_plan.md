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
| data/perf_200.csv | 200 tiến trình, kiểm thử giao diện với dữ liệu lớn (tạo bằng tests/make_big_csv.py) | IT14 |

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
- Sau khi code được tích hợp, TC01 đến TC11 đã chạy: PASS. TC12 (đo hiệu năng), đang BLOCKED.
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
| TC01 | normal.csv | FCFS | P1 -> P2 -> P3 -> P4 | Khớp bảng TC01 | PASS | TV5 | 27/10/2026 | Unit test; GUI 10/11/2026 PASS |
| TC01 | normal.csv | SJF | P1 -> P3 -> P2 -> P4 | Khớp bảng TC01 | PASS | TV5 | 30/10/2026 | Unit test; GUI 10/11/2026 PASS |
| TC02 | cpu_idle.csv | FCFS, SJF | P1 -> P2; Idle 0-2 và 5-8 | Khớp | PASS | TV5 | 27/10/2026 (FCFS), 30/10/2026 (SJF) | Unit test; GUI 10/11/2026 PASS |
| TC03 | invalid_data.csv | Đọc CSV | Từ chối, báo lỗi, không crash | Hộp thoại "Dong 3: ArrivalTime phai >= 0." | PASS | TV5 | 10/11/2026 | Chỉ báo lỗi đầu tiên (BUG07). BT = 0 và trùng ProcessID kiểm riêng bằng integration test: PASS |
| TC04 | same_arrival.csv | FCFS | P1 -> P2 -> P3 | Khớp bảng TC04 | PASS | TV5 | 27/10/2026 | Unit test; GUI 10/11/2026 PASS |
| TC04 | same_arrival.csv | SJF | P2 -> P3 -> P1 | Khớp bảng TC04 | PASS | TV5 | 30/10/2026 | Unit test; GUI 10/11/2026 PASS |
| TC05 | single_process.csv | FCFS | P1; CT = 5, TAT = 5, WT = 0, RT = 0 | Khớp (unit test và GUI EC07) | PASS | TV5 | 10/11/2026 | |
| TC05 | single_process.csv | SJF | P1; CT = 5, TAT = 5, WT = 0, RT = 0 | Khớp | PASS | TV5 | 30/10/2026 | Unit test |
| TC06 | equal_burst.csv | FCFS | P1 -> P2 -> P3 | Khớp | PASS | TV5 | 10/11/2026 | Unit test |
| TC06 | equal_burst.csv | SJF | P2 -> P3 -> P1 | Khớp | PASS | TV5 | 30/10/2026 | Unit test |
| TC07 | process_during_busy.csv | FCFS | P1 -> P2 -> P3 | Khớp | PASS | TV5 | 10/11/2026 | Unit test |
| TC07 | process_during_busy.csv | SJF | P1 -> P3 -> P2 | Khớp | PASS | TV5 | 30/10/2026 | Unit test |
| TC08 | missing_column.csv | Đọc CSV | Báo thiếu cột | Hộp thoại "Tieu de CSV phai la: ProcessID,ArrivalTime,BurstTime." | PASS | TV5 | 10/11/2026 | BUG02 đã sửa ở nhánh diem; xem BUG08 |
| TC09 | non_numeric.csv | Đọc CSV | Báo AT không phải số | Hộp thoại "Dong 3: ArrivalTime va BurstTime phai la so nguyen." | PASS | TV5 | 10/11/2026 | BUG01 đã sửa; xem BUG08 |
| TC10 | empty_pid.csv | Đọc CSV | Báo ProcessID trống | Hộp thoại "Dong 3: ProcessID khong duoc de trong." | PASS | TV5 | 10/11/2026 | BUG02 đã sửa ở nhánh diem |
| TC11 | header_only.csv | Đọc CSV | Báo không có tiến trình | Hộp thoại "File CSV khong co tien trinh hop le." | PASS | TV5 | 10/11/2026 | |
| TC12 | perf_*.csv | FCFS, SJF | Hoàn thành, ghi thời gian | | BLOCKED | | | Đã có tests/stress_test.py; chờ chạy trên máy TV5 |

## 14. Bảng ghi lỗi

| Mã lỗi | Test case | Mô tả lỗi | Mức độ | Người phụ trách sửa | Trạng thái | Kết quả kiểm tra lại |
|---|---|---|---|---|---|---|
| BUG01 | TC03, TC09 | CSVHandler đọc cột `Arrival_Time` và `Burst_Time`, trong khi spec dùng `ArrivalTime` và `BurstTime`; file CSV theo spec bị bỏ qua mọi dòng mà không báo lỗi | Cao | TV1 | Đã sửa | TC03, TC09 PASS ngày 30/10/2026 |
| BUG02 | TC08, TC10 | Thiếu cột hoặc ProcessID trống: code `continue` bỏ qua dòng thay vì báo lỗi (spec mục 9 yêu cầu từ chối) | Cao | TV1 | Đã sửa ở nhánh diem, chờ merge | TC08, TC10 PASS trên GUI ngày 10/11/2026; main.py của nhánh test và testnhungkhongviettat vẫn lỗi |
| BUG03 | TC03 | Không kiểm tra ProcessID trùng (spec mục 9) | Trung bình | TV1 | Đã sửa ở nhánh diem, chờ merge | Integration test (bad_duplicate_pid.csv, bad_zero_bt.csv) PASS ngày 10/11/2026 |
| BUG04 | Tích hợp | Có 3 kiểu main.py khác tên thuộc tính và hàm (pid/st/ft; finish_time; run_first_come_first_served). Chỉ bản nhánh diem khớp gui.py trên main; dùng bản khác thì GUI báo AttributeError khi bấm Chạy | Cao | TV1, TV2, TV4 | Mở | Cần chốt một API trước khi merge |
| BUG05 | IT11 | Chạy mô phỏng, thêm tiến trình mới rồi bấm Xuất CSV: file xuất thiếu tiến trình mới (kết quả và Gantt cũ không bị xóa) | Cao | TV3 | Mở | Xác nhận bằng ảnh và file gui01_test.csv ngày 10/11/2026 |
| BUG06 | IT12 | Nút Xóa danh sách và Nhập CSV không xóa biểu đồ Gantt cũ, bảng và Gantt lệch nhau | Trung bình | TV3 | Mở | Xác nhận bằng ảnh ngày 10/11/2026 |
| BUG07 | TC03 | Nhập CSV chỉ báo lỗi dòng đầu tiên, không liệt kê đủ lỗi | Thấp | TV4 | Mở | Cần TV4 xác nhận chính sách báo lỗi (mục 7) |
| BUG08 | TC03, TC08, TC09, TC10, TC11 | Thông báo lỗi CSV không có dấu tiếng Việt | Thấp | TV4 | Mở | |
| BUG09 | IT14 | Với 200 tiến trình: nhãn Gantt chồng thành vệt đen, hộp thoại kết quả liệt kê toàn bộ Gantt quá lớn | Thấp | TV3 | Mở | Số liệu đúng, chỉ lỗi hiển thị |
| BUG10 | IT13 | Thu nhỏ cửa sổ: Gantt bị cắt, không co giãn, không có thanh cuộn ngang; tiêu đề cột bị cắt | Trung bình | TV3 | Mở | Xác nhận bằng ảnh ngày 10/11/2026 |

## 15. Kết quả Unit Test FCFS 

File test: `tests/test_fcfs.py`

Lệnh chạy: `python -m unittest discover -s tests -v`

Tổng: 12 test, 12 PASS, 0 FAIL (trước đó 10 PASS, 2 FAIL do BUG02).

| Test | Nội dung | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|
| test_tc01_du_lieu_thong_thuong | normal.csv | Khớp bảng TC01 | Khớp | PASS |
| test_tc02_cpu_idle | cpu_idle.csv | Khớp TC02, Idle 0-2 và 5-8 | Khớp | PASS |
| test_tc04_tien_trinh_den_cung_luc | same_arrival.csv | Khớp bảng TC04 | Khớp | PASS |
| test_oracle_Test1_Basic | Oracle của TV2 | Khớp oracle | Khớp | PASS |
| test_oracle_Test2_Idle | Oracle của TV2 | Khớp oracle | Khớp | PASS |
| test_tc03_at_am_bt_bang_0_pid_trung | invalid_data.csv | Báo lỗi ValueError | Báo ValueError | PASS (BUG01 đã sửa) |
| test_tc09_at_khong_phai_so | non_numeric.csv | Báo lỗi ValueError | Báo ValueError | PASS (BUG01 đã sửa) |
| test_tc08_thieu_cot | missing_column.csv | Báo lỗi ValueError | Báo ValueError | PASS |
| test_tc10_pid_trong | empty_pid.csv | Báo lỗi ValueError | Báo ValueError | PASS |

Các test oracle chạy 2 lần (đầu vào giữ nguyên và đảo ngược thứ tự), cả hai đều đạt.

## 16. Kết quả Unit Test SJF 

File test: `tests/test_sjf.py`

Lệnh chạy: `python tests/test_sjf.py`

Tổng: 22 test, 22 PASS, 0 FAIL.

### Góc chết (corner cases)

| Mã | Góc chết | Dữ liệu (AT, BT) | Kết quả mong đợi | Trạng thái |
|---|---|---|---|---|
| GC01 | Đến cùng lúc, BT khác nhau | P1(0,6) P2(0,2) P3(0,4) | P2 -> P3 -> P1 | PASS |
| GC02 | Đến cùng lúc, BT bằng nhau, phá hòa theo ProcessID | P3(0,3) P1(0,3) P2(0,3) | P1 -> P2 -> P3 | PASS |
| GC03 | BT bằng nhau, AT ưu tiên hơn ProcessID | P1(0,5) P2(2,3) P3(1,3) | P1 -> P3 -> P2 | PASS |
| GC04 | Chênh lệch BT lớn, không ngắt tiến trình đang chạy | P1(0,1000) P2(1,1) P3(2,1) P4(3,2) | P1 -> P2 -> P3 -> P4 | PASS |
| GC05 | BT cực lớn (10^9) | P1(0,10^9) P2(0,1) | P2 -> P1 | PASS |
| GC06 | Đến đúng lúc CPU rảnh | P1(0,4) P2(4,2) P3(4,1) | P1 -> P3 -> P2 | PASS |
| GC07 | Đến sau CPU rảnh 1 đơn vị | P1(0,4) P2(5,1) | P1, Idle 4-5, P2 | PASS |
| GC08 | CPU Idle đầu và giữa | P1(3,2) P2(10,1) | Idle 0-3, P1, Idle 5-10, P2 | PASS |
| GC09 | Một tiến trình | P1(0,5) | P1 | PASS |
| GC10 | Danh sách rỗng | (không có) | Không lỗi, kết quả rỗng | PASS |
| GC11 | 5 tiến trình đến cùng lúc, BT giảm dần | P1(0,5) ... P5(0,1) | P5 -> P4 -> P3 -> P2 -> P1 | PASS |
| GC12 | 300 bộ ngẫu nhiên (seed 2026), BT từ 1 đến 5000 | Ngẫu nhiên | Đúng quy tắc SJF | PASS |

### Dữ liệu mẫu và oracle

| Test | Nội dung | Trạng thái |
|---|---|---|
| test_tc01, test_tc02, test_tc04, test_tc05, test_tc06, test_tc07 | Dữ liệu trong `data/` so với bảng SJF trong `test_cases.md` | PASS |
| test_oracle_Test1_Basic, Test2_Idle, Test3_TieBreak | Đối chiếu oracle của TV2 | PASS |

## 17. KẾ HOẠCH KIỂM THỬ  – KIỂM THỬ TÍCH HỢP
### 17.1. Mục tiêu kiểm thử tích hợp

- Kiểm tra sự kết nối giữa giao diện GUI và bộ xử lý thuật toán FCFS, SJF.
- Kiểm tra dữ liệu nhập thủ công được truyền chính xác đến thuật toán.
- Kiểm tra chức năng Import CSV và Export CSV trên giao diện.
- Kiểm tra tính chính xác của bảng kết quả và biểu đồ Gantt.
- Kiểm tra khả năng xử lý dữ liệu đầu vào không hợp lệ.
- Đảm bảo giao diện hoạt động ổn định khi người dùng thao tác.

### 17.2. Danh sách kiểm thử tích hợp

| Mã | Nội dung kiểm thử | Kết quả mong đợi | Trạng thái | Ghi chú |
|---|---|---|---|---|
| IT01 | Khởi động GUI | Giao diện hiển thị bình thường | PASS | 10/11/2026 |
| IT02 | Chạy FCFS trên GUI | Kết quả đúng với Test Oracle | PASS | Khớp TC01, TC02, TC04; 200 tiến trình khớp mô phỏng độc lập |
| IT03 | Chạy SJF trên GUI | Kết quả đúng với Test Oracle | PASS | Như IT02 |
| IT04 | Nhập dữ liệu thủ công | Tiến trình được thêm chính xác | PASS | EC02, EC07 |
| IT05 | Import file normal.csv | Dữ liệu được hiển thị đầy đủ | PASS | "Đã nhập 4 tiến trình từ normal.csv" |
| IT06 | Export kết quả CSV | File xuất đúng cấu trúc và dữ liệu | PASS | Xuất ngay sau khi chạy: đúng; trường hợp khác xem IT11 |
| IT07 | Kiểm tra biểu đồ Gantt | Thứ tự và thời gian khớp thuật toán | PASS | Có khối IDLE (EC09) |
| IT08 | Import CSV sai định dạng | Hiển thị thông báo lỗi, không crash | PASS | TC03, TC08, TC09, TC10, TC11; dữ liệu cũ không mất |
| IT09 | Chạy với dữ liệu rỗng | Xử lý an toàn, không crash | PASS | EC06 |
| IT10 | Chuyển đổi giữa FCFS và SJF | Kết quả được cập nhật chính xác | PASS | Chạy FCFS, SJF, FCFS: kết quả không dính |
| IT11 | Thêm tiến trình sau khi chạy rồi Export | File xuất có đủ tiến trình mới | FAIL | BUG05 |
| IT12 | Xóa danh sách hoặc Import CSV mới sau khi chạy | Gantt cũ bị xóa | FAIL | BUG06 |
| IT13 | Thu nhỏ cửa sổ | Gantt và bảng co giãn, không bị cắt | FAIL | BUG10 |
| IT14 | Nạp perf_200.csv (200 tiến trình) | Không treo, số liệu đúng, Gantt đọc được | PASS | Số liệu đúng; nhãn Gantt chồng nhau (BUG09) |

### 17.3. Kiểm thử giao diện người dùng (UI Testing)

- Kiểm tra các nút chức năng có hoạt động đúng không.
- Kiểm tra các ô nhập ProcessID, ArrivalTime và BurstTime.
- Kiểm tra dữ liệu sau khi thêm hoặc xóa tiến trình.
- Kiểm tra bảng kết quả sau khi chạy thuật toán.
- Kiểm tra biểu đồ Gantt hiển thị đúng thứ tự tiến trình.
- Kiểm tra thông báo lỗi khi người dùng nhập dữ liệu không hợp lệ.
- Kiểm tra giao diện sau khi chuyển đổi giữa FCFS và SJF.

### 17.4. Kiểm thử dữ liệu đầu vào biên (Edge Input Cases)

| Mã | Trường hợp kiểm thử | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|
| EC01 | Không nhập ProcessID | Hiển thị thông báo lỗi | "Vui lòng nhập đầy đủ ProcessID, ArrivalTime và BurstTime." | PASS |
| EC02 | Nhập ProcessID trùng | Từ chối dữ liệu | "ProcessID 'P1' đã tồn tại." | PASS |
| EC03 | ArrivalTime âm | Hiển thị thông báo lỗi | "ArrivalTime phải lớn hơn hoặc bằng 0." | PASS |
| EC04 | BurstTime bằng 0 | Hiển thị thông báo lỗi | "BurstTime phải lớn hơn 0." | PASS |
| EC05 | Nhập dữ liệu không phải số | Hiển thị thông báo lỗi | "ArrivalTime và BurstTime phải là số nguyên." (thử `abc` và `1.25`) | PASS |
| EC06 | Không nhập tiến trình nào | Không crash ứng dụng | "Vui lòng thêm tiến trình hoặc nhập file CSV trước." | PASS |
| EC07 | Chỉ có một tiến trình | Hiển thị kết quả chính xác | FCFS và SJF: CT = 5, TAT = 5, WT = 0, RT = 0 | PASS |
| EC08 | Nhiều tiến trình đến cùng lúc | Xử lý đúng quy tắc Tie-break | FCFS: P1, P2, P3; SJF: P2, P3, P1 | PASS |
| EC09 | Có khoảng thời gian CPU Idle | Gantt Chart hiển thị khoảng Idle | Hai khối IDLE ở 0-2 và 5-8 | PASS |
| EC10 | File CSV thiếu cột dữ liệu | Hiển thị thông báo lỗi | "Tieu de CSV phai la: ProcessID,ArrivalTime,BurstTime." | PASS |

### 17.5. Phương pháp đánh giá

- PASS: Chức năng hoạt động đúng với kết quả mong đợi.
- FAIL: Chức năng hoạt động sai, hiển thị kết quả không chính xác hoặc phát sinh lỗi.
- BLOCKED: Chưa thể thực hiện kiểm thử do chức năng chưa được tích hợp hoặc chưa sẵn sàng.

Mỗi lỗi phát hiện cần được ghi nhận vào mục 14 – Bảng ghi lỗi và chuyển cho thành viên phụ trách để xử lý.

### 17.6. Kết quả kiểm thử

- Integration test tự động: `python -m unittest discover -s tests -v`, 83 test OK, 2 expected failures (BUG05, BUG06 còn tồn tại).
- Kiểm thử tích hợp IT01 đến IT14: 11 PASS, 3 FAIL (IT11, IT12, IT13).
- Edge input EC01 đến EC10: 10 PASS.
- Lỗi mới: BUG04 đến BUG10 (2 lỗi mức Cao: BUG04, BUG05).
- Kết luận: nghiệm thu chức năng (TC01 đến TC11) đạt. Còn 4 lỗi mở chờ nhóm sửa (BUG04, BUG05, BUG06, BUG10); TC12 ở giai đoạn sau.

### 17.7. Minh chứng kiểm thử (thư mục docs/minh_chung)

#### a. Kiểm thử tự động và khởi động giao diện

| Mã | Nội dung | Ảnh |
|---|---|---|
| Unit và Integration | `python -m unittest discover -s tests -v`: 83 test OK, 2 expected failures (BUG05, BUG06) | ![](minh_chung/unittest_83_ok.png) |
| IT01 | Khởi động giao diện | ![](minh_chung/IT01_khoi_dong_GUI.png) |

#### b. Nhập dữ liệu biên (EC01 đến EC10)

| Mã | Nội dung | Ảnh |
|---|---|---|
| EC01 | Không nhập ProcessID | ![](minh_chung/EC01_thieu_du_lieu.png) |
| EC02 | ProcessID trùng | ![](minh_chung/EC02_pid_trung.png) |
| EC03 | ArrivalTime âm | ![](minh_chung/EC03_at_am.png) |
| EC04 | BurstTime bằng 0 | ![](minh_chung/EC04_bt_bang_0.png) |
| EC05 | ArrivalTime là chữ `abc` | ![](minh_chung/EC05_at_abc.png) |
| EC05 | ArrivalTime là số thực `1.25` | ![](minh_chung/EC05_at_so_thuc.png) |
| EC06 | Chạy khi chưa có tiến trình | ![](minh_chung/EC06_du_lieu_rong.png) |
| EC07 | Một tiến trình, FCFS | ![](minh_chung/EC07_FCFS.png) |
| EC07 | Một tiến trình, SJF | ![](minh_chung/EC07_SJF.png) |
| EC08 | Đến cùng lúc, FCFS (P1, P2, P3) | ![](minh_chung/EC08_FCFS.png) |
| EC08 | Đến cùng lúc, SJF (P2, P3, P1) | ![](minh_chung/EC08_SJF.png) |
| EC09 | CPU Idle, FCFS | ![](minh_chung/EC09_FCFS_idle.png) |
| EC09 | CPU Idle, SJF | ![](minh_chung/EC09_SJF_idle.png) |
| EC10 | CSV thiếu cột, dữ liệu cũ vẫn còn | ![](minh_chung/EC10_thieu_cot_giu_du_lieu_cu.png) |

#### c. Dữ liệu CSV của nhóm (TC01, TC03, TC09, TC10, TC11)

| Mã | Nội dung | Ảnh |
|---|---|---|
| TC01 | normal.csv, FCFS: P1, P2, P3, P4 | ![](minh_chung/TC01_FCFS.png) |
| TC01 | normal.csv, SJF: P1, P3, P2, P4 | ![](minh_chung/TC01_SJF.png) |
| TC03 | invalid_data.csv: chỉ báo lỗi dòng đầu (BUG07, BUG08) | ![](minh_chung/TC03_invalid_data.png) |
| TC09 | non_numeric.csv | ![](minh_chung/TC09_non_numeric.png) |
| TC10 | empty_pid.csv | ![](minh_chung/TC10_empty_pid.png) |
| TC11 | header_only.csv | ![](minh_chung/TC11_header_only.png) |

#### d. Xuất CSV và chạy lặp (IT06, IT10, EXP)

| Mã | Nội dung | Ảnh |
|---|---|---|
| EXP-3 | Xuất khi chưa chạy mô phỏng: có cảnh báo (đồng thời thấy Gantt cũ còn nguyên, BUG06) | ![](minh_chung/EXP3_xuat_khi_chua_chay.png) |
| EXP-4 | Nhập lại file vừa xuất bị từ chối vì dòng đầu là "Scheduling Report" (chỉ ghi nhận, không phải lỗi) | ![](minh_chung/EXP4_nhap_lai_file_xuat_bi_tu_choi.png) |
| IT10 | 200 tiến trình, FCFS lần 1: chờ 971.88, quay vòng 983.52 | ![](minh_chung/UIA_1_FCFS_200.png) |
| IT10 | 200 tiến trình, SJF: chờ 648.24, quay vòng 659.87 | ![](minh_chung/UIA_2_SJF_200.png) |
| IT10 | 200 tiến trình, FCFS lần 3: kết quả giống lần 1 | ![](minh_chung/UIA_3_FCFS_200.png) |

#### e. Lỗi đã phát hiện

| Mã lỗi | Mô tả | Ảnh |
|---|---|---|
| BUG05 | Bước 1: sau khi chạy, thêm P3; bảng có P3 nhưng Gantt cũ còn nguyên | ![](minh_chung/BUG05_buoc1_them_P3_gantt_cu_con.png) |
| BUG05 | Bước 2: file `gui01_test.csv` xuất ra chỉ có P1, P2, thiếu P3 | ![](minh_chung/BUG05_buoc2_file_xuat_thieu_P3.png) |
| BUG06 | Sau Xóa danh sách, bảng trống nhưng Gantt cũ vẫn còn | ![](minh_chung/BUG06_xoa_danh_sach_gantt_cu_con.png) |
| BUG09 | 200 tiến trình: nhãn Gantt chồng thành vệt, hộp thoại kết quả quá lớn | ![](minh_chung/BUG09_200_tien_trinh_SJF.png) |
| BUG10 | Trước khi thu nhỏ cửa sổ | ![](minh_chung/BUG10_truoc_khi_thu_nho.png) |
| BUG10 | Sau khi thu nhỏ: Gantt bị cắt, không có thanh cuộn | ![](minh_chung/BUG10_sau_khi_thu_nho.png) |

### 17.8. Người thực hiện

Phạm Minh Duy: Kỹ sư kiểm thử (QA/QC) và Hiệu năng.

