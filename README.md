# CPU SCHEDULING SIMULATOR – OS_SCH_01
## FIRST COME FIRST SERVED (FCFS) AND NON-PREEMPTIVE SHORTEST JOB FIRST (SJF) ALGORITHMS


Đồ án môn học **Hệ Điều Hành (012012500102)** – Trường Đại học Giao thông vận tải TP. Hồ Chí Minh (UTH).

- **Mã đề tài:** OS_SCH_01
- **Tên đề tài:** Mô phỏng thuật toán lập lịch CPU FCFS và SJF không độc quyền.

---

## 1. GIỚI THIỆU DỰ ÁN

Dự án xây dựng ứng dụng desktop bằng Python nhằm mô phỏng và trực quan hóa hoạt động lập lịch CPU theo hai thuật toán:

- **FCFS (First-Come, First-Served):** tiến trình đến trước được thực hiện trước.
- **SJF Non-preemptive (Shortest Job First):** tại mỗi thời điểm CPU sẵn sàng, chọn tiến trình đã đến có thời gian thực thi (Burst Time) nhỏ nhất. Tiến trình đang chạy không bị ngắt.

Ứng dụng cho phép người dùng nhập danh sách tiến trình, chọn thuật toán, xem bảng kết quả và biểu đồ Gantt, đồng thời xuất báo cáo kết quả ra file CSV.

## 2. CHỨC NĂNG CHÍNH

### 2.1. Quản lý dữ liệu tiến trình

Mỗi tiến trình gồm ba thông tin đầu vào:

| Thuộc tính | Ý nghĩa |
|---|---|
| ProcessID | Mã định danh tiến trình |
| ArrivalTime (AT) | Thời điểm tiến trình đến hệ thống |
| BurstTime (BT) | Thời gian CPU cần để thực thi tiến trình |

Người dùng có thể thêm tiến trình trực tiếp, xóa danh sách hiện tại hoặc nhập danh sách từ file CSV.

Chương trình kiểm tra dữ liệu trước khi mô phỏng:
- ProcessID không được để trống hoặc trùng lặp.
- ArrivalTime phải là số nguyên không âm.
- BurstTime phải là số nguyên dương.
- File CSV phải có đúng các cột `ProcessID,ArrivalTime,BurstTime`.

### 2.2. Mô phỏng thuật toán

Người dùng chọn FCFS hoặc SJF Non-preemptive để chạy mô phỏng. Chương trình xác định thứ tự thực thi, thời điểm bắt đầu và kết thúc của từng tiến trình; nếu chưa có tiến trình sẵn sàng, CPU được thể hiện ở trạng thái **IDLE**.

### 2.3. Hiển thị kết quả

| Ký hiệu | Ý nghĩa | Công thức |
|---|---|---|
| ST | Start Time – thời điểm bắt đầu | — |
| CT / FT | Completion / Finish Time – thời điểm hoàn thành | CT = ST + BT |
| TAT | Turnaround Time – thời gian hoàn thành quay vòng | TAT = CT − AT |
| WT | Waiting Time – thời gian chờ | WT = TAT − BT |
| RT | Response Time – thời gian đáp ứng đầu tiên | RT = ST − AT |

Với hai thuật toán không ngắt trong dự án, RT bằng WT. Ứng dụng hiển thị các giá trị trung bình WT, TAT và RT, cùng biểu đồ Gantt mô tả thứ tự thực thi và các khoảng CPU IDLE.

### 2.4. Nhập và xuất CSV

- File đầu vào mẫu: `input/input.csv`.
- Chọn **Nhập file CSV** trên giao diện để nạp dữ liệu.
- Sau khi chạy mô phỏng, chọn **Xuất file CSV** và chọn vị trí lưu.
- Báo cáo CSV gồm thông tin tiến trình, các chỉ số thời gian, các chỉ số trung bình và nhật ký các đoạn Gantt.

## 3. QUY TẮC LẬP LỊCH

### 3.1. FCFS

1. ArrivalTime nhỏ hơn được chọn trước.
2. Nếu ArrivalTime bằng nhau, ProcessID được sắp xếp tăng dần theo thứ tự từ điển.

### 3.2. SJF Non-preemptive

Tại thời điểm CPU sẵn sàng, chỉ xét các tiến trình đã đến (ArrivalTime ≤ thời điểm hiện tại). Thứ tự ưu tiên:
1. BurstTime nhỏ nhất.
2. Nếu BurstTime bằng nhau, ArrivalTime nhỏ hơn.
3. Nếu ArrivalTime cũng bằng nhau, ProcessID tăng dần theo thứ tự từ điển.

Nếu hàng đợi sẵn sàng rỗng, CPU chuyển sang IDLE đến thời điểm tiến trình tiếp theo đến. Tiến trình đã bắt đầu chạy sẽ chạy đến khi hoàn thành, không bị ngắt giữa chừng.

## 4. CÔNG NGHỆ SỬ DỤNG

- **Ngôn ngữ:** Python.
- **Giao diện desktop:** Tkinter và ttk.
- **Xử lý dữ liệu:** thư viện chuẩn `csv`, `pathlib`.
- **Trực quan hóa/biểu đồ:** Matplotlib.
- **Kiểm thử:** `unittest`.

## 5. CẤU TRÚC THƯ MỤC

```text
HeDieuHanh/
├── main.py                         # Mô hình tiến trình, FCFS, SJF và ghi báo cáo CSV
├── gui.py                          # Giao diện desktop Tkinter và biểu đồ Gantt
├── data_io.py                      # Đọc, kiểm tra và xuất dữ liệu CSV
├── input/
│   └── input.csv                   # Dữ liệu đầu vào mẫu
├── output/
│   ├── .gitkeep                    # Giữ thư mục output trong Git
│   ├── benchmark.png               # Biểu đồ benchmark
│   └── stress_benchmark.png        # Biểu đồ Stress Test
├── docs/
│   ├── pseudocode(fcfs).md         # Pseudocode FCFS
│   ├── pseudocode(sjf).md          # Pseudocode SJF
│   ├── test_cases.md               # Các trường hợp kiểm thử
│   ├── test_plan.md                # Kế hoạch và kết quả kiểm thử
│   ├── testing.md                  # Báo cáo kiểm thử và hiệu năng
│   ├── stress_results.csv          # Dữ liệu kết quả Stress Test
│   └── minh_chung/                 # Ảnh minh chứng giao diện và kiểm thử
├── tests/
│   ├── data_csv/                   # Dữ liệu CSV kiểm thử hợp lệ/không hợp lệ
│   ├── test_oracle.csv             # Bảng dữ liệu Test Oracle
│   ├── oracle_data.py              # Dữ liệu Oracle dùng trong unit test
│   ├── test_oracle_handcalc.py     # Kiểm tra kết quả với Oracle tính tay
│   ├── test_fcfs.py                # Kiểm thử FCFS
│   ├── test_sjf.py                 # Kiểm thử SJF
│   ├── test_data_io.py             # Kiểm thử đọc và kiểm tra CSV
│   ├── test_csv_report.py          # Kiểm thử báo cáo CSV
│   ├── test_integration.py         # Kiểm thử tích hợp
│   └── stress_test.py              # Script Stress Test và đo hiệu năng
├── test/
│   └── test_oracle.py              # Thư mục kiểm thử cũ được lưu trong repository
├── .gitignore
└── README.md
```

**Lưu ý về file output:** các file CSV được tạo khi chạy chương trình có thể được lưu ở vị trí do người dùng chọn. Quy tắc `.gitignore` hiện tại bỏ qua `output/*.csv`, vì vậy các file CSV trong thư mục `output/` không tự động được Git theo dõi.

## 6. YÊU CẦU MÔI TRƯỜNG VÀ CÀI ĐẶT

### 6.1. Yêu cầu

- Python 3.8 trở lên.
- Tkinter (thường được tích hợp trong bản cài Python trên Windows).
- Matplotlib.

### 6.2. Cài đặt thư viện

Mở Terminal tại thư mục gốc dự án và chạy:

```bash
python -m pip install matplotlib
```

Để sử dụng phần đo RSS bộ nhớ trong Stress Test, có thể cài thêm `psutil` (không bắt buộc):

```bash
python -m pip install psutil
```

## 7. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH 

### 7.1. Khởi động giao diện

Từ thư mục gốc dự án, chạy:

```bash
python gui.py
```

### 7.2. Các bước sử dụng

1. Nhập ProcessID, ArrivalTime và BurstTime rồi chọn **Thêm tiến trình**, hoặc chọn **Nhập file CSV**.
2. Chọn thuật toán FCFS hoặc SJF không độc quyền.
3. Chọn **Chạy mô phỏng**.
4. Quan sát bảng chỉ số thời gian, các giá trị trung bình và biểu đồ Gantt.
5. Chọn **Xuất file CSV** để lưu báo cáo.

### 7.3. Định dạng CSV đầu vào

File CSV phải có dòng tiêu đề và đúng thứ tự cột:

```csv
ProcessID,ArrivalTime,BurstTime
P1,0,7
P2,2,4
P3,4,1
P4,5,4
```

Có thể sử dụng file mẫu `input/input.csv` để thử chương trình.

## 8. KIỂM THỬ

Chạy toàn bộ unit test từ thư mục gốc:

```bash
python -m unittest discover -s tests -v
```

Chạy riêng kiểm thử Test Oracle:

```bash
python -m unittest discover -s tests -p "test_oracle_handcalc.py" -v
```

Chạy Stress Test (ví dụ):

```bash
python tests/stress_test.py --sizes 10 100 500 1000 2000 3000 --repeats 5
```

Stress Test tạo dữ liệu theo các kịch bản `random`, `simultaneous` và `sparse`, đo thời gian thực thi và kiểm tra một số bất biến của kết quả. Chi tiết phương pháp và kết quả đã ghi nhận được trình bày trong `docs/testing.md` và `docs/test_plan.md`.

**Lưu ý:** Kết quả kiểm thử trong tài liệu phản ánh lần chạy được ghi nhận tại thời điểm lập báo cáo; nên chạy lại bộ test sau khi thay đổi mã nguồn và cập nhật tài liệu nếu kết quả thay đổi.

## 9. PHÂN CÔNG THÀNH VIÊN

| Thành viên | Vai trò | Công việc phụ trách |
|---|---|---|
| **ThanhLong** | Group Leader & FCFS Dev | Thiết kế kiến trúc, cài đặt FCFS, quản lý repository Git |
| **TrongNguyen** | SJF Dev & Test Oracle | Cài đặt SJF Non-preemptive, lập bộ Test Oracle |
| **KiemDung** | GUI & Visualizer | Xây dựng giao diện desktop (`gui.py`), trực quan hóa biểu đồ Gantt |
| **BichDiem** | Data Engine | Xây dựng CSV Handler, kiểm tra dữ liệu đầu vào |
| **MinhDuy** | QA & Stress Test | Kiểm thử, Stress Test và đánh giá hiệu năng |

## 10. TÀI LIỆU TRONG REPOSITORY

- [Pseudocode FCFS](docs/pseudocode(fcfs).md)
- [Pseudocode SJF](docs/pseudocode(sjf).md)
- [Test Cases](docs/test_cases.md)
- [Test Plan](docs/test_plan.md)
- [Báo cáo kiểm thử và hiệu năng](docs/testing.md)
- [Ảnh minh chứng](docs/minh_chung/)

## 11. KHAI BÁO SỬ DỤNG AI

Nhóm khai báo có sử dụng công cụ AI Gemini để hỗ trợ định hướng thiết kế mã nguồn, xây dựng giao diện GUI và Visualizer. Các thành viên chịu trách nhiệm rà soát, kiểm tra và hoàn thiện sản phẩm trước khi nộp.
