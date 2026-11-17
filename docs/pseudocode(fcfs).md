ALGORITHM FCFS_Scheduling(Processes):
    Input: Danh sách tiến trình, mỗi tiến trình gồm (PID, ArrivalTime, BurstTime)
    Output: Thứ tự thực thi, thời gian bắt đầu, kết thúc, Waiting Time (WT), Turnaround Time (TAT)

    1. Sắp xếp danh sách tiến trình tăng dần theo ArrivalTime (AT).
       NẾU trùng AT, sắp xếp theo thứ tự PID tăng dần (tiêu chí phá hòa).
    
    2. Khởi tạo:
       currentTime = 0
       completedCount = 0
       n = Tổng số tiến trình

    3. WHILE completedCount < n:
        a. Lấy tiến trình p đầu tiên trong hàng đợi chưa hoàn thành.
        b. NẾU currentTime < p.ArrivalTime:
            - Cập nhật currentTime = p.ArrivalTime (CPU ở trạng thái Idle chờ tiến trình đến).
        c. p.StartTime = currentTime
        d. p.CompletionTime = p.StartTime + p.BurstTime
        e. p.TurnaroundTime = p.CompletionTime - p.ArrivalTime
        f. p.WaitingTime = p.TurnaroundTime - p.BurstTime
        g. currentTime = p.CompletionTime
        h. Đánh dấu p đã hoàn thành, tăng completedCount thêm 1.

    4. TRẢ VỀ kết quả lập lịch và các chỉ số hiệu suất trung bình.