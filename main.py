import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("students.json")


class StudentStore:
    def __init__(self, path=DATA_FILE):
        self.path = Path(path)
        self.students = self._load()

    def _load(self):
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            students = json.load(file)

        if not isinstance(students, list) or any(
            not isinstance(student, dict)
            or not all(key in student for key in ("id", "name", "age", "course"))
            for student in students
        ):
            raise ValueError(f"Invalid student data in {self.path}")
        return students

    def _save(self):
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=2)

    def add(self, student_id, name, age, course):
        student_id = student_id.strip()
        name = name.strip()
        course = course.strip()
        if not student_id or not name or not course:
            raise ValueError("ID, name, and course cannot be empty.")
        if any(student["id"] == student_id for student in self.students):
            raise ValueError(f"Student ID '{student_id}' already exists.")
        if age < 1:
            raise ValueError("Age must be a positive number.")

        self.students.append(
            {"id": student_id, "name": name, "age": age, "course": course}
        )
        self._save()

    def find(self, query):
        query = query.strip().casefold()
        return [
            student
            for student in self.students
            if query in student["id"].casefold()
            or query in student["name"].casefold()
        ]

    def update(self, student_id, name, age, course):
        student = next(
            (student for student in self.students if student["id"] == student_id),
            None,
        )
        if student is None:
            raise ValueError(f"No student found with ID '{student_id}'.")
        if not name.strip() or not course.strip():
            raise ValueError("Name and course cannot be empty.")
        if age < 1:
            raise ValueError("Age must be a positive number.")

        student.update({"name": name.strip(), "age": age, "course": course.strip()})
        self._save()

    def delete(self, student_id):
        remaining = [
            student for student in self.students if student["id"] != student_id
        ]
        if len(remaining) == len(self.students):
            raise ValueError(f"No student found with ID '{student_id}'.")
        self.students = remaining
        self._save()


def display_students(students):
    if not students:
        print("No students found.")
        return

    print(f"\n{'ID':<12} {'Name':<24} {'Age':<6} Course")
    print("-" * 60)
    for student in students:
        print(
            f"{student['id']:<12} {student['name']:<24} "
            f"{student['age']:<6} {student['course']}"
        )


def read_age():
    try:
        age = int(input("Age: ").strip())
    except ValueError as error:
        raise ValueError("Age must be a whole number.") from error
    if age < 1:
        raise ValueError("Age must be a positive number.")
    return age


def run_cli(store):
    actions = {
        "1": "Add student",
        "2": "List students",
        "3": "Search students",
        "4": "Update student",
        "5": "Delete student",
        "0": "Exit",
    }

    while True:
        print("\nStudent Management System")
        for choice, label in actions.items():
            print(f"{choice}. {label}")

        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                store.add(
                    input("Student ID: "),
                    input("Name: "),
                    read_age(),
                    input("Course: "),
                )
                print("Student added.")
            elif choice == "2":
                display_students(store.students)
            elif choice == "3":
                display_students(store.find(input("Search by ID or name: ")))
            elif choice == "4":
                student_id = input("Student ID to update: ").strip()
                name = input("New name: ")
                age = read_age()
                course = input("New course: ")
                store.update(student_id, name, age, course)
                print("Student updated.")
            elif choice == "5":
                store.delete(input("Student ID to delete: ").strip())
                print("Student deleted.")
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Invalid option. Choose a number from 0 to 5.")
        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"Could not save student data: {error}")


if __name__ == "__main__":
    try:
        run_cli(StudentStore())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load student data: {error}")
