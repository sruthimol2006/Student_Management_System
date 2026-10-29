# Student Management System CLI

A basic student record manager that runs in the terminal. It uses only the
Python standard library.

## Run

```powershell
python main.py
```

Choose an option from the menu to add, list, search, update, or delete students.
Student records are saved in `students.json` beside `main.py` and remain
available the next time the program runs. Each student has an ID, name, age,
and course; IDs must be unique.

## Run tests

```powershell
python -m unittest
```
