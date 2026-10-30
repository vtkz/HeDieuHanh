# CPU SCHEDULING SIMULATOR (OS_SCH_01)
## FIRST-COME, FIRST-SERVED & SHORTEST JOB FIRST NON-PREEMPTIVE

Operating System Course Project (125001) - Ho Chi Minh City University of Transport (UTH).
Topic: **OS_SCH_01 - CPU Scheduling Simulation for First-Come, First-Served and Shortest Job First Non-Preemptive Algorithms**.

---

### 1. PROJECT STRUCTURE & DIRECTORY LAYOUT

```text
OS_SCH_01_PROJECT/
├── main.py                         # Core execution & Test Oracle runner
├── gui.py                          # Graphical User Interface application (Tkinter)
├── input/                          # Input data directory
│   ├── input.csv                   # Default input dataset (ProcessID, ArrivalTime, BurstTime)
│   ├── input_idle.csv              # Input dataset featuring CPU idle periods
│   └── input_tie.csv               # Input dataset for tie-breaking verification
├── output/                         # Simulation output directory
│   ├── output_fcfs.csv             # Execution trace log and metrics for First-Come, First-Served
│   ├── output_sjf.csv              # Execution trace log and metrics for Shortest Job First Non-Preemptive
│   ├── gantt.png                   # Visual Gantt chart comparison diagram
│   └── benchmark.png               # Performance stress test plot (O(N log N) vs O(N^2))
├── test/                           # Automated testing directory
│   └── test_oracle.py              # Test Oracle verification suite
├── Bao_Cao_Do_An_OS_SCH_01.docx    # Official academic project report document
├── TIEN_DO_MA_NGUON_THEO_TUAN.md   # Incremental weekly progress tracking log
└── README.md                       # Project documentation and execution guide
```

---

### 2. INSTALLATION & EXECUTION GUIDE

#### 2.1 System Requirements:
* Python 3.8+
* Required Dependencies: `matplotlib`

Install dependencies using:
```bash
pip install matplotlib
```

#### 2.2 Launch Graphical User Interface Application:
To run the interactive desktop application:
```bash
python gui.py
```
*Features:* Manual process entry, strict input validation (ArrivalTime >= 0, BurstTime > 0), CSV file loading/exporting, algorithm selection, execution table with ProcessID, ArrivalTime, BurstTime, StartTime, FinishTime, TurnaroundTime, WaitingTime, ResponseTime, and summary statistics.

#### 2.3 Automated Test Execution & Command Line Simulation:
To execute the automated Test Oracle suite, generate output CSV files, and render visualization plots:
```bash
python main.py
```

---

### 3. TIE-BREAKING RULES

1. **First-Come, First-Served Algorithm:**
   * Priority 1: Smallest ArrivalTime.
   * Priority 2: Smallest ProcessID (Alphanumeric order).

2. **Shortest Job First Non-Preemptive Algorithm:**
   * Priority 1: Smallest BurstTime.
   * Priority 2: Smallest ArrivalTime.
   * Priority 3: Smallest ProcessID (Alphanumeric order).

---

### 4. TEAM MEMBER RESPONSIBILITIES & PARTICIPATION

| Team Member | Role | Core Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | Group Leader & First-Come First-Served Lead | Architecture design, First-Come First-Served algorithm engine implementation, project management |
| **Member 2** | Shortest Job First Lead & Test Oracle Specialist | Shortest Job First Non-Preemptive engine implementation, Test Oracle suite development |
| **Member 3** | Graphical User Interface & Visualization Developer | Desktop application (gui.py) development, Gantt chart renderer implementation |
| **Member 4** | Data Engine Developer | CSV Handler implementation, input data validation and error handling |
| **Member 5** | Quality Assurance & Performance Benchmark Engineer | Performance stress testing (N = 10 to 3000 processes), benchmark plot generation |

---

### 5. AI USE STATEMENT

The team declares the transparent use of AI tools (Gemini Notebook) for library syntax reference, report formatting compliance, and test case suggestions. All core scheduling logic, algorithms, data structures, and verification tests were fully authored and validated by the team.
