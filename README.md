# Lab1_mwayo-tech
# Grade Evaluator & Archiver

## Overview
This project has two parts:
1. **`grade-evaluator.py`** — reads a CSV of course assignments, validates the scores and weights, calculates the final grade and GPA, and reports PASS/FAIL status along with any assignments eligible for resubmission.
2. **`organizer.sh`** — archives the current `grades.csv` with a timestamp, resets the workspace with a fresh empty file, and logs the action.

## Requirements
- Python 3
- Bash (Linux/macOS terminal, or WSL/Git Bash on Windows)

## 1. Running `grade-evaluator.py`

From the project directory, run:
```bash
python3 grade-evaluator.py
```

You will be prompted to enter the CSV filename:
```
Enter the name of the CSV file to process (e.g., grades.csv):
```
Type the filename (e.g. `grades.csv`) and press Enter.

### Expected CSV format
The file must have these exact column headers:
```
assignment,group,score,weight
```
- `group` must be either `Formative` or `Summative`
- `score` must be between 0 and 100
- Formative weights must sum to exactly 60, Summative weights must sum to exactly 40 (Total = 100)

### Example output
```
--- Processing Grades ---
Formative Total: 44.40 / 60
Summative Total: 32.50 / 40
Final Grade: 76.90%
GPA: 3.845
Status: PASSED
Available for resubmission: Discussion Forum
```

### Pass/Fail rule
A student passes only if they score **at least 50%** in **both** the Formative (≥30/60) and Summative (≥20/40) categories.

### Resubmission rule
Any Formative assignment scoring below 50 is eligible for resubmission. If multiple failed Formative assignments are tied for the **highest weight**, all of them are listed.

## 2. Running `organizer.sh`

Make the script executable (only needed once):
```bash
chmod +x organizer.sh
```

Then run it:
```bash
./organizer.sh
```

### What it does
1. Creates an `archive/` directory if one doesn't already exist.
2. Renames the current `grades.csv` by appending a timestamp (e.g. `grades_20260723-184650.csv`).
3. Moves the renamed file into `archive/`.
4. Creates a new, empty `grades.csv` in the current directory so the workspace is ready for the next batch of grades.
5. Appends a record of the run to `organizer.log`, including the timestamp, original filename, and archived filename.

### Example log entry
```
20260723-184650 | Original: grades.csv | Archived as: archive/grades_20260723-184650.csv
```

## Suggested workflow
1. Place your grade data in `grades.csv`.
2. Run `python3 grade-evaluator.py` and enter `grades.csv` to see the results.
3. Once you're done with that batch, run `./organizer.sh` to archive it and start fresh.
