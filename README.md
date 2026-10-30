# CPU SCHEDULING SIMULATOR (OS_SCH_01)
## FCFS & SJF NON-PREEMPTIVE ALGORITHM SIMULATION

Đồ án môn học **Hệ Điều Hành (125001)** - Trường Đại học Giao thông vận tải TP.HCM (UTH).
Đề tài: **OS_SCH_01 - Mô phỏng thuật toán lập lịch CPU FCFS và SJF Không cướp quyền**.

---

### 1. CẤU TRÚC THƯ MỤC DỰ ÁN & DANH SÁCH FILE SHORTENED

```text
OS_SCH_01_PROJECT/
├── main.py                         # Mã nguồn lõi (Process Model, FCFS/SJF Engines, Test Oracle & Benchmark)
├── gui.py                          # Giao diện Desktop GUI Tkinter nạp/xuất CSV và hiển thị kết quả
├── input.csv                       # Dữ liệu tiến trình đầu vào mẫu (ProcessID, ArrivalTime, BurstTime)
├── output_fcfs.csv                 # Kết quả xuất vết chạy và chỉ số thống kê FCFS
├── output_sjf.csv                  # Kết quả xuất vết chạy và chỉ số thống kê SJF
├── gantt.png                       # Biểu đồ thanh Gantt Chart so sánh FCFS vs SJF
├── benchmark.png                   # Đồ thị đánh giá hiệu năng Stress Test O(N log N) vs O(N^2)
├── Bao_Cao_Do_An_OS_SCH_01.docx    # Báo cáo Đồ án hoàn chỉnh 8-12 trang chuẩn định dạng UTH
└── README.md                       # Tài liệu hướng dẫn cài đặt và vận hành
```

---

### 2. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH

#### 2.1 Yêu cầu môi trường:
* Python 3.8+ 
* Thư viện phụ thuộc: `matplotlib`

Cài đặt thư viện:
```bash
pip install matplotlib
```

#### 2.2 Chạy ứng dụng Desktop GUI:
```bash
python gui.py
```
*Tính năng GUI:* Nhập tiến trình thủ công, kiểm tra bẫy lỗi dữ liệu (ArrivalTime >= 0, BurstTime > 0), nạp file `input.csv`, chọn thuật toán FCFS/SJF, hiển thị thời gian ST, FT, TAT, WT, RT và xuất báo cáo CSV.

---

### 3. QUY TẮC 

1. **Thuật toán FCFS:**
   * Ưu tiên 1: ArrivalTime nhỏ nhất.
   * Ưu tiên 2: ProcessID nhỏ nhất theo thứ tự từ điển (Alphanumeric).

2. **Thuật toán SJF Không cướp quyền:**
   * Ưu tiên 1: BurstTime nhỏ nhất.
   * Ưu tiên 2: ArrivalTime nhỏ nhất.
   * Ưu tiên 3: ProcessID nhỏ nhất theo thứ tự từ điển (Alphanumeric).

---

### 4. BẢNG PHÂN CÔNG THÀNH VIÊN & LỊCH SỬ GIT COMMIT

| Thành viên | Vai trò | Công việc phụ trách | Commit Message Mẫu |
| :--- | :--- | :--- | :--- |
| **** | Group Leader & FCFS Dev | Thiết kế kiến trúc, cài đặt FCFS, quản lý Repo Git | `feat(core): implement FCFS scheduling engine` |
| **** | SJF Dev & Test Oracle | Cài đặt SJF Non-Preemptive, lập bộ Test Oracle | `feat(core): implement SJF non-preemptive engine` |
| **** | GUI & Visualizer | Xây dựng Desktop GUI (gui.py), vẽ sơ đồ Gantt | `feat(gui): build Tkinter app and Gantt chart renderer` |
| **** | Data Engine | Xây dựng CSV Handler, kiểm tra bẫy lỗi (Validation) | `feat(data): implement CSV reader with input validation` |
| **** | QA & Stress Test | Chạy Stress Test (N=10-3000), vẽ biểu đồ hiệu năng | `test(qa): integrate Test Oracle and benchmark runner` |

---

### 5. KHAI BÁO SỬ DỤNG AI (AI USE STATEMENT)

Nhóm khai báo sử dụng công cụ AI Gemini trong định hướng thiết kế, tạo giao diện GUI và Visualizer
