# Data
tasks = [
    {"id": 1, "title": "Write README", "status": "todo"},
    {"id": 2, "title": "Fix bug", "status": "in_progress"},
]

# Task States
TODO = "todo"
IN_PROGRESS = "in_progress"
DONE = "done"


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

    width = 54  # inside width

    print("|" + "-" * width + "|")
    print("|" + title.center(width) + "|")
    print("|" + "-" * width + "|")

    for line in commands:
        print("| " + line.ljust(width - 1) + "|")

    print("|" + "-" * width + "|")


show_menu()

# while True:
