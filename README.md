# Task Manager by Arpith Mishra

#### Video Demo: https://youtu.be/3WGXeWHXQeQ

#### Description:
I created this project to help me with keeping track of my tasks. After creating an account, one can:
- Create tasks
- Assign them descriptions, due dates, priority (high, medium, low), and categories
- Edit tasks and mark them as complete
- View all the tasks that need to be completed by the end of a certain day
- View all the tasks that they have created (sorted by due date) along with their descriptions, due dates, priorities, and categories
- View a history of all the tasks that they have completed sorted by the completion date

FILES:
- app.py: This file contains all the necessary routes and functions to make the program usable. I used the same apology function and the same login_required function as Finance. The routes it contains are:
--- "/" (Homepage, where user views incomplete tasks ordered by due date)
--- "/login": (Allows user to log in [Almost identical to the "/login" of Finance])
--- "/logout": (Allows the user to log out [Identical to the "/logout" of Finance])
--- "/register": (Allows the user to register [Almost identical to the "/register" of Finance])
--- "/add_task": Allows the user to add a task
--- "/edit_task": Allows the user to edit tasks
--- "/tasks_today": Allows the user to view overdue tasks and tasks due on that day ordered by both priority and due date
--- "/history": Allows the user to view every task that they ever completed ordered by completion date

- project.db: This database is used to store all the information that the user provides. It has two tables: users and tasks.
--- Users: This table contains an ID which autoincrements, an unique username, and a hashed password for each user
--- Tasks: This table contains every task ever added used the website. Each row of the table has an unique id, the user's id from users, the name of the task, an optional description of the task, the due date of the task both in date and text format, the status of the task (complete or incomplete), the priority of the task (low, medium, or high), the category of the task, the date the task was created, and a placeholder for when the task was completed in date and text format.

- requirements.txt: This file just contains Flask

- README.md: This file contains a description of all the files and their function

- Templates:
--- layout.html: This file serves as the layout for every other file in the program. It imports Bootstrap, creates a working navigation bar which can take the user to different routes (which change based on whether the user is logged in or not), and it outlines how the files should respond to messages from the 'flash' function.
--- apology.html: This file is essentially the error message for when the user does something wrong. This file is exactly the same as the one from Finance.
--- register.html: This file allows the user to register. It is almost the same as the "register.html" from Finance
--- login.html: This file allows the user to log in to their accounts. It is almost the same as the "login.html" from Finance
--- index.html: This file displays all of the users incomplete tasks. It has a table which displays every incomplete task, an optional description of the task, a due date, a priority from low to high, and a category. It also has a button which prompts the user to edit a task or create a new task.
--- add_task.html: This file prompts the user to enter a task, an optional description, a due date, a category, and a priority from low to high. The file then submits that information to app.py, where it is sent to project.db.
--- edit_task.html: This file allows the user to edit tasks. It prompts the user to enter an action: the actions it can take are marking a task as complete, deleting a task, changing the description of a task, changing the due date of a task, changing the priority of a task, and changing the category of a task. Based on what option the user selects, Javascript makes different inputs visible, and prompts the user to sumbit information to app.py, and eventually modify project.db.
--- tasks_today.html: This file takes information from project.db to tell the user all of the tasks that they need to complete by the end of the day, which includes tasks due that day and overdue tasks. It also provides the user with the information in the "edit_task.html" file about each task. The tasks are ordered based on priority and due date.
--- history.html: This file takes information project.db and shows the user every task that they have completed, along with all of its information. The tasks are sorted based on completion date.

#### Acknowledgments
I used Grok (xAI's AI assistant) to help with UI styling (Bootstrap layouts, dynamic row coloring, card designs), template consistency, and minor code improvements. The core functionality, database design, and feature logic are my own work.
