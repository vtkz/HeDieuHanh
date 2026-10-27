# CSV Input/Output Specification

## 1. Input CSV Format

The input CSV file contains the following columns in the required order:

| Column | Data type | Validation rule | Description |
|---|---|---|---|
| ProcessID | String | Must not be empty or duplicated | Process identifier |
| ArrivalTime | Integer | Must be greater than or equal to 0 | Time when the process arrives |
| BurstTime | Integer | Must be greater than 0 | CPU execution time required |

Required header:

ProcessID,ArrivalTime,BurstTime

## 2. Input Validation Rules

- The CSV file must contain all required columns with the exact header names.
- A process ID must not be empty.
- Process IDs must be unique.
- ArrivalTime must be a valid integer and must not be negative.
- BurstTime must be a valid integer greater than zero.
- Rows with missing or extra column values must be rejected.
- Blank rows are skipped.
- A file containing only the header and no process records is rejected.
- A missing input file is rejected.

## 3. Error Cases

| Error case | Expected handling |
|---|---|
| Input file does not exist | Reject the input |
| Incorrect or missing headers | Reject the input |
| Empty ProcessID | Reject the input |
| Duplicate ProcessID | Reject the input |
| Empty ArrivalTime | Reject the input |
| Non-numeric ArrivalTime or BurstTime | Reject the input |
| Negative ArrivalTime | Reject the input |
| BurstTime is zero or negative | Reject the input |
| Missing column value | Reject the input |
| Extra column value | Reject the input |
| Header-only CSV | Reject the input |
| Blank row | Skip the row |

## 4. Output CSV

The application exports simulation results to `output/simulation_results.csv` by default. A custom output path can also be provided.

The standard output columns are listed in the following order:

| Column | Description |
|---|---|
| ProcessID | Process identifier |
| ArrivalTime | Process arrival time |
| BurstTime | CPU burst time |
| StartTime | Process execution start time |
| CompletionTime | Process completion time |
| TurnaroundTime | Total time from arrival to completion |
| WaitingTime | Time spent waiting in the ready queue |
| ResponseTime | Time from arrival until first execution |

Output validation rules:

- The results list must not be empty.
- All result rows must contain the same column names in the same order.
- Invalid or inconsistent result data must be rejected.
- The output directory is created automatically if it does not exist.
- The CSV file is written using UTF-8 with BOM encoding.

## 5. Verification

Run the CSV data I/O test suite using the following command:

```bash
python -m unittest discover -s tests -v
```

The test suite covers CSV input parsing, input validation, simulation result export, and invalid or inconsistent data handling.

All tests must pass before the CSV data I/O changes are considered ready for submission. The test count should be updated whenever tests are added or removed.
