### Mã giả thuật toán SJF Không độc quyền (Non-preemptive)

Input: Danh sách N tiến trình (PID, ArrivalTime, BurstTime)
Output: Bảng kết quả (StartTime, CompletionTime, TAT, WT)

1. Khởi tạo:
   - currentTime = 0
   - completed = 0
   - readyQueue = Rỗng
   - remainingProcesses = Tập hợp tất cả tiến trình

2. Lặp khi completed < N:
   a. Chuyển các tiến trình có ArrivalTime <= currentTime từ remainingProcesses vào readyQueue.
   b. Nếu readyQueue rỗng:
      - Nhảy currentTime tới ArrivalTime nhỏ nhất tiếp theo trong remainingProcesses.
      - Quay lại bước 2a.
   c. Chọn tiến trình P trong readyQueue thỏa mãn:
      - BurstTime nhỏ nhất.
      - Tie-break 1: Nếu trùng BurstTime, ưu tiên ArrivalTime nhỏ hơn.
      - Tie-break 2: Nếu trùng cả ArrivalTime, ưu tiên PID nhỏ hơn.
      - Lấy P ra khỏi readyQueue.
   d. Tính toán:
      - P.StartTime = currentTime
      - P.CompletionTime = currentTime + P.BurstTime
      - P.TAT = P.CompletionTime - P.ArrivalTime
      - P.WT = P.StartTime - P.ArrivalTime
   e. Cập nhật:
      - currentTime = P.CompletionTime
      - completed = completed + 1

3. Trả về bảng kết quả.