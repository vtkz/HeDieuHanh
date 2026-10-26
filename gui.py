import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from main import Process, SchedulerEngine, CSVHandler


class SchedulerGUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng lập lịch CPU - FCFS và SJF")
        self.root.geometry("1100x650")

        self.processes = []
        self.last_results = []
        self.last_gantt_chart = []
        self.last_algorithm = ""

        self.setup_ui()

    def setup_ui(self):
        header = ttk.Label(
            self.root,
            text="MÔ PHỎNG LẬP LỊCH CPU - FCFS VÀ SJF KHÔNG ĐỘC QUYỀN",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=10)

        input_frame = ttk.LabelFrame(
            self.root,
            text="Nhập thông tin tiến trình"
        )
        input_frame.pack(fill="x", padx=15, pady=5)

        ttk.Label(input_frame, text="ProcessID:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.entry_process_id = ttk.Entry(input_frame, width=12)
        self.entry_process_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="ArrivalTime:").grid(
            row=0, column=2, padx=5, pady=5
        )
        self.entry_arrival_time = ttk.Entry(input_frame, width=12)
        self.entry_arrival_time.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="BurstTime:").grid(
            row=0, column=4, padx=5, pady=5
        )
        self.entry_burst_time = ttk.Entry(input_frame, width=12)
        self.entry_burst_time.grid(row=0, column=5, padx=5, pady=5)

        ttk.Button(
            input_frame,
            text="Thêm tiến trình",
            command=self.add_process
        ).grid(row=0, column=6, padx=8, pady=5)

        ttk.Button(
            input_frame,
            text="Xóa danh sách",
            command=self.clear_all
        ).grid(row=0, column=7, padx=5, pady=5)

        table_frame = ttk.LabelFrame(
            self.root,
            text="Danh sách tiến trình và kết quả mô phỏng"
        )
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = (
            "ProcessID",
            "ArrivalTime",
            "BurstTime",
            "StartTime",
            "CompletionTime",
            "TurnaroundTime",
            "WaitingTime",
            "ResponseTime"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=125, anchor="center")

        self.tree.pack(
            fill="both",
            expand=True,
            side="left"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=15, pady=10)

        self.algorithm_var = tk.StringVar(value="FCFS")

        ttk.Radiobutton(
            control_frame,
            text="FCFS",
            variable=self.algorithm_var,
            value="FCFS"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            control_frame,
            text="SJF không độc quyền",
            variable=self.algorithm_var,
            value="SJF"
        ).pack(side="left", padx=10)

        ttk.Button(
            control_frame,
            text="Chạy mô phỏng",
            command=self.run_simulation
        ).pack(side="left", padx=10)

        ttk.Button(
            control_frame,
            text="Nhập file CSV",
            command=self.import_csv
        ).pack(side="right", padx=5)

        ttk.Button(
            control_frame,
            text="Xuất file CSV",
            command=self.export_csv
        ).pack(side="right", padx=5)

        self.status_label = ttk.Label(
            self.root,
            text="Sẵn sàng nhập dữ liệu.",
            font=("Arial", 10, "italic")
        )
        self.status_label.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=5
        )

    def add_process(self):
        process_id = self.entry_process_id.get().strip()
        arrival_time_text = self.entry_arrival_time.get().strip()
        burst_time_text = self.entry_burst_time.get().strip()

        if not process_id or not arrival_time_text or not burst_time_text:
            messagebox.showerror(
                "Thiếu dữ liệu",
                "Vui lòng nhập đầy đủ ProcessID, ArrivalTime và BurstTime."
            )
            return

        if any(
            process.process_id == process_id
            for process in self.processes
        ):
            messagebox.showerror(
                "Dữ liệu không hợp lệ",
                f"ProcessID '{process_id}' đã tồn tại."
            )
            return

        try:
            arrival_time = int(arrival_time_text)
            burst_time = int(burst_time_text)
        except ValueError:
            messagebox.showerror(
                "Dữ liệu không hợp lệ",
                "ArrivalTime và BurstTime phải là số nguyên."
            )
            return

        if arrival_time < 0:
            messagebox.showerror(
                "Dữ liệu không hợp lệ",
                "ArrivalTime phải lớn hơn hoặc bằng 0."
            )
            return

        if burst_time <= 0:
            messagebox.showerror(
                "Dữ liệu không hợp lệ",
                "BurstTime phải lớn hơn 0."
            )
            return

        process = Process(
            process_id,
            arrival_time,
            burst_time
        )
        self.processes.append(process)

        self.refresh_table()
        self.clear_entries()

        self.status_label.config(
            text=f"Đã thêm tiến trình {process_id}."
        )

    def clear_entries(self):
        self.entry_process_id.delete(0, tk.END)
        self.entry_arrival_time.delete(0, tk.END)
        self.entry_burst_time.delete(0, tk.END)

    def clear_all(self):
        self.processes.clear()
        self.last_results = []
        self.last_gantt_chart = []
        self.last_algorithm = ""

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.status_label.config(
            text="Đã xóa danh sách tiến trình."
        )

    def refresh_table(self, results=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_processes = (
            results if results is not None else self.processes
        )

        for process in display_processes:
            if results is None:
                values = (
                    process.process_id,
                    process.arrival_time,
                    process.burst_time,
                    "-",
                    "-",
                    "-",
                    "-",
                    "-"
                )
            else:
                values = (
                    process.process_id,
                    process.arrival_time,
                    process.burst_time,
                    process.start_time,
                    process.completion_time,
                    process.turnaround_time,
                    process.waiting_time,
                    process.response_time
                )

            self.tree.insert("", tk.END, values=values)

    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning(
                "Chưa có dữ liệu",
                "Vui lòng thêm tiến trình hoặc nhập file CSV trước."
            )
            return

        algorithm = self.algorithm_var.get()

        if algorithm == "FCFS":
            results, gantt_chart = SchedulerEngine.run_fcfs(
                self.processes
            )
        else:
            results, gantt_chart = (
                SchedulerEngine.run_sjf_non_preemptive(
                    self.processes
                )
            )

        self.last_results = results
        self.last_gantt_chart = gantt_chart
        self.last_algorithm = algorithm

        self.refresh_table(results)

        number_of_processes = len(results)
        average_waiting_time = (
            sum(p.waiting_time for p in results)
            / number_of_processes
        )
        average_turnaround_time = (
            sum(p.turnaround_time for p in results)
            / number_of_processes
        )
        average_response_time = (
            sum(p.response_time for p in results)
            / number_of_processes
        )

        gantt_text = " | ".join(
            f"{process_id} [{start_time}-{completion_time}]"
            for process_id, start_time, completion_time in gantt_chart
        )

        self.status_label.config(
            text=(
                f"{algorithm} hoàn tất | "
                f"AverageWaitingTime: {average_waiting_time:.2f} | "
                f"AverageTurnaroundTime: {average_turnaround_time:.2f} | "
                f"AverageResponseTime: {average_response_time:.2f}"
            )
        )

        messagebox.showinfo(
            "Kết quả mô phỏng",
            f"Thuật toán: {algorithm}\n"
            f"AverageWaitingTime: {average_waiting_time:.2f}\n"
            f"AverageTurnaroundTime: {average_turnaround_time:.2f}\n"
            f"AverageResponseTime: {average_response_time:.2f}\n\n"
            f"Gantt Chart:\n{gantt_text}"
        )

    def import_csv(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file CSV đầu vào",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        try:
            imported_processes = CSVHandler.read_input_csv(file_path)

            self.processes = imported_processes
            self.last_results = []
            self.last_gantt_chart = []
            self.last_algorithm = ""

            self.refresh_table()

            self.status_label.config(
                text=(
                    f"Đã nhập {len(imported_processes)} tiến trình "
                    f"từ {os.path.basename(file_path)}."
                )
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Lỗi nhập CSV",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Lỗi nhập CSV",
                f"Không thể đọc file: {error}"
            )

    def export_csv(self):
        if not self.processes:
            messagebox.showwarning(
                "Chưa có dữ liệu",
                "Không có tiến trình để xuất."
            )
            return

        if not self.last_results:
            messagebox.showwarning(
                "Chưa chạy mô phỏng",
                "Vui lòng chạy FCFS hoặc SJF trước khi xuất kết quả."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Lưu báo cáo kết quả",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )

        if not file_path:
            return

        try:
            CSVHandler.write_output_csv(
                file_path,
                self.last_results,
                self.last_gantt_chart,
                self.last_algorithm
            )

            messagebox.showinfo(
                "Xuất thành công",
                f"Đã xuất báo cáo tới:\n{file_path}"
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Lỗi xuất CSV",
                str(error)
            )


def launch_gui():
    root = tk.Tk()
    SchedulerGUIApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()