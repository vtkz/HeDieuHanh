ALGORITHM SJF_NonPreemptive(Processes):
    Input: Danh sách tiến trình (PID, ArrivalTime, BurstTime)
    Output: Lịch trình thực thi và các chỉ số hiệu suất

    1. Khởi tạo:
       currentTime = 0, completedCount = 0, n = Tổng số tiến trình
       Đánh dấu tất cả tiến trình là chưa hoàn thành (done = False).

    2. WHILE completedCount < n:
        a. Lọc tập ReadyQueue gồm các tiến trình thỏa mãn: p.ArrivalTime <= currentTime và p.done == False.
        b. NẾU ReadyQueue không rỗng:
            - Chọn tiến trình p tốt nhất trong ReadyQueue theo tiêu chí:
              + Burst Time nhỏ nhất.
              + Nếu trùng BT, chọn ArrivalTime nhỏ nhất.
              + Nếu trùng cả BT và AT, chọn PID nhỏ hơn.
            - p.StartTime = MAX(currentTime, p.ArrivalTime)
            - p.CompletionTime = p.StartTime + p.BurstTime
            - p.TurnaroundTime = p.CompletionTime - p.ArrivalTime
            - p.WaitingTime = p.TurnaroundTime - p.BurstTime
            - currentTime = p.CompletionTime
            - p.done = True, completedCount += 1
        c. NGƯỢC LẠI (CPU Idle, chưa có tiến trình nào đến):
            - Tìm tiến trình chưa hoàn thành có ArrivalTime nhỏ nhất trong hệ thống.
            - Cập nhật currentTime = ArrivalTime của tiến trình đó.

    3. TRẢ VỀ kết quả lập lịch.