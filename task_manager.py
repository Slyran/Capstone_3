from datetime import date
from datetime import datetime

# Checks that the user is the administrator, gets info
# for the new user and saves it to the user.txt file
def reg_user():
    users = []
    with open("user.txt", "a+") as file:
        file.seek(0)
        file_lines = file.readlines()
        for line in file_lines:
            users.append(line.split(", ")[0])
        if username == "admin": 
            while True:    
                new_username = input("Enter the username to register: ")
                if new_username not in users:
                    break
                else:
                    print("\n\33[31mUser already exists! Choose another name.\33[0m\n")
            new_password = input("Enter new password: ")
            if input("Enter password again: ") == new_password:
                file.write(f"\n{new_username}, {new_password}")
                print("\n\33[32mUser registered successfully\33[0m\n")
            else:
                print("\n\33[31mOops, those passwords weren't the same.\33[0m\n")
        else:
            print("\n\33[31mOnly the administrator can register a new user.\33[0m\n")

# Gets the user to input details for a new task and
# saves it to the tasks.txt file
def add_task():
    current_date = date.today().strftime("%d %b %Y")
    task_user = input("Which user is the task assigned to: ")
    task_title = input("Enter task title: ")
    task_description = input("Enter task discription: ")
    task_due = input("Enter task due date DD MMM YYYY: ")
    with open("tasks.txt", "a") as file:
        file.write(f"\n{task_user}, {task_title}, {task_description}, {current_date}, {task_due}, No")

# Prints a selected task in an easy to read format
def display_task(task):
    task = task.strip("\n").split(", ")
    print(f"""
Task:                   {task[1]}
Assigned to:            {task[0]}
Date assigned:          {task[3]}
Due date:               {task[4]}
Task Complete?          {task[5]}
Task description:
  {task[2]}""")

# Displays every task in the task.txt file
def view_all():
    with open("tasks.txt", "r") as file:
            task_list = file.readlines()
            for task in task_list:
                display_task(task)

# Checks the tasks.txt file for tasks assigned to the
# active user and displays the relevant tasks
def view_mine():
    with open("tasks.txt", "r") as file:
        task_list = file.readlines()
    print("")
    user_task_list = [(i, task) for i, task in enumerate(task_list) if task.split(", ")[0] == username]
    for j, task in enumerate(user_task_list, start=1):
        print(f"\n\33[4mTask Number: {j}\33[0m", end="")
        display_task(task[1])
    if len(user_task_list) == 0:
        print("\n\33[31mYou have no assigned tasks yet\33[0m\n")
    else:
        # Prompts the user to select a task to modify
        task_selection = int(input("""
Enter a task number to modify that task or mark as completed
Enter -1 to return to main menu
: """))
        if task_selection == -1:
            return
        elif task_selection in range(len(user_task_list)+1):
            index = user_task_list[task_selection-1][0]
            modify_task(index)

# Provides a menu of task modification options for the user
def modify_task(index):
    while True:
        task_options = input("""
m - Mark task as complete
e - Edit task
r - return to main menu
    : """).lower()
        if task_options == "m":
            mark_as_complete(index)
            return
        elif task_options == "e":
            edit_task(index)
            return
        elif task_options == "r":
            return
        else:
            print("\n\33[31mInvalid input, try again\33[0m")

# Marks the task at the given index as complete
def mark_as_complete(index):
    with open("tasks.txt", "r+") as file:
        task_list = file.readlines()
        split_task = task_list[index].split(", ")
        split_task[5] = "Yes"
        task_list[index] = ", ".join(split_task)
        file.seek(0)
        for line in task_list:
            file.write(line)
        print("\n\33[32mTask marked as complete\33[0m\n")

# Allows the user to change the user and/or the
# due date for the selected task
def edit_task(index):
    with open("tasks.txt", "r+") as file:
        task_list = file.readlines()
        split_task = task_list[index].split(", ")
        new_user = input("Enter new user for the task to be assigned to, or press enter to skip: ")
        if new_user != "":
            split_task[0] = new_user
        new_due_date = input("Enter new due date for the task (DD MMM YYYY), or press enter to skip: ")
        if new_due_date != "":
            split_task[4] = new_due_date
        task_list[index] = ", ".join(split_task)
        file.seek(0)
        for line in task_list:
            file.write(line)

# Display the contents of the task_overview.txt and 
# user_overview.txt files
def display_stats():
        with open("task_overview.txt", "r") as task_overview, open("user_overview.txt", "r") as user_overview:
            print(f"\n\33[4mTask Overview\33[0m\n{task_overview.read()}")
            print(f"\n\33[4mUser Overview\33[0m\n{user_overview.read()}")

# Generate statistics reports from the information in the
# tasks.txt, and user.txt files
def generate_reports():
    with open("tasks.txt", "r") as task_file, open("user.txt", "r") as user_file:    
        task_list = task_file.readlines()
        user_list = user_file.readlines()
    split_tasks = [task.split(", ") for task in task_list]
    split_users = [users.split(", ") for users in user_list]
    generate_task_report(split_tasks)
    generate_user_report(split_users, split_tasks)

# Generates the statistics report from the tasks.txt file
# and stores the report in the task_overview.txt file
def generate_task_report(split_task_list):
    total_tasks = len(split_task_list)
    incomplete_tasks = 0
    overdue_tasks = 0
    for task in split_task_list:
        if task[5].strip("\n") == "No":
            incomplete_tasks += 1
            if datetime.strptime(task[4], "%d %b %Y") < datetime.today():
                overdue_tasks += 1
    with open("task_overview.txt", "w") as file:
        if total_tasks != 0:
            file.write(f"""Total tasks: {total_tasks}
Complete Tasks: {total_tasks-incomplete_tasks}
Incompete Tasks: {incomplete_tasks}
Overdue Tasks: {overdue_tasks}
Percentage incomplete: {round(incomplete_tasks/total_tasks * 100, 2)}%
Percentage Overdue: {round(overdue_tasks/total_tasks * 100, 2)}%""")
        else:
            print("\33[31mError, no tasks found in tasks.txt\33[0m")

# Generates a statistics report for each user in the
# user.txt file, and saves the reports to the user_overview.txt file
def generate_user_report(split_user_list, split_task_list):
    total_users = len(split_user_list)
    total_tasks = len(split_task_list)
    with open("user_overview.txt", "w") as file:
        file.write(f"Total users: {total_users}")
        for user in split_user_list:
            user_tasks = 0
            incomplete_tasks = 0
            overdue_tasks = 0
            for task in split_task_list:
                if user[0] == task[0]:
                    user_tasks += 1
                    if task[5].strip("\n") == "No":
                        incomplete_tasks += 1
                        if datetime.strptime(task[4], "%d %b %Y") < datetime.today():
                             overdue_tasks += 1
            if user_tasks == 0:
                file.write(f"\n{'-'*60}\nUser: {user[0]}\nTasks: No tasks assigned to this user")
            else:
                file.write(f"""\n{"-"*60}
User: {user[0]}
Percentage of all tasks assigned to user: {round(user_tasks/total_tasks * 100, 2)}%
User tasks complete: {round((user_tasks-incomplete_tasks)/user_tasks * 100, 2)}%
User tasks incomplete: {round(incomplete_tasks/user_tasks * 100, 2)}%
User tasks overdue: {round(overdue_tasks/user_tasks * 100, 2)}%""")            


# Creates a dictionary from the data in user.txt
login_info = {}
with open("user.txt", "r") as file:
    file_lines = file.readlines()
    for line in file_lines:
        k, v = line.split(", ")
        login_info[k] = v.strip("\n")

# Gets the user to log in    
while True:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in login_info:
        if login_info[username] == password:
            print("\n\33[32mLog in successful\33[0m\n")
            break
    print("\n\33[31mIncorrect details, please try again\33[0m\n")


while True:
    # Presents the menu to the user and makes
    # sure that the user input is converted to lower case.
    print(f'''{'-'*60}
Select one of the following options:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task''')
    if username == "admin":
        print("""gr - Generate reports (admin)
ds - Display statistics (admin)""")
    print(f"""e - Exit
{'-'*60}""")
    menu = input(": ")
    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == "gr" and username == "admin":
        generate_reports()

    elif menu == "ds" and username == "admin":
        try:
            display_stats()
        except FileNotFoundError:
            generate_reports()
            display_stats()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("\n\33[31mYou have made a wrong choice, please try again\33[0m")