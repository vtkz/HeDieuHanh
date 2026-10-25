# ĐẶC TẢ YÊU CẦU DỰ ÁN (SPECIFICATION)
**Đề tài:** Mô phỏng các giải thuật lập lịch CPU (FCFS và SJF Non-preemptive)  
**Phân công thực hiện:** TV2 (SJF & Test Oracle) & TV5 (QA/QC & Kiểm thử)  
**Tài liệu tham chiếu:** Outline_HEDIEUHANH  

---

## 1. MỤC TIÊU VÀ PHẠM VI DỰ ÁN
- Xây dựng ứng dụng Desktop GUI mô phỏng trực quan tiến trình điều phối CPU.
- Hiện thực hai thuật toán:
  1. **FCFS (First-Come, First-Served):** Đến trước phục vụ trước.
  2. **SJF (Shortest Job First - Non-preemptive):** Điều phối tiến trình có thời gian thực thi ngắn nhất trước, không độc quyền (không chiếm quyền khi tiến trình đang chạy).
- Mô phỏng và hiển thị biểu đồ Gantt Chart động (trực quan hóa cả thời gian tiến trình chạy và khoảng nghỉ CPU Idle).
- Tính toán và so sánh chi tiết các thông số đo lường hiệu năng của hai thuật toán.

---

## 2. QUY TẮC ĐIỀU PHỐI VÀ TIE-BREAK (XỬ LÝ XUNG ĐỘT)
Để đảm bảo chương trình chạy nhất quán và khớp 100% với Test Oracle, hệ thống tuân theo các quy tắc sau:

### 2.1. Quy tắc Tie-break (Bẻ gãy xung đột)
- **Trường hợp 1 (FCFS hoặc SJF trùng Arrival Time):**
  - Nếu hai hoặc nhiều tiến trình đến cùng một thời điểm, ưu tiên tiến trình có `PID` nhỏ hơn theo thứ tự từ điển hoặc số (ví dụ: `P1` được chọn trước `P2`).
- **Trường hợp 2 (SJF trùng Burst Time trong Ready Queue):**
  - Khi CPU hoàn thành và cần chọn tiến trình tiếp theo trong Ready Queue, nếu có nhiều tiến trình có cùng `BurstTime` nhỏ nhất:
    - **Ưu tiên 1:** Tiến trình có `ArrivalTime` nhỏ hơn (đến sớm hơn) sẽ được chạy trước.
    - **Ưu tiên 2:** Nếu có cùng cả `BurstTime` và `ArrivalTime`, chọn tiến trình có `PID` nhỏ hơn.

### 2.2. Trạng thái CPU rảnh rỗi (CPU Idle)
- Nếu tại thời điểm hiện tại (`currentTime`) mà không có bất kỳ tiến trình nào trong hàng đợi sẵn sàng (Ready Queue):
  - CPU chuyển sang trạng thái `IDLE`.
  - Đồng hồ thời gian nhảy đến `ArrivalTime` của tiến trình tiếp theo sẽ đến.
  - Khối thời gian rảnh phải được thể hiện rõ ràng trên biểu đồ Gantt (nhãn `[IDLE]`).

---

## 3. ĐẶC TẢ DỮ LIỆU ĐẦU VÀO VÀ ĐẦU RA

### 3.1. Dữ liệu đầu vào (Input CSV)
- Định dạng tập tin: `.csv` sử dụng dấu phẩy `,` làm dấu phân cách.
- Cấu trúc gồm 3 cột bắt buộc:
  ```csv
  ProcessID,ArrivalTime,BurstTime
