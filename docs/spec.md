
# OS_SCH_01 - FCFS và SJF không độc quyền

## 1. Thông tin dự án

- Mã đề tài: OS_SCH_01
- Tên đề tài: Mô phỏng lập lịch CPU bằng FCFS và SJF không độc quyền
- Ngôn ngữ: Python
- Môi trường phát triển: Visual Studio Code
- Nền tảng: Windows Desktop
- Nhóm: 5 thành viên

## 2. Mục tiêu

Xây dựng ứng dụng desktop cho phép người dùng nhập hoặc đọc danh sách
tiến trình, mô phỏng hai thuật toán FCFS và SJF không độc quyền,
hiển thị thứ tự thực thi, Gantt chart và các chỉ số thời gian.

Ứng dụng hỗ trợ kiểm tra dữ liệu đầu vào, xuất kết quả CSV và cung cấp
dữ liệu để kiểm thử tính đúng đắn của thuật toán.

## 3. Phạm vi

Ứng dụng bao gồm:
- Thuật toán FCFS.
- Thuật toán SJF không độc quyền.
- Đọc và kiểm tra CSV.
- Hiển thị bảng kết quả và Gantt chart.
- Tính CT, WT, TAT và RT.
- Xuất kết quả CSV.
- Kiểm thử và đánh giá hiệu năng.

Ứng dụng không mô phỏng hệ điều hành thật hoặc chuyển đổi tiến trình
thực tế trên CPU. Đây là chương trình mô phỏng thuật toán lập lịch.

## 4. Mô hình dữ liệu

Đầu vào của mỗi tiến trình:
- ProcessID: mã tiến trình.
- ArrivalTime (AT): thời điểm tiến trình đến.
- BurstTime (BT): thời gian CPU cần để chạy.

Kết quả tính toán:
- StartTime (ST): thời điểm bắt đầu chạy.
- CompletionTime (CT): thời điểm hoàn thành.
- WaitingTime (WT): thời gian chờ.
- TurnaroundTime (TAT): thời gian hoàn thành trừ thời điểm đến.
- ResponseTime (RT): thời điểm bắt đầu chạy trừ thời điểm đến.

## 5. Công thức

CT = ST + BT
TAT = CT - AT
WT = TAT - BT
RT = ST - AT

## 6. Giả định

- Chỉ có một CPU.
- Mỗi tiến trình có một đợt sử dụng CPU.
- AT là số nguyên không âm.
- BT là số nguyên dương.
- ProcessID không được trùng.
- Tiến trình đang chạy không bị ngắt giữa chừng.
- CPU ở trạng thái Idle khi chưa có tiến trình sẵn sàng.

## 7. Quy tắc chọn tiến trình

FCFS:
1. AT tăng dần.
2. Nếu AT bằng nhau, ProcessID tăng dần.
3. Nếu vẫn bằng nhau, giữ thứ tự đầu vào.

SJF không độc quyền:
1. Chỉ xét tiến trình đã đến và chưa chạy.
2. Chọn BT nhỏ nhất.
3. Nếu BT bằng nhau, AT nhỏ hơn được chọn trước.
4. Nếu vẫn bằng nhau, ProcessID tăng dần.
5. Nếu CPU không có tiến trình sẵn sàng, ghi nhận khoảng Idle.

Các quy tắc phá hòa phải được nhóm xác nhận và áp dụng nhất quán
trong code, kiểm thử và báo cáo.

## 8. Định dạng CSV đầu vào

Tên cột:
ProcessID,ArrivalTime,BurstTime

Ví dụ:
ProcessID,ArrivalTime,BurstTime
P1,0,5
P2,1,3
P3,2,2
P4,4,4

## 9. Kiểm tra dữ liệu

- Từ chối ProcessID trống hoặc trùng.
- Từ chối AT âm.
- Từ chối BT bằng 0 hoặc âm.
- Báo lỗi nếu thiếu cột hoặc dữ liệu không hợp lệ.
- Lỗi đầu vào không được làm ứng dụng bị dừng đột ngột.

## 10. Kiểm thử

Cần có các trường hợp:
- Dữ liệu thông thường.
- Chỉ một tiến trình.
- Nhiều tiến trình đến cùng lúc.
- Nhiều tiến trình có BT bằng nhau.
- CPU rỗi.
- Tiến trình đến khi CPU đang bận.
- Dữ liệu âm, bằng 0, ProcessID trùng hoặc CSV sai định dạng.

Kết quả chương trình phải được so sánh với kết quả tính tay hoặc
nguồn lý thuyết phù hợp.

## 11. Sản phẩm bàn giao

- Mã nguồn.
- Ứng dụng desktop chạy trên Windows.
- Dữ liệu CSV đầu vào và đầu ra mẫu.
- README hướng dẫn cài đặt và sử dụng.
- Bộ kiểm thử và kết quả kiểm thử.
- Báo cáo theo yêu cầu môn học.
- Video demo.
- Minh chứng đóng góp của từng thành viên.


