import os
from main import Process, SchedulerEngine

def test_idle_case():
    procs = [Process('P1', 2, 5), Process('P2', 10, 3)]
    _, gantt = SchedulerEngine.run_fcfs(procs)
    assert any(item[0] == 'IDLE' for item in gantt)

def test_tie_case():
    procs = [Process('P2', 0, 5), Process('P1', 0, 5)]
    res, _ = SchedulerEngine.run_fcfs(procs)
    assert res[0].pid == 'P1'

if __name__ == '__main__':
    test_idle_case()
    test_tie_case()
    print('All tests passed!')

