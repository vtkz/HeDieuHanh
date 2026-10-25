
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
- Kiểm tra các chỉ số CT, WT, TAT và RT.
- Kiểm tra xử lý CPU Idle và các trường hợp bằng nhau.
- Kiểm tra dữ liệu CSV hợp lệ và không hợp lệ.
- Đánh giá thời gian chạy khi số lượng tiến trình tăng.

## 3. Phạm vi kiểm thử

- Kiểm tra dữ liệu đầu vào.
- Kiểm tra thứ tự thực thi tiến trình.
- Kiểm tra Gantt chart.
- Kiểm tra các chỉ số thời gian.
- Kiểm tra đọc và xuất CSV.
- Kiểm tra hiệu năng của FCFS và SJF.

## 4. Quy tắc kiểm thử

- PID không được trống hoặc trùng.
- AT phải là số nguyên không âm.
- BT phải là số nguyên dương.
- FCFS ưu tiên AT nhỏ hơn; nếu bằng nhau thì PID tăng dần.
- SJF chọn tiến trình đã đến có BT nhỏ nhất.
- Nếu BT bằng nhau, ưu tiên AT nhỏ hơn rồi PID tăng dần.
- Tiến trình đang chạy không bị ngắt.
- Nếu chưa có tiến trình sẵn sàng, CPU ở trạng thái Idle.

## 5. Danh sách kiểm thử ban đầu

| Mã | Trường hợp | Kết quả mong đợi |
|---|---|---|
| TC01 | Dữ liệu thông thường | Kết quả đúng tính tay |
| TC02 | Một tiến trình | Các chỉ số thời gian chính xác |
| TC03 | Các tiến trình đến cùng lúc | Đúng quy tắc phá hòa |
| TC04 | Các tiến trình có BT bằng nhau | SJF chọn đúng tiến trình |
| TC05 | CPU rỗi lúc bắt đầu | Ghi nhận khoảng Idle |
| TC06 | CPU rỗi giữa các tiến trình | Ghi nhận đúng khoảng Idle |
| TC07 | Tiến trình đến khi CPU bận | Không ngắt tiến trình đang chạy |
| TC08 | AT âm | Báo lỗi |
| TC09 | BT bằng 0 hoặc âm | Báo lỗi |
| TC10 | PID trống hoặc trùng | Báo lỗi |
| TC11 | CSV thiếu cột hoặc sai định dạng | Báo lỗi, không làm ứng dụng crash |
| TC12 | Nhiều tiến trình | Hoàn thành và ghi nhận thời gian chạy |

## 6. Kế hoạch kiểm tra hiệu năng

- Sử dụng cùng bộ dữ liệu khi so sánh FCFS và SJF.
- Dự kiến thử với 10, 100, 1000 và 5000 tiến trình.
- Dùng time.perf_counter() để đo thời gian thực thi.
- Chạy thử một lần trước khi đo và đo ít nhất 5 lần cho mỗi cấu hình.
- Tính thời gian trung bình theo mili giây.
- Tách thời gian thuật toán khỏi thời gian đọc CSV và vẽ giao diện.

## 7. Đối chiếu kết quả

- So sánh kết quả chương trình với kết quả tính tay.
- Kiểm tra CT = ST + BT.
- Kiểm tra TAT = CT - AT.
- Kiểm tra WT = TAT - BT.
- Kiểm tra RT = ST - AT.
- Ghi nhận kết quả PASS hoặc FAIL và mô tả lỗi.

## 8. Sản phẩm kiểm thử

- Kế hoạch kiểm thử.
- Bộ dữ liệu CSV mẫu.
- Mã nguồn Unit Test.
- Kết quả kiểm thử.
- Bảng đo hiệu năng.
- Báo cáo lỗi và minh chứng chạy chương trình.

