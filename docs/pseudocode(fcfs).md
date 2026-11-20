    ALGORITHM FCFS_Scheduling(Processes):
    Input: List of processes (PID, AT, BT)
    Output: Execution order and scheduling metrics

    1. Sort Processes by AT in ascending order.
       If AT is equal, sort by PID in ascending order.

    2. Initialize:
       currentTime = 0
       completedCount = 0
       n = total number of processes

    3. FOR each process p in Processes:
        a. IF currentTime < p.AT:
              Append (IDLE, currentTime, p.AT) to Gantt Chart
              currentTime = p.AT
        b. p.ST = currentTime
        c. p.CT = p.ST + p.BT
        d. p.TAT = p.CT - p.AT
        e. p.WT = p.ST - p.AT
        f. p.RT = p.WT
        g. Append (p.PID, p.ST, p.CT) to Gantt Chart
        h. currentTime = p.CT

    4. Return scheduling results and average metrics.
