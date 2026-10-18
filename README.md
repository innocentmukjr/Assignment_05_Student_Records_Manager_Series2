# 🎓 Student Records Manager — MIJ Academy Client Project

**Assignment 05 (Series 2) — MIJ Technologies Python Programming Series**
*From Complete Beginner to Software Engineer, Series 2 — File Handling Client Brief (Module 7)*

A menu-driven command-line program built from a simulated real-world client brief: MIJ Academy, a small training centre, needed their paper-based student tracking replaced with a tool that persists records between sessions, computes grades automatically, and produces a summary report — without ever crashing on non-technical staff.

---

## 🎯 Overview

This project is the **Series 2 edition of the Module 7 file-handling wrap-up project** — a separate, client-brief-style assignment distinct from Series 1's progressive five-assignment track. Where earlier assignments processed one session's worth of in-memory transactions, this one is built entirely around **persistence**: every record read, written, searched, updated, and deleted goes through `records.csv`, with a `summary.json` export layered on top, all wrapped in exception handling so the program is safe to hand to someone non-technical.

| | |
|---|---|
| **Modules Tested** | Modules 1–7 (Getting Started through File Handling) |
| **Difficulty** | File Handling (5/5) |
| **Total Marks** | 74 |
| **Estimated Time** | 5–7 hours |

---

## ✨ Features

- **Menu-driven interface** that loops until the user explicitly quits, with a clear message and a return to the menu on any invalid choice.
- **CSV-backed persistence** — student records live in `records.csv` and survive a full program restart.
- **Automatic file initialization** — on startup, `pathlib` checks whether `records.csv` exists; if not, it's created with just the header row, and left untouched if it already exists.
- **Corrupted-file recovery** — if an existing records file can't be parsed, it's backed up to `records_corrupted.csv` and a fresh file is created, rather than crashing on load.
- **Automatic grade computation** — grades are never typed in; they're always derived from the score via a lookup table, so a stale or mistyped grade can never end up on file.
- **Immediate save on add** — a new student is appended to `records.csv` the moment they're entered, so nothing is lost if the program is interrupted right after.
- **Case-insensitive, partial-match search** — searching "ali" finds "Alice", with every match (or a clear "no match") displayed in a formatted table.
- **Safe update and delete** — both look up matching students by name, let the user confirm which one if there's more than one match, rewrite the file, and roll back the in-memory change if the file write itself fails.
- **JSON summary export/view** — computes total students, average score, and the top and low scorers, writes them to `summary.json` in a human-readable indented format, and can reload and display that file on demand.
- **Exception handling around every file operation**, covering at least `FileNotFoundError` and `OSError` (handling `OSError` alone covers both, since `FileNotFoundError` is a subclass of it), plus `ValueError` protection on numeric input so non-numeric ages or scores are rejected and re-prompted instead of crashing the program.
- **Graceful exit handling** — `Ctrl+C` / `Ctrl+D` are caught so the program never crashes on interrupt.

---

## 🧮 Business Rules

**Grading Rule** (always computed from score — never entered by the user)

| Score | Grade |
|---|---|
| 90 and above | A |
| 80 – 89 | B |
| 70 – 79 | C |
| 60 – 69 | D |
| Below 60 | F |

**Menu Options**

| Option | Action |
|---|---|
| 1 | Add Student |
| 2 | View All Students |
| 3 | Search by Name |
| 4 | Update Score |
| 5 | Delete Student |
| 6 | Export JSON Summary |
| 7 | View JSON Summary |
| 8 | Quit |

**Summary Export Formula**
```
average     = round(sum(scores) / total, 2)
top_student = the student with the highest score
low_student = the student with the lowest score
```

---

## 🏗️ Code Structure

Each student record is a single dictionary (`d`) with four keys (`name`, `age`, `score`, `grade`), and the full in-memory roster is a list of these dictionaries, loaded once at startup and kept in sync with `records.csv` after every change.

| Function | Responsibility |
|---|---|
| `get_student_details()` | Collects name, age, and score for a new student |
| `validate_entry()` | Ensures no field is left blank; normalizes casing |
| `validate_integer_range()` | Ensures a numeric field is a valid integer within a min/max range |
| `determine_student_grade()` | Computes a student's grade from their score using the grading table |
| `load_records()` | Creates `records.csv` if missing, loads it if present, and recovers from a corrupted file |
| `save_records()` | Rewrites `records.csv` in full from the in-memory student list |
| `print_table()` | Renders a formatted, column-aligned table of student rows |
| `find_matches()` | Case-insensitive partial name search, shared by search/update/delete |
| `choose_student()` | Lets the user pick a specific student when a search returns multiple matches |
| `add_student()` | Collects a new student, grades them, appends to the file immediately, then updates memory |
| `view_all()` | Displays every student, or an empty-state message |
| `search_student()` | Searches by partial, case-insensitive name |
| `update_score()` | Finds, confirms, updates, and regrades a student, rolling back on save failure |
| `delete_student()` | Finds, confirms, and removes a student, rolling back on save failure |
| `export_summary()` | Computes total/average/top/low statistics and writes them to `summary.json` |
| `view_summary()` | Loads and displays `summary.json`, with a clear message if it hasn't been created yet |
| `main()` | Loads records on startup, then runs the menu loop until the user quits |

Centering everything on `find_matches()` + `choose_student()` means search, update, and delete all share the same lookup-and-disambiguate logic instead of three separate implementations.

---

## ▶️ How to Run

```bash
python3 student_records_manager.py
```

> **Note:** the original client brief requires the deliverable script be named exactly `MODULE 7 WRAP UP PROJECT.py` for grading — rename accordingly if submitting to the course rather than just browsing the portfolio.

On first run, `records.csv` is created automatically if it doesn't exist. From there, the menu loop handles everything — add, view, search, update, delete, export, and view summary — until you choose **8. Quit**.

---

## 🖥️ Sample Session

```
===============================================================================
 MIJ ACADEMY -- STUDENT RECORDS MANAGER
===============================================================================
records.csv not found -- creating with header row.

1. Add Student          2. View All Students     3. Search by Name
4. Update Score         5. Delete Student         6. Export JSON Summary
7. View JSON Summary    8. Quit

Choose an option: 1
Name: Alice Nakato | Age: 20 | Score: 92
Saved. Alice Nakato -- Grade: A

Choose an option: 2
===============================================================================
 ALL STUDENTS
===============================================================================
#  Name           Age  Score  Grade
1  Alice Nakato   20   92     A
Total students: 1

Choose an option: 6
{
  "total": 1,
  "average": 92.0,
  "top_student": {"name": "Alice Nakato", "score": 92},
  "low_student": {"name": "Alice Nakato", "score": 92}
}
Summary exported to summary.json

Choose an option: 8
Goodbye! Your records are saved in records.csv.
```

---

## ✅ Acceptance Test (Verified)

This is the exact sequence the client brief specifies as sign-off criteria — confirmed working end-to-end, including the persistence check across a restart:

| Step | Action | Expected Result |
|---|---|---|
| 1 | Delete `records.csv`, start program | File recreated with header only |
| 2 | Add Alice Nakato (20/92), Okello Bob (22/78), Atim Carol (19/85), Kato David (21/58) | Grades: A, C, B, F |
| 3 | View All | Shows 4 students with those grades |
| 4 | Search "ali" / "ALICE" / "zzz" | Finds Alice both times; no match for "zzz" |
| 5 | Export summary | `total=4`, `average=78.25`, top=Alice (92), low=Kato (58) |
| 6 | Update Kato David's score to 64, export again | Grade becomes D; `average=79.75` |
| 7 | Delete Okello Bob, export again | View All shows 3 students; `average=80.33` |
| 8 | Quit and restart | View All still shows the same 3 students |
| 9 | Choose invalid option 9; delete a nonexistent name | Both show a clear message with no state change |

---

## 🧠 What This Assignment Reinforced

- Treating a CSV file as the real source of truth, with every mutation (add/update/delete) immediately persisted rather than held only in memory
- Using `pathlib` to check file existence cleanly instead of `try`/`except` or `os.path`
- Recovering from a corrupted data file by quarantining it and starting fresh, instead of crashing or silently discarding data
- Rolling back an in-memory change when the corresponding file write fails, so memory and disk never drift out of sync
- Sharing one case-insensitive partial-match lookup function across three different features (search, update, delete) instead of duplicating the logic
- Exporting computed statistics to a separate, human-readable JSON file as a distinct reporting layer on top of the raw CSV records
- Writing exception handling around every file operation specifically so the program is safe for a non-technical end user

---

## 📂 Repository Contents

```
├── Assignment_05_Student_Records_Manager_Series2.pdf   # Original client brief
├── student_records_manager.py                          # My solution
├── records.csv                                          # Generated record store (created on first run)
├── summary.json                                         # Generated summary export (created via menu option 6)
└── README.md                                             # This file
```

---

## 🧵 Series Note

This assignment belongs to **Series 2** of the MIJ Technologies Python Programming curriculum — a separate, client-brief-style track focused on file handling (Modules 1–7), distinct from the Series 1 progressive assignments (Library Book Borrowing → Restaurant Billing → Electricity Vending → Parking Lot → Hospital Billing) documented earlier in this portfolio. Every solution in this repo series is written and understood by me before being committed — assignments are reviewed line-by-line for syntax and logic before upload.
