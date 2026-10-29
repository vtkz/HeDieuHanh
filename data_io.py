
import csv
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_FILE = PROJECT_DIR / "input" / "processes.csv"
REQUIRED_COLUMNS = ["ProcessID", "ArrivalTime", "BurstTime"]



def read_processes_csv(file_path=DEFAULT_INPUT_FILE):
    processes = []
    process_ids = set()

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("File CSV rong hoac khong co tieu de.")

            headers = [name.strip() if name else "" for name in reader.fieldnames]

            if headers != REQUIRED_COLUMNS:
                raise ValueError(
                    "Tieu de CSV phai la: ProcessID,ArrivalTime,BurstTime."
                )

            reader.fieldnames = headers

            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError(
                        f"Dong {line_number}: CSV co nhieu cot hon quy dinh."
                    )

                if not any(
                    value and value.strip()
                    for value in row.values()
                    if isinstance(value, str)
                ):
                    continue

                missing_columns = [
                    column
                    for column in REQUIRED_COLUMNS
                    if row.get(column) is None
                ]

                if missing_columns:
                    raise ValueError(
                        f"Dong {line_number}: CSV thieu cot du lieu."
                    )

                process_id = (row.get("ProcessID") or "").strip()
                arrival_text = (row.get("ArrivalTime") or "").strip()
                burst_text = (row.get("BurstTime") or "").strip()

                if not process_id:
                    raise ValueError(
                        f"Dong {line_number}: ProcessID khong duoc de trong."
                    )

                if process_id in process_ids:
                    raise ValueError(
                        f"Dong {line_number}: ProcessID '{process_id}' bi trung."
                    )

                try:
                    arrival_time = int(arrival_text)
                    burst_time = int(burst_text)
                except ValueError:
                    raise ValueError(
                        f"Dong {line_number}: ArrivalTime va BurstTime "
                        "phai la so nguyen."
                    ) from None

                if arrival_time < 0:
                    raise ValueError(
                        f"Dong {line_number}: ArrivalTime phai >= 0."
                    )

                if burst_time <= 0:
                    raise ValueError(
                        f"Dong {line_number}: BurstTime phai > 0."
                    )

                process_ids.add(process_id)
                processes.append({
                    "ProcessID": process_id,
                    "ArrivalTime": arrival_time,
                    "BurstTime": burst_time
                })

    except FileNotFoundError:
        raise FileNotFoundError(
            f"Khong tim thay file CSV: {file_path}"
        ) from None

    if not processes:
        raise ValueError("File CSV khong co tien trinh hop le.")

    return processes

def export_results_csv(results, file_path=None):
    if file_path is None:
        file_path = PROJECT_DIR / "output" / "simulation_results.csv"
    else:
        file_path = Path(file_path)

    if not results:
        raise ValueError("Khong co ket qua de xuat.")

    rows = []

    for result in results:
        if isinstance(result, dict):
            rows.append(result)
        else:
            rows.append({
                "ProcessID": result.pid,
                "ArrivalTime": result.at,
                "BurstTime": result.bt,
                "StartTime": result.st,
                "CompletionTime": result.ft,
                "TurnaroundTime": result.tat,
                "WaitingTime": result.wt,
                "ResponseTime": result.rt
            })

    fieldnames = list(rows[0].keys())

    for row in rows:
        if list(row.keys()) != fieldnames:
            raise ValueError("Cac dong ket qua khong cung cau truc.")

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return file_path


if __name__ == "__main__":
    try:
        result = read_processes_csv()
        print("Doc CSV thanh cong!")
        print(f"So tien trinh: {len(result)}")

        for process in result:
            print(process)

        output_path = export_results_csv(result)
        print(f"Da xuat CSV tai: {output_path}")

    except (ValueError, OSError) as error:
        print(f"Loi: {error}")

