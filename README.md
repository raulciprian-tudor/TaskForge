# TaskForge 🧩

TaskForge is a command-line task and workflow manager written in Python.  
It was built as part of my learning journey to practice **state management, system evolution, and non-trivial program logic**.

The project started as a small task list and gradually evolved into a feature-rich system through iterative refinement.

---

## ✨ Features

- Create, update, and delete tasks
- Task status workflow:
  - `todo → in progress → done`
- Priority levels:
  - `low → medium → high`
- Due dates with overdue task detection
- Task filtering by status and priority
- Persistent storage using JSON (load/save on startup)
- Audit logging of task actions
- Undo functionality using state snapshots
- Incremental task IDs
- Input validation and defensive logic

---

## 🧠 What This Project Demonstrates

- Modeling workflows as state transitions
- Using rules (`ALLOWED_TRANSITIONS`) instead of hard-coded logic
- Incremental refactoring without breaking behavior
- Data persistence and serialization
- Time-based logic (due dates & overdue tasks)
- Undo functionality via deep copies and history tracking
- Separation of concerns (validation, helpers, core logic)
- Designing for extension rather than rewriting

This project intentionally avoids frameworks and advanced abstractions to focus on **fundamentals and reasoning**.

---

## 🗂 Data Model (Simplified)

Each task is represented as a dictionary:

```python
{
  "id": 1,
  "title": "Write README",
  "description": "Document the project",
  "due": "2024-02-10",
  "priority": "medium",
  "status": "todo"
}
```
## How to run
```bash
python taskforge.py
```

## Available Commands
```bash
add                   - Create a new task
list                  - Show all tasks
update                - Update task status
delete                - Delete a task by ID
filter by status      - Filter tasks by status
filter by priority    - Filter tasks by priority
overdue               - Show overdue tasks
view log              - Show task action logs
undo                  - Undo last action on a task
help                  - Show command list
exit                  - Exit the program
```
---

## 👤 Author

Built by **Ciprian**

This project is part of my learning journey in software engineering, focused on building complete systems and improving through iteration.
