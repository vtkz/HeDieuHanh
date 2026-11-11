# NỘI DUNG BÁO CÁO DỰ ÁN DÀNH CHO TV2 (TUẦN 7)
## Đề tài: Mô phỏng thuật toán lập lịch CPU - SJF Non-preemptive & FCFS

---

### PHẦN 1: BỐI CẢNH BÀI TOÁN & MÔ HÌNH HỆ THỐNG (Q1 & Q2)

#### 1. Bối cảnh bài toán lập lịch CPU (CPU Scheduling)
Trong các hệ điều hành đa nhiệm (Multitasking Operating Systems), CPU là tài nguyên quan trọng nhất nhưng có số lượng hạn chế. Tại một thời điểm, nhiều tiến trình (processes) cùng cạnh tranh để được CPU xử lý. Do đó, hệ điều hành cần một bộ điều phối CPU (CPU Scheduler) nhằm quyết định tiến trình nào trong hàng đợi sẵn sàng (Ready Queue) sẽ được cấp phát thời gian chạy CPU.

Mục tiêu chính của các thuật toán lập lịch bao gồm:
- **Tối đa hóa hiệu suất sử dụng CPU (CPU Utilization):** Giữ cho CPU luôn ở trạng thái bận rộn.
- **Tối đa hóa thông lượng (Throughput):** Hoàn thành số lượng tiến trình nhiều nhất trong một đơn vị thời gian.
- **Tối thiểu hóa thời gian chờ (Waiting Time - WT):** Giảm tổng thời gian tiến trình phải nằm trong Ready Queue.
- **Tối thiểu hóa thời gian hoàn thành (Turnaround Time - TAT):** Giảm khoảng thời gian từ lúc tiến trình vào hệ thống đến khi kết thúc.

#### 2. Mô hình toán học & Các chỉ số đánh giá
Giả sử hệ thống có tập hợp $N$ tiến trình $\mathcal{P} = \{P_1, P_2, ..., P_N\}$. Mỗi tiến trình $P_i$ được đặc tả bởi 2 thông số đầu vào:
- $AT_i$ (Arrival Time): Thời điểm tiến trình $P_i$ vào hàng đợi Ready Queue.
- $BT_i$ (Burst Time): Thời gian thực thi CPU cần thiết để $P_i$ hoàn thành.

Bộ điều phối tính toán các mốc thời gian đầu ra:
- $ST_i$ (Start Time): Thời điểm $P_i$ bắt đầu được cấp CPU.
- $CT_i$ (Completion Time): Thời điểm $P_i$ thực thi xong ($CT_i = ST_i + BT_i$).
- $TAT_i$ (Turnaround Time): Thời gian lưu lại trong hệ thống ($TAT_i = CT_i - AT_i$).
- $WT_i$ (Waiting Time): Thời gian chờ trong Ready Queue ($WT_i = ST_i - AT_i = TAT_i - BT_i$).

Các chỉ số thống kê hiệu năng hệ thống:
- **Average Waiting Time (AWT):** Tổng thời gian chờ chia cho số tiến trình.
- **Average Turnaround Time (ATAT):** Tổng thời gian hoàn thành chia cho số tiến trình.

---

### PHẦN 2: GIẢI THÍCH CHI TIẾT THUẬT TOÁN SJF NON-PREEMPTIVE

#### 1. Nguyên lý hoạt động
Thuật toán **SJF Không độc quyền (Shortest Job First - Non-preemptive)** chọn tiến trình có thời gian thực thi ngắn nhất ($BT$ nhỏ nhất) trong số các tiến trình đang có mặt tại Ready Queue để cấp CPU. 

Tính chất **Không độc quyền (Non-preemptive)** đảm bảo rằng một khi tiến trình đã nhận CPU, nó sẽ giữ CPU và chạy liên tục cho đến khi hoàn tất mà không bị tiến trình mới xuất hiện chiếm quyền (preempt).

#### 2. Quy tắc phá hòa (Tie-break Rules)
Để đảm bảo tính nhất quán và tái lập được kết quả (deterministic execution), thuật toán áp dụng quy tắc phá hòa 3 tầng chặt chẽ:
1. **Tiêu chí 1 (Chính):** Chọn tiến trình có $BT$ nhỏ nhất.
2. **Tiêu chí 2 (Tie-break 1):** Nếu nhiều tiến trình trùng $BT$, chọn tiến trình có thời gian đến $AT$ sớm hơn.
3. **Tiêu chí 3 (Tie-break 2):** Nếu trùng cả $BT$ và $AT$, chọn tiến trình có mã định danh $PID$ nhỏ hơn (theo thứ tự số/từ điển).

---

### PHẦN 3: MÃ GIẢ (PSEUDOCODE) THUẬT TOÁN SJF

```text
ALGORITHM SJF_NonPreemptive(Processes):
    Input: Danh sách N tiến trình với (PID, ArrivalTime, BurstTime)
    Output: Danh sách các tiến trình đã được lập lịch kèm (StartTime, CompletionTime, TAT, WT)

    1. Sắp xếp Processes ban đầu theo ArrivalTime tăng dần, nếu trùng thì theo PID tăng dần
    2. Completed = 0
    3. CurrentTime = 0
    4. RemainingProcesses = Copy(Processes)
    5. ScheduledResult = []

    6. WHILE Completed < N DO:
        ReadyQueue = [p IN RemainingProcesses WHERE p.ArrivalTime <= CurrentTime]

        IF ReadyQueue IS EMPTY THEN:
            CurrentTime = RemainingProcesses[0].ArrivalTime
            CONTINUE
        END IF

        SelectedProcess = FindMinProcess(ReadyQueue, Key=(BurstTime, ArrivalTime, PID))
        
        SelectedProcess.StartTime = CurrentTime
        SelectedProcess.CompletionTime = CurrentTime + SelectedProcess.BurstTime
        SelectedProcess.TurnaroundTime = SelectedProcess.CompletionTime - SelectedProcess.ArrivalTime
        SelectedProcess.WaitingTime = SelectedProcess.StartTime - SelectedProcess.ArrivalTime

        CurrentTime = SelectedProcess.CompletionTime
        Completed = Completed + 1
        Remove SelectedProcess FROM RemainingProcesses
        Append SelectedProcess TO ScheduledResult
    END WHILE

    RETURN ScheduledResult
END ALGORITHM