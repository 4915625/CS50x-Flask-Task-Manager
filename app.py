from cs50 import SQL

from datetime import datetime, date
from flask import Flask,  flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    today = date.today()
    tasks = db.execute("SELECT *, JULIANDAY(due_date) - JULIANDAY(?) AS days_until_due FROM tasks WHERE user_id = ? AND status = 'incomplete' ORDER BY due_date ASC", today, user_id)
    return render_template("index.html", tasks=tasks)



@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if username == "" or username == None:
            return apology("Error: Invalid Username")
        if password == "" or password == None:
            return apology("Error: Invalid Password")
        if confirmation == "" or confirmation == None:
            return apology("Error: Invalid Confirmation Password")
        if password != confirmation:
            return apology("Error: Passwords do not match")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Error: Username is taken")
        hash = generate_password_hash(password, method='scrypt', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        user_id = session["user_id"]
        task = request.form.get("task")
        description = request.form.get("description")
        due_date_str = request.form.get("due_date")
        priority = request.form.get("priority")
        category = request.form.get("category")
        current_date = datetime.now()

        if not task:
            return apology("Please enter a task")
        if not due_date_str:
            return apology("Please enter a due date")
        if not description:
            description = "N/A"
        if not priority:
            priority = "medium"
        if not category:
            category = "uncategorized"

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            due_date_formatted = due_date.strftime('%B %d, %Y')
            today_date_formatted = current_date.strftime('%B %d, %Y')
        except ValueError:
            return apology("Invalid date format")

        db.execute("INSERT INTO tasks (user_id, task, description, status, due_date, due_date_text, priority, category, created_date) VALUES (?, ?, ?, 'incomplete', ?, ?, ?, ?, ?)", user_id, task, description, due_date, due_date_formatted, priority, category, today_date_formatted)
        flash(f"Task '{task}' (Due {due_date_formatted}) successfully added!")
        return redirect("/")

    else:
        return render_template("add_task.html")


@app.route("/edit_task", methods=["GET", "POST"])
@login_required
def edit_task():
    user_id = session["user_id"]

    if request.method == "POST":
        action = request.form.get("action")
        task = request.form.get("task")
        new_description = request.form.get("new-description")
        new_due_date_str = request.form.get("new-due-date")
        new_priority = request.form.get("new-priority")
        new_category = request.form.get("new-category")
        today = date.today()
        today_text = today.strftime('%B %d, %Y')

        valid_actions = ["complete", "delete", "modify-description", "modify-due-date", "modify-priority", "modify-category"]
        if not action:
            return apology("Must select an action")
        if action not in valid_actions:
            return apology("Invalid action")
        if not task:
            return apology("Must select a task")

        user_tasks = db.execute("SELECT task FROM tasks WHERE user_id = ? AND status = 'incomplete'", user_id)
        task_list = [row["task"] for row in user_tasks]
        if task not in task_list:
            return apology("Invalid or already completed task")

        if action == "complete":
            db.execute("UPDATE tasks SET status = 'complete', completion_date = ?, completion_date_text = ? WHERE user_id = ? AND task = ?", today, today_text, user_id, task)
            flash(f"Task '{task}' marked as complete!")

        elif action == "delete":
            db.execute("DELETE FROM tasks WHERE user_id = ? AND task = ?", user_id, task)
            flash(f"Task '{task}' deleted!")

        elif action == "modify-description":
            if not new_description:
                return apology("Must enter a new description")
            db.execute("UPDATE tasks SET description = ? WHERE user_id = ? AND task = ?", new_description, user_id, task)
            flash(f"Description for '{task}' updated!")

        elif action == "modify-due-date":
            if not new_due_date_str:
                return apology("Must select a new due date")
            try:
                due_date = datetime.strptime(new_due_date_str, '%Y-%m-%d')
                due_date_formatted = due_date.strftime('%B %d, %Y')
            except ValueError:
                return apology("Invalid date format")

            db.execute("UPDATE tasks SET due_date = ?, due_date_text = ? WHERE user_id = ? AND task = ?", due_date, due_date_formatted, user_id, task)
            flash(f"Due date for '{task}' updated to {due_date_formatted}!")

        elif action == "modify-priority":
            if not new_priority:
                return apology("Must select a new priority")
            priorities = ["Low", "Medium", "High"]
            if new_priority not in priorities:
                return apology("Invalid priority")
            db.execute("UPDATE tasks SET priority = ? WHERE user_id = ? AND task = ?", new_priority, user_id, task)
            flash(f"Priority for Task '{task}' changed to {new_priority}!")

        elif action == "modify-category":
            if not new_category:
                return apology("Must select a new category")
            db.execute("UPDATE tasks SET category = ? WHERE user_id = ? AND task = ?", new_category, user_id, task)
            flash(f"Category for Task '{task}' changed to {new_category}!")

        return redirect("/")

    else:
        tasks = db.execute("SELECT task FROM tasks WHERE user_id = ? AND status = 'incomplete'", user_id)
        return render_template("edit_task.html", tasks=tasks)


@app.route("/tasks_today")
@login_required
def tasks_today():
    user_id = session["user_id"]
    date_today = date.today()
    date_today_text = date_today.strftime('%B %d, %Y')

    tasks_due = db.execute("SELECT *, JULIANDAY(due_date) - JULIANDAY(?) AS days_until_due FROM tasks WHERE user_id = ? AND status = 'incomplete' ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END, due_date ASC", date_today, user_id)

    focus_tasks = [t for t in tasks_due if t["days_until_due"] <= 0]

    return render_template("tasks_today.html", today=date_today, today_text=date_today_text, tasks=focus_tasks)


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    tasks_completed = db.execute("SELECT * FROM tasks WHERE user_id = ? AND status = 'complete' ORDER BY completion_date DESC", user_id)
    return render_template("history.html", tasks=tasks_completed)



if __name__ == "__main__":
    app.run(debug=False)
