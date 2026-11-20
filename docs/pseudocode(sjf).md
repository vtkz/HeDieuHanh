ALGORITHM SJF_NonPreemptive(Processes):
    Input: List of processes (PID, AT, BT)
    Output: Execution schedule and scheduling metrics

    1. Initialize:
       currentTime = 0
       completedCount = 0
       n = total number of processes
       Mark all processes as not completed (done = False).

    2. WHILE completedCount < n:
        a. Build ReadyQueue containing processes where:
           p.AT <= currentTime AND p.done == False.

        b. IF ReadyQueue is not empty:
              Select process p using the following criteria:
              - Smallest BT.
              - If BT is equal, smallest AT.
              - If both BT and AT are equal, smallest PID.

              p.ST = currentTime
              p.CT = p.ST + p.BT
              p.TAT = p.CT - p.AT
              p.WT = p.ST - p.AT
              p.RT = p.WT

              Append (p.PID, p.ST, p.CT) to Gantt Chart
              currentTime = p.CT
              p.done = True
              completedCount = completedCount + 1

        c. ELSE:
              Find the unfinished process with the smallest AT.
              Append (IDLE, currentTime, minimum AT) to Gantt Chart.
              currentTime = minimum AT.

    3. Return scheduling results and Gantt Chart.
