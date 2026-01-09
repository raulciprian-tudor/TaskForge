import random

# Data
tasks = [
    {"id": 1, "title": "Write README", "status": "todo"},
    {"id": 2, "title": "Fix bug", "status": "in progress"},
]

# Task States
TODO = "todo"
IN_PROGRESS = "in progress"
DONE = "done"

ALLOWED_TRANSITIONS = {TODO: IN_PROGRESS, IN_PROGRESS: DONE}


# Show commands function
def show_menu():
    """Info: show CLI menu"""
    title = "COMMANDS"
    commands = [
        "- add: create a new task",
        "- list: show all tasks",
        "- update: change task status",
        "- delete: remove task",
        "- filter: show tasks by status",
        "- help: show commands",
        "- exit: quit program",
    ]

    width = 54

    print("|" + "-" * width + "|")
    print("|" + title.center(width) + "|")
    print("|" + "-" * width + "|")

    for line in commands:
        print("| " + line.ljust(width - 1) + "|")

    print("|" + "-" * width + "|")


# Validation logic
def get_non_empty(prompt):
    """Info: validation for task title input"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Task title cannot be empty.")


# Helpers
def find_task_by_id(task_id):
    """Info: helper to find task by id"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def next_id():
    """Info: helper to generate incremental id"""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# Core Logic
def create_task():
    """Info: function create task"""
    task_title = get_non_empty("Task name: ")

    new_id = next_id()
    tasks.append({"id": new_id, "title": task_title, "status": TODO})


def update_task():
    """Info: update task status"""
    task_id = get_non_empty("Enter the task ID to update: ")

    try:
        task_id = int(task_id)
    except ValueError:
        print("ID must be a number.")
        return

    # find task by ID
    target_task = find_task_by_id(task_id)
    if target_task:
        current = target_task["status"]

        if current not in ALLOWED_TRANSITIONS:
            print("Task is already DONE and cannot be updated.")
            return

        next_allowed = ALLOWED_TRANSITIONS[current]

        update_request = input(f"Set status to ({next_allowed})? ").strip()

        if update_request == next_allowed:
            target_task["status"] = next_allowed
            print(f"Task updated to {next_allowed}")
        else:
            print(f"Invalid status. You can only move to {next_allowed}")
        return
    else:
        print("Task not found.")


def delete_task():
    """Info: remove task"""
    task_id = get_non_empty("Enter task ID to delete: ")

    try:
        task_id = int(task_id)
    except ValueError:
        print("ID must be a number.")
        return

    # find task by ID
    target_task = find_task_by_id(task_id)

    if target_task:
        tasks.remove(target_task)
        print("Task deleted.")
    else:
        print("Task not found.")


def filter_tasks():
    """Info: filter task by status"""
    task_status = input("Enter task STATUS to filter: ").strip()
    found = False

    if task_status not in [TODO, IN_PROGRESS, DONE]:
        print(f"Invalid status. Must be one of: {TODO, IN_PROGRESS, DONE}")
        return

    for task in tasks:
        if task["status"] == task_status:
            print(task)
            found = True
    if not found:
        print("Task not found.")


def show_all():
    """Info: show all tasks"""
    for task in tasks:
        print("-----TASK-----")
        print(f"ID : {task['id']}")
        print(f"TITLE: {task['title']}")
        print(f"STATUS: {task['status']}")
        print("-----------------")


show_menu()
while True:
    command = input("Command: ")

    if command == "add":
        create_task()
    elif command == "list":
        show_all()
    elif command == "update":
        update_task()
    elif command == "delete":
        delete_task()
    elif command == "filter":
        filter_tasks()
    elif command == "help":
        show_menu()
    elif command == "exit":
        print("Quitting program...")
        break
