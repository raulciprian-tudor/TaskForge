from datetime import datetime
from datetime import date
import json
from copy import deepcopy

# JSON data
TASK_FILE = "./json/tasks.json"

# Task States
TODO = "todo"
IN_PROGRESS = "in progress"
DONE = "done"

LOW = "low"
MEDIUM = "medium"
HIGH = "high"

# FLOWS
ALLOWED_TRANSITIONS = {TODO: IN_PROGRESS, IN_PROGRESS: DONE}
PRIORITY_FLOW = {LOW: MEDIUM, MEDIUM: HIGH}

# LOGGER
logger = []
history = {}


# Show commands function
def show_menu():
    """Info: show CLI menu"""
    title = "COMMANDS"
    commands = [
        "- add: create a new task",
        "- list: show all tasks",
        "- update: change task status",
        "- delete: remove task",
        "- filter by status: show tasks by status",
        "- filter by priority: show tasks by priority",
        "- overdue: show tasks that are overdue",
        "- view log: show logs",
        "- undo: undo last action",
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


# Load data on program initialization
def load_task():
    """Info: load data on start"""
    try:
        with open(TASK_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    # convert due date strings to date objects
    for task in data:
        if isinstance(task.get("due"), str):
            task["due"] = datetime.strptime(task["due"], "%Y-%m-%d").date()

    return data


# load data
tasks = load_task()


# Logger
def add_log(task, action):
    """Info: log activity"""
    global logger

    logger.append(
        {
            "task": task,
            "action": action,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def show_log():
    """Info: show logs"""
    global logger

    for entry in logger:
        print(entry)


# Validation logic
def get_non_empty(prompt):
    """Info: validation for task title input"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Task title cannot be empty.")


def get_valid_date(prompt):
    """Info: validation for date input"""
    while True:
        value = get_non_empty(prompt)
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")


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


def priority_order():
    """Info: define priority order"""
    order = []
    current = LOW

    while current:
        order.append(current)
        current = PRIORITY_FLOW.get(current)

    return order


def snapshot(task):
    """Info: save action"""
    task_id = task["id"]

    if task_id not in history:
        history[task_id] = []

    history[task_id].append(deepcopy(task))


# Core Logic
def save_tasks(tasks):
    """Info: save data to json"""
    serializable = []
    for task in tasks:
        new_task = task.copy()
        if hasattr(new_task["due"], "isoformat"):
            new_task["due"] = new_task["due"].isoformat()
        serializable.append(new_task)

    with open(TASK_FILE, "w") as f:
        json.dump(serializable, f, indent=2)


def create_task():
    """Info: function create task"""
    task_title = get_non_empty("Enter task name: ")
    task_description = get_non_empty("Enter task description: ")
    task_due_date = get_valid_date("Enter task due date (YYYY-MM-DD): ")
    task_priority = get_non_empty("Enter task priority (LOW | MEDIUM | HIGH): ")

    new_id = next_id()
    tasks.append(
        {
            "id": new_id,
            "title": task_title,
            "description": task_description,
            "due": task_due_date,
            "priority": task_priority,
            "status": TODO,
        }
    )
    save_tasks(tasks)
    add_log(task_title, "added task")


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
            add_log(target_task, "attempted update on task that was already DONE.")
            return

        next_allowed = ALLOWED_TRANSITIONS[current]

        update_request = input(f"Set status to ({next_allowed})? ").strip()

        if update_request == next_allowed:
            snapshot(target_task)
            add_log(target_task, "updated task status")
            target_task["status"] = next_allowed
            save_tasks(tasks)
            print(f"Task updated to {next_allowed}")
        else:
            add_log(target_task, "invalid status")
            print(f"Invalid status. You can only move to {next_allowed}")
        return
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
        snapshot(target_task)
        add_log(target_task, "removed task")
        tasks.remove(target_task)
        save_tasks(tasks)
        print("Task deleted.")
    else:
        print("Task not found.")


def filter_by_status():
    """Info: filter tasks by status"""
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


def filter_by_priority():
    """Info: filter tasks by priority"""

    order = priority_order()

    for p in order:
        print(f"\n=== {p.upper()} PRIORITY ===")
        filtered = [task for task in tasks if task["priority"] == p]

        if not filtered:
            print("No tasks.")
            return

        for task in filtered:
            print(f"- {task['id']} | {task['title']} (due: {task['due']})")


def overdue_tasks():
    """Info: show list of all overdue tasks"""
    today = date.today()
    overdue = [task for task in tasks if task["due"] < today]

    if not overdue:
        print("No overdue tasks.")
        return

    print("Overdue tasks:")
    for task in overdue:
        print(f"- {task['id']} | {task['title']} (Due: {task['due']})")


def show_all():
    """Info: show all tasks"""
    if tasks:
        for task in tasks:
            print("-----TASK-----")
            print(f"ID : {task['id']}")
            print(f"TITLE: {task['title']}")
            print(f"DESCRIPTION: {task['description']}")
            print(f"DUE DATE: {task['due']}")
            print(f"PRIORITY: {task['priority']}")
            print(f"STATUS: {task['status']}")
            print("-----------------")
        return

    print("No tasks found.")


def undo_task():
    """Info: undo action on task by id"""
    task_id = get_non_empty("Enter the task ID to undo: ")

    try:
        task_id = int(task_id)
    except ValueError:
        print("ID must be a number")
        return

    if task_id not in history or len(history[task_id]) == 0:
        print("No undo info for this task.")
        return

    last_state = history[task_id].pop()

    task = find_task_by_id(task_id)

    if task:
        task.clear()
        task.update(last_state)
    else:
        tasks.append(last_state)

    add_log(last_state, "undo")
    save_tasks(tasks)
    print("Undo complete.")


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
    elif command == "filter by status":
        filter_by_status()
    elif command == "filter by priority":
        filter_by_priority()
    elif command == "overdue":
        overdue_tasks()
    elif command == "view log":
        show_log()
    elif command == "undo":
        print(history)
        if history:
            undo_task()
        else:
            print("There are no actions to undo.")
    elif command == "help":
        show_menu()
    elif command == "exit":
        print("Quitting program...")
        break
