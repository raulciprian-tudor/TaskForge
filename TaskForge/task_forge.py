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


# Core Logic
def create_task():
    """Info: function create task"""
    task_title = get_non_empty("Task name: ")

    while True:
        secret_id = random.randrange(0, 99999999)
        if secret_id not in [task["id"] for task in tasks]:
            break
    tasks.append({"id": secret_id, "title": task_title, "status": TODO})


def update_task():
    """Info: update task status"""
    task_title = get_non_empty("Task name: ")

    # find task by title
    for task in tasks:
        if task["title"] == task_title:
            current = task["status"]

            # show allowed next state
            if current == TODO:
                next_allowed = IN_PROGRESS
            elif current == IN_PROGRESS:
                next_allowed = DONE
            else:
                print("Task is already DONE and cannot be updated.")
                return

            update_request = input(f"Set status to ({next_allowed})? ").strip()

            if update_request == next_allowed:
                task["status"] = next_allowed
                print(f"Task updated to {next_allowed}")
            else:
                print(f"Invalid status. You can only move to {next_allowed}")
            return

    print("Task not found.")


show_menu()
while True:
    command = input("Command: ")

    if command == "add":
        create_task()
    elif command == "list":
        print("show all tasks")
    elif command == "update":
        update_task()
    elif command == "delete":
        print("remove task")
    elif command == "filter":
        print("show tasks by status")
    elif command == "help":
        show_menu()
    elif command == "exit":
        print("Quitting program...")
        break
