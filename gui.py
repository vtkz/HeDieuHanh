import sys
import os
import csv
from main import Process, SchedulerEngine, CSVHandler

def launch_gui():
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
    except ImportError:
        print("[NOTICE] Môi trường không hỗ trợ Tkinter display. Ung dung GUI hoat dong o che do Script!")
        return

    class SchedulerGUIApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Mô Phỏng CPU Scheduling - FCFS vs SJF (OS_SCH_01)")
            self.root.geometry("900x650")
            
            self.processes = []
            self.setup_ui()
            
        def setup_ui(self):
            # Header
            header = ttk.Label(self.root, text="MÔ PHỎNG CPU SCHEDULING - FCFS & SJF KHÔNG CƯỚP QUYỀN", 
                               font=("Arial", 14, "bold"))
            header.pack(pady=10)
            
            # Input Frame
            input_frame = ttk.LabelFrame(self.root, text="Nhập Tiến Trình Thủ Công")
            input_frame.pack(fill="x", padx=15, pady=5)
            
            ttk.Label(input_frame, text="ProcessID:").grid(row=0, column=0, padx=5, pady=5)
            self.entry_pid = ttk.Entry(input_frame, width=10)
            self.entry_pid.grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(input_frame, text="ArrivalTime:").grid(row=0, column=2, padx=5, pady=5)
            self.entry_at = ttk.Entry(input_frame, width=10)
            self.entry_at.grid(row=0, column=3, padx=5, pady=5)
            
            ttk.Label(input_frame, text="BurstTime:").grid(row=0, column=4, padx=5, pady=5)
            self.entry_bt = ttk.Entry(input_frame, width=10)
            self.entry_bt.grid(row=0, column=5, padx=5, pady=5)
            
            btn_add = ttk.Button(input_frame, text="add process", command=self.add_process)
            btn_add.grid(row=0, column=6, padx=10, pady=5)
            
            btn_clear = ttk.Button(input_frame, text="clear", command=self.clear_all)
            btn_clear.grid(row=0, column=7, padx=5, pady=5)

            # Table Frame
            table_frame = ttk.LabelFrame(self.root, text="Danh Sách Tiến Trình & Kết Quả Mô Phỏng")
            table_frame.pack(fill="both", expand=True, padx=15, pady=5)
            
            cols = ("ProcessID", "ArrivalTime", "BurstTime", "StartTime", "FinishTime", "TurnaroundTime", "WaitingTime", "ResponseTime")
            self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
            for col in cols:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=95, anchor="center")
            self.tree.pack(fill="both", expand=True, side="left")
            
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # Control Frame
            ctrl_frame = ttk.Frame(self.root)
            ctrl_frame.pack(fill="x", padx=15, pady=10)
            
            self.algo_var = tk.StringVar(value="FCFS")
            ttk.Radiobutton(ctrl_frame, text="FCFS", variable=self.algo_var, value="FCFS").pack(side="left", padx=10)
            ttk.Radiobutton(ctrl_frame, text="SJF Non-Preemptive", variable=self.algo_var, value="SJF").pack(side="left", padx=10)
            
            btn_run = ttk.Button(ctrl_frame, text="Chạy Mô Phỏng", command=self.run_simulation)
            btn_run.pack(side="left", padx=15)
            
            btn_import = ttk.Button(ctrl_frame, text="import CSV", command=self.import_csv)
            btn_import.pack(side="right", padx=5)
            
            btn_export = ttk.Button(ctrl_frame, text="export CSV", command=self.export_csv)
            btn_export.pack(side="right", padx=5)
            
            # Status Bar
            self.status_label = ttk.Label(self.root, text="Sẵn sàng nhập dữ liệu...", font=("Arial", 10, "italic"))
            self.status_label.pack(side="bottom", fill="x", padx=15, pady=5)

        def add_process(self):
            pid = self.entry_pid.get().strip()
            at_str = self.entry_at.get().strip()
            bt_str = self.entry_bt.get().strip()
            
            if not pid or not at_str or not bt_str:
                messagebox.showerror("Vui lòng nhập đầy đủ ProcessID, ArrivalTime và BurstTime!")
                return
            try:
                at = int(at_str)
                bt = int(bt_str)
            except ValueError:
                messagebox.showerror("ArrivalTime và BurstTime phải là số nguyên!")
                return
                
            if at < 0 or bt <= 0:
                messagebox.showerror("Ràng buộc: ArrivalTime >= 0 và BurstTime > 0!")
                return
                
            p = Process(pid, at, bt)
            self.processes.append(p)
            self.tree.insert("", "end", values=(p.pid, p.at, p.bt, "-", "-", "-", "-", "-"))
            
            self.entry_pid.delete(0, "end")
            self.entry_at.delete(0, "end")
            self.entry_bt.delete(0, "end")
            self.status_label.config(text=f"Đã thêm tiến trình {pid}.")

        def clear_all(self):
            self.processes.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.status_label.config(text="Đã xóa danh sách tiến trình.")

        def run_simulation(self):
            if not self.processes:
                messagebox.showwarning("Danh sách tiến trình rỗng!")
                return
                
            algo = self.algo_var.get()
            if algo == "FCFS":
                results, _ = SchedulerEngine.run_fcfs(self.processes)
            else:
                results, _ = SchedulerEngine.run_sjf_non_preemptive(self.processes)
                
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            tot_wt, tot_tat = 0, 0
            for p in results:
                self.tree.insert("", "end", values=(p.pid, p.at, p.bt, p.st, p.ft, p.tat, p.wt, p.rt))
                tot_wt += p.wt
                tot_tat += p.tat
                
            n = len(results)
            avg_wt = tot_wt / n
            avg_tat = tot_tat / n
            self.status_label.config(text=f"Hoàn thành! Thuật toán {algo} - Avg WT: {avg_wt:.2f}ms | Avg TAT: {avg_tat:.2f}ms")

        def import_csv(self):
            path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if path:
                try:
                    procs = CSVHandler.read_input_csv(path)
                    self.clear_all()
                    self.processes = procs
                    for p in procs:
                        self.tree.insert("", "end", values=(p.pid, p.at, p.bt, "-", "-", "-", "-", "-"))
                    self.status_label.config(text=f"Đã thêm {len(procs)} tiến trình từ {os.path.basename(path)}")
                except Exception as e:
                    messagebox.showerror("Lỗi import", str(e))

        def export_csv(self):
            if not self.processes:
                messagebox.showwarning("Không có dữ liệu để xuất!")
                return
            path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if path:
                try:
                    algo = self.algo_var.get()
                    if algo == "FCFS":
                        res, gantt = SchedulerEngine.run_fcfs(self.processes)
                    else:
                        res, gantt = SchedulerEngine.run_sjf_non_preemptive(self.processes)
                    CSVHandler.write_output_csv(path, res, gantt, algo)
                    messagebox.showinfo("Thành Công", f"Đã xuất kết quả ra file {os.path.basename(path)}")
                except Exception as e:
                    messagebox.showerror("Lỗi export", str(e))

    root = tk.Tk()
    app = SchedulerGUIApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
