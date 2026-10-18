'''
                                    STUDENT RECORDS MANAGER
'''

import csv
import json
from pathlib import Path

VALID_OPTIONS = ('Yes', 'No')
VALID_CHOICES = ('1','2','3','4','5','6','7','8')
LINE_WIDTH = 100
SEPARATOR = "=" * LINE_WIDTH
LABEL_WIDTH = 25
FIELD_NAMES = ['name', 'age', 'score', 'grade']
GRADE_RULE = [
    (90,'A'),
    (80,'B'),
    (70, 'C'),
    (60, 'D')
]

BASE_FOLDER = Path(__file__).resolve().parent

BELOW_60 = 'F'

MENU_LAYOUT= [
    ('1. Add Student'),
    ('2. View All Students'),
    ('3. Search by Name'),
    ('4. Update Score'),
    ('5. Delete Student'),
    ('6. Export JSON Summary'),
    ('7. View JSON Summary'),
    ('8. Quit')
]

def get_student_details():
    """Ask for a student's name, age and score and return them as a dictionary."""
    d = {}
    d['name'] = validate_entry("Enter Student Name: ")
    d['age'] = validate_integer_range("Enter Student Age: ", 1,100)
    d['score'] = validate_integer_range("Enter Student Score: ", 0, 100)

    return d

def validate_entry(prompt):
    """Keep asking until the user types something non-empty; return it stripped and title-cased."""
    while True:
        entry = input(prompt)
        if entry.strip():
            return entry.strip().title()
        print('Field Cannot be empty!, please try again by entering something...')

def validate_integer_range(prompt, minimum, maximum=None):
    """Keep asking until the user enters an integer within minimum and maximum; return it."""
    while True:
        try:
            value = int(validate_entry(prompt))
            if value < minimum or (maximum is not None and value > maximum):
                print("Value entered is out of acceptable range, please try again...")
            else:
                return value
        except ValueError:
            print("Non integer entries are not allowed, please try again by entering an integer...")

def determine_student_grade(d):
    """Set the 'grade' key of a student dictionary from its score using GRADE_RULE."""
    d['grade'] = next((grade for minimum, grade in GRADE_RULE if d['score'] >= minimum),BELOW_60)

def load_records(records_file):
    """Create records.csv if missing, otherwise load it; return the list of students."""
    students = []
    if not records_file.exists():
        try:
            with records_file.open('w', encoding= 'utf-8', newline='') as csv_file:
                writer = csv.DictWriter(csv_file,fieldnames=FIELD_NAMES)
                writer.writeheader()
        except OSError as error:
            print(f"Could not create the records file: {error}")
    else:
        try:
            temp = []
            with records_file.open('r', encoding='utf-8',newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for student in reader:
                    student['score'] = int(student['score'])
                    student['age']  = int(student['age'])
                    temp.append(student)
                students = temp
        except(OSError,ValueError,KeyError):
            print("The file seems to be corrupted, please contact support for further assistance...")
            try:
                records_file.replace(BASE_FOLDER / 'records_corrupted.csv')
                with records_file.open('w', encoding='utf-8', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
                    writer.writeheader()
            except OSError as error:
                print(f"Could not back up the corrupted file: {error}")
    return students

def save_records(records_file, students):
    """Rewrite records.csv with every student; return True on success, False on failure."""
    try:
        with records_file.open('w',encoding='utf-8',newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        return True
    except OSError as error:
        print(f"Could not save the records file: {error}")
        return False

def print_table(title, rows):
    """Print rows of students as a formatted table under the given title."""
    name_width = max(4,max(len(d['name']) for d in rows)) + 10
    print(SEPARATOR)
    print(title.center(LINE_WIDTH))
    print(SEPARATOR)
    print()
    print('-' * (name_width + 35))
    print(f"{'No.':<5}{'Name':<{name_width}}{'Age':<10}{'Score':<10}{'Grade':<10}")
    for label, d in enumerate(rows,start=1):
        print(f"{label:<5}{d['name']:<{name_width}}{d['age']:<10}{d['score']:<10}{d['grade']:<10}")
    print('-' * (name_width + 35))

def find_matches(students, prompt):
    """Ask for a name, show the matching students, and return them (empty list if none)."""
    if not students:
        print("There is no student details recorded yet...")
        return []
    name_search = validate_entry(prompt).lower()
    matches = [d for d in students if name_search in d['name'].lower() ]
    if not matches:
        print(f"No Such a student matches your search '{name_search}'")
        return []
    print_table("MATCHING STUDENTS", matches)
    return matches

def choose_student(matches, prompt):
    """Ask for a number from the displayed matches and return the chosen student."""
    print()
    while True:
        try:
            choose_number = int(validate_entry(prompt))
            if choose_number < 1 or choose_number > len(matches):
                print("Chosen number out of range, please try again...")
            else:
                return matches[choose_number - 1]
        except ValueError:
            print("Non integer entries are not allowed, please try again")

def add_student(records_file, students):
    """Collect a new student, save the record to the file, then add it to memory."""
    d = get_student_details()
    determine_student_grade(d)
    try:
        with records_file.open('a',encoding='utf-8',newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
            writer.writerow(d)
    except OSError as error:
        print(f"Could not save the new student: {error}")
        return
    students.append(d)
    print()
    print(f"{d['name']} has successfully been added with grade {d['grade']}")

def view_all(students):
    """Display every student, or a message when there are none."""
    if not students:
        print("There is no student details recorded yet...")
    else:
        print_table("ALL STUDENTS", students)

def search_student(students):
    """Search students by partial, case-insensitive name and display the matches."""
    find_matches(students, 'Enter Name to Search: ')

def update_score(records_file, students):
    """Find a student, let the user pick one, and update that student's score and grade."""
    matches = find_matches(students, "Search Name to update their score: ")
    if not matches:
        return
    chosen = choose_student(matches, 'Enter number matching student score to update: ')
    old_score = chosen['score']
    old_grade = chosen['grade']
    chosen['score'] = validate_integer_range("Enter New score to update: ",0,100)
    determine_student_grade(chosen)
    if save_records(records_file, students):
        print()
        print(f"{chosen['name']}'s score has successfully been updated to {chosen['score']}")
    else:
        chosen['score'] = old_score
        chosen['grade'] = old_grade
        print("The score was not updated.")

def delete_student(records_file, students):
    """Find a student, let the user pick one, and delete that student."""
    matches = find_matches(students, "Search Name of student to delete: ")
    if not matches:
        return
    chosen = choose_student(matches, 'Enter number matching student to delete: ')
    position = students.index(chosen)
    students.remove(chosen)
    if save_records(records_file, students):
        print()
        print(f"{chosen['name']}'s details have successfully been deleted ")
    else:
        students.insert(position, chosen)
        print("The student was not deleted.")

def export_summary(summary_file, students):
    """Compute total, average, top and low students and write them to summary.json."""
    if not students:
        print("There is no student details recorded yet...")
        return
    scores = [d['score'] for d in students ]
    average = round(sum(scores)/len(scores), 2)
    top = max(students, key=lambda d: d['score'])
    low = min(students, key=lambda d: d['score'])
    summary = {
        "total": len(students),
        "average": average,
        "top_student": {"name": top['name'], "score": top['score']},
        "low_student": {"name": low['name'], "score": low['score']}
        }
    try:
        with summary_file.open('w', encoding='utf-8') as json_file:
            json.dump(summary, json_file, indent=4)
    except OSError as error:
        print(f"Could not export the summary: {error}")
        return
    print("Summary exported successfully to summary.json")

def view_summary(summary_file):
    """Load summary.json and display it, or explain what is wrong with it."""
    if not summary_file.exists():
        print("File does not exist!, please first choose option 6 to create it...")
        return
    try:
        with summary_file.open("r", encoding='utf-8') as json_file:
            summary = json.load(json_file)
        report = [
            f"Total Students : {summary['total']}",
            f"Average Score  : {summary['average']}",
            f"Top Student    : {summary['top_student']['name']} ({summary['top_student']['score']})",
            f"Low Student    : {summary['low_student']['name']} ({summary['low_student']['score']})"
        ]
    except (OSError, ValueError, KeyError, TypeError):
        print("The summary file is damaged or unreadable, please choose option 6 to create it again...")
        return
    print(SEPARATOR)
    print("SUMMARY REPORT".center(LINE_WIDTH))
    print(SEPARATOR)
    for line in report:
        print(line)
    print(SEPARATOR)

def main():
    """Load the records and run the menu loop until the user quits."""
    records_file = BASE_FOLDER/'records.csv'
    summary_file = BASE_FOLDER / 'summary.json'
    students = load_records(records_file)
    while True:
        print()
        print(SEPARATOR)
        print('STUDENTS RECORDS MANAGER GENERAL MENU'.center(100))
        print(SEPARATOR)
        for item in MENU_LAYOUT:
            print(item)
        print()
        choice = validate_entry('Choose Option (1-8) To Proceed: ')
        print("\n")
        if choice in VALID_CHOICES:
            if choice == '1':
                add_student(records_file, students)
            elif choice == '2':
                view_all(students)
            elif choice == '3':
                search_student(students)
            elif choice == '4':
                update_score(records_file, students)
            elif choice == '5':
                delete_student(records_file, students)
            elif choice == '6':
                export_summary(summary_file, students)
            elif choice == '7':
                view_summary(summary_file)
            elif choice == '8':
                return
        else:
            print('Choice out of range, please try again choosing from (1-8)...')

if __name__ == "__main__":
    try:
        main()
    except(EOFError, KeyboardInterrupt):
        print("Program Interrupted by the User, closing...")
    except OSError as error:
        print(f"An Unexpected error {error} occured!...")
