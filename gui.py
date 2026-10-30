import sys
import os
import csv
from main import Process, SchedulerEngine, CSVHandler

def launch_gui():
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
    except ImportError:
        return

    class SchedulerGUIApp:
        def __init__(self, root):
            self.root = root
            self.root.title("CPU Scheduling Simulator - First-Come First-Served vs Shortest Job First")
            self.root.geometry("950x650")
            self.processes = []
            self.setup_ui()
            
        def setup_ui(self):
            header = ttk.Label(self.root, text="CPU SCHEDULING SIMULATOR - FIRST-COME FIRST-SERVED & SHORTEST JOB FIRST", font=("Arial", 13, "bold"))
            header.pack(pady=10)
            
            input_frame = ttk.LabelFrame(self.root, text="Manual Process Entry")
            input_frame.pack(fill="x", padx=15, pady=5)
            
            ttk.Label(input_frame, text="ProcessID:").grid(row=0, column=0, padx=5, pady=5)
            self.entry_process_id = ttk.Entry(input_frame, width=10)
            self.entry_process_id.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(input_frame, text="ArrivalTime:").grid(row=0, column=2, padx=5, pady=5)
            self.entry_arrival_time = ttk.Entry(input_frame, width=10)
            self.entry_arrival_time.grid(row=0, column=3, padx=5, pady=5)
            
            ttk.Label(input_frame, text="BurstTime:").grid(row=0, column=4, padx=5, pady=5)
            self.entry_burst_time = ttk.Entry(input_frame, width=10)
            self.entry_burst_time.grid(row=0, column=5, padx=5, pady=5)
            
            btn_add = ttk.Button(input_frame, text="Add Process", command=self.add_process)
            btn_add.grid(row=0, column=6, padx=10, pady=5)
            
            btn_clear = ttk.Button(input_frame, text="Clear All", command=self.clear_all)
            btn_clear.grid(row=0, column=7, padx=5, pady=5)

            table_frame = ttk.LabelFrame(self.root, text="Process List & Simulation Results")
            table_frame.pack(fill="both", expand=True, padx=15, pady=5)
            
            columns = ("ProcessID", "ArrivalTime", "BurstTime", "StartTime", "FinishTime", "TurnaroundTime", "WaitingTime", "ResponseTime")
            self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=110, anchor="center")
            self.tree.pack(fill="both", expand=True, side="left")
            
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            control_frame = ttk.Frame(self.root)
            control_frame.pack(fill="x", padx=15, pady=10)
            
            self.algorithm_var = tk.StringVar(value="First-Come, First-Served")
            ttk.Radiobutton(control_frame, text="First-Come, First-Served", variable=self.algorithm_var, value="First-Come, First-Served").pack(side="left", padx=10)
            ttk.Radiobutton(control_frame, text="Shortest Job First Non-Preemptive", variable=self.algorithm_var, value="Shortest Job First").pack(side="left", padx=10)
            
            btn_run = ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
            btn_run.pack(side="left", padx=15)
            
            btn_import = ttk.Button(control_frame, text="Load CSV File", command=self.import_csv)
            btn_import.pack(side="right", padx=5)
            
            btn_export = ttk.Button(control_frame, text="Export CSV Results", command=self.export_csv)
            btn_export.pack(side="right", padx=5)
            
            self.status_label = ttk.Label(self.root, text="Ready to accept input...", font=("Arial", 10, "italic"))
            self.status_label.pack(side="bottom", fill="x", padx=15, pady=5)

        def add_process(self):
            process_id = self.entry_process_id.get().strip()
            arrival_time_str = self.entry_arrival_time.get().strip()
            burst_time_str = self.entry_burst_time.get().strip()
            
            if not process_id or not arrival_time_str or not burst_time_str:
                messagebox.showerror("Input Error", "Please fill in ProcessID, ArrivalTime, and BurstTime!")
                return
            try:
                arrival_time = int(arrival_time_str)
                burst_time = int(burst_time_str)
            except ValueError:
                messagebox.showerror("Input Error", "ArrivalTime and BurstTime must be integers!")
                return
                
            if arrival_time < 0 or burst_time <= 0:
                messagebox.showerror("Input Error", "Constraint violation: ArrivalTime >= 0 and BurstTime > 0!")
                return
                
            process = Process(process_id, arrival_time, burst_time)
            self.processes.append(process)
            self.tree.insert("", "end", values=(process.process_id, process.arrival_time, process.burst_time, "-", "-", "-", "-", "-"))
            
            self.entry_process_id.delete(0, "end")
            self.entry_arrival_time.delete(0, "end")
            self.entry_burst_time.delete(0, "end")
            self.status_label.config(text=f"Added process {process_id}.")

        def clear_all(self):
            self.processes.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.status_label.config(text="Cleared process list.")

        def run_simulation(self):
            if not self.processes:
                messagebox.showwarning("Warning", "Process list is empty!")
                return
                
            algorithm = self.algorithm_var.get()
            if algorithm == "First-Come, First-Served":
                results, _ = SchedulerEngine.run_first_come_first_served(self.processes)
            else:
                results, _ = SchedulerEngine.run_shortest_job_first_non_preemptive(self.processes)
                
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            total_waiting_time, total_turnaround_time = 0, 0
            for process in results:
                self.tree.insert("", "end", values=(process.process_id, process.arrival_time, process.burst_time, process.start_time, process.finish_time, process.turnaround_time, process.waiting_time, process.response_time))
                total_waiting_time += process.waiting_time
                total_turnaround_time += process.turnaround_time
                
            count = len(results)
            average_waiting_time = total_waiting_time / count
            average_turnaround_time = total_turnaround_time / count
            self.status_label.config(text=f"Success! Algorithm: {algorithm} - Average Waiting Time: {average_waiting_time:.2f}ms | Average Turnaround Time: {average_turnaround_time:.2f}ms")

        def import_csv(self):
            filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if filepath:
                try:
                    processes = CSVHandler.read_input_csv(filepath)
                    self.clear_all()
                    self.processes = processes
                    for process in processes:
                        self.tree.insert("", "end", values=(process.process_id, process.arrival_time, process.burst_time, "-", "-", "-", "-", "-"))
                    self.status_label.config(text=f"Loaded {len(processes)} processes from {os.path.basename(filepath)}")
                except Exception as error:
                    messagebox.showerror("File Import Error", str(error))

        def export_csv(self):
            if not self.processes:
                messagebox.showwarning("Warning", "No data available to export!")
                return
            filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if filepath:
                try:
                    algorithm = self.algorithm_var.get()
                    if algorithm == "First-Come, First-Served":
                        results, gantt_chart = SchedulerEngine.run_first_come_first_served(self.processes)
                    else:
                        results, gantt_chart = SchedulerEngine.run_shortest_job_first_non_preemptive(self.processes)
                    CSVHandler.write_output_csv(filepath, results, gantt_chart, algorithm)
                    messagebox.showinfo("Success", f"Exported results to {os.path.basename(filepath)}")
                except Exception as error:
                    messagebox.showerror("File Export Error", str(error))

    root = tk.Tk()
    app = SchedulerGUIApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
