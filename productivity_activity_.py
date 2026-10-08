import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector



MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"
MYSQL_DATABASE = "productivity_db"




def connect_database():

    try:

        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        return connection

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            "Unable to connect to MySQL.\n\n" + str(e)
        )

        return None


# ============================================================
# GLOBAL USER
# ============================================================

current_user_id = None
current_username = ""




def login():

    global current_user_id
    global current_username

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "" or password == "":

        messagebox.showwarning(
            "Missing Information",
            "Please enter username and password."
        )

        return

    connection = connect_database()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        query = """
            SELECT id, username
            FROM users
            WHERE username = %s AND password = %s
        """

        cursor.execute(
            query,
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            current_user_id = user[0]
            current_username = user[1]

            messagebox.showinfo(
                "Login Successful",
                "Welcome " + current_username + "!"
            )

            open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    except Exception as e:

        messagebox.showerror(
            "Login Error",
            str(e)
        )



def clear_login():

    username_entry.delete(
        0,
        tk.END
    )

    password_entry.delete(
        0,
        tk.END
    )

    username_entry.focus()




def open_registration():

    registration_window = tk.Toplevel(login_window)

    registration_window.title(
        "User Registration"
    )

    registration_window.geometry(
        "450x550"
    )

    registration_window.configure(
        bg="#F4F7FB"
    )

    registration_window.resizable(
        False,
        False
    )

    # HEADER

    header = tk.Frame(
        registration_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    title = tk.Label(
        header,
        text="USER REGISTRATION",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    )

    title.pack(
        pady=20
    )

    # FORM

    form = tk.Frame(
        registration_window,
        bg="white"
    )

    form.pack(
        padx=30,
        pady=30,
        fill="both",
        expand=True
    )

    # NAME

    tk.Label(
        form,
        text="Full Name",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#444444"
    ).pack(
        anchor="w",
        padx=25,
        pady=(25, 5)
    )

    name_entry = tk.Entry(
        form,
        font=("Arial", 11),
        bg="#F4F7FB",
        relief="flat"
    )

    name_entry.pack(
        padx=25,
        fill="x",
        ipady=8
    )

    # USERNAME

    tk.Label(
        form,
        text="Username",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#444444"
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    reg_username_entry = tk.Entry(
        form,
        font=("Arial", 11),
        bg="#F4F7FB",
        relief="flat"
    )

    reg_username_entry.pack(
        padx=25,
        fill="x",
        ipady=8
    )

    # PASSWORD

    tk.Label(
        form,
        text="Password",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#444444"
    ).pack(
        anchor="w",
        padx=25,
        pady=(15, 5)
    )

    reg_password_entry = tk.Entry(
        form,
        font=("Arial", 11),
        bg="#F4F7FB",
        relief="flat",
        show="*"
    )

    reg_password_entry.pack(
        padx=25,
        fill="x",
        ipady=8
    )

    # REGISTER FUNCTION

    def register_user():

        name = name_entry.get().strip()
        username = reg_username_entry.get().strip()
        password = reg_password_entry.get()

        if name == "" or username == "" or password == "":

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            check_query = """
                SELECT id
                FROM users
                WHERE username = %s
            """

            cursor.execute(
                check_query,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                messagebox.showwarning(
                    "Username Exists",
                    "This username already exists."
                )

                cursor.close()
                connection.close()

                return

            query = """
                INSERT INTO users
                (
                    full_name,
                    username,
                    password
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    name,
                    username,
                    password
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully."
            )

            registration_window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Registration Error",
                str(e)
            )

    # BUTTON

    register_button = tk.Button(
        form,
        text="REGISTER",
        font=("Arial", 11, "bold"),
        bg="#243B6B",
        fg="white",
        relief="flat",
        padx=25,
        pady=10,
        command=register_user
    )

    register_button.pack(
        pady=30
    )



def open_task_management():

    task_window = tk.Toplevel(login_window)

    task_window.title(
        "Task Management"
    )

    task_window.geometry(
        "1000x700"
    )

    task_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        task_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="TASK MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=(15, 3)
    )

    tk.Label(
        header,
        text="Add, update, complete and delete your tasks",
        font=("Arial", 10),
        bg="#243B6B",
        fg="#DCE6FF"
    ).pack(
        pady=(0, 15)
    )

    # MAIN

    main_frame = tk.Frame(
        task_window,
        bg="#F4F7FB"
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    # FORM

    form = tk.Frame(
        main_frame,
        bg="white"
    )

    form.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        form,
        text="Task Title",
        font=("Arial", 10, "bold"),
        bg="white"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    task_title_entry = tk.Entry(
        form,
        width=25,
        font=("Arial", 10)
    )

    task_title_entry.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    tk.Label(
        form,
        text="Priority",
        font=("Arial", 10, "bold"),
        bg="white"
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    priority_combo = ttk.Combobox(
        form,
        values=[
            "High",
            "Medium",
            "Low"
        ],
        state="readonly",
        width=12
    )

    priority_combo.set("Medium")

    priority_combo.grid(
        row=0,
        column=3,
        padx=10
    )

    tk.Label(
        form,
        text="Due Date",
        font=("Arial", 10, "bold"),
        bg="white"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    due_date_entry = tk.Entry(
        form,
        width=25,
        font=("Arial", 10)
    )

    due_date_entry.grid(
        row=1,
        column=1,
        padx=10
    )

    tk.Label(
        form,
        text="Due Time",
        font=("Arial", 10, "bold"),
        bg="white"
    ).grid(
        row=1,
        column=2,
        padx=10
    )

    due_time_entry = tk.Entry(
        form,
        width=15,
        font=("Arial", 10)
    )

    due_time_entry.grid(
        row=1,
        column=3,
        padx=10
    )

    selected_task_id = tk.StringVar()

    # CLEAR FORM

    def clear_form():

        selected_task_id.set("")

        task_title_entry.delete(
            0,
            tk.END
        )

        priority_combo.set("Medium")

        due_date_entry.delete(
            0,
            tk.END
        )

        due_time_entry.delete(
            0,
            tk.END
        )

        task_title_entry.focus()

    # LOAD TASKS

    def load_tasks():

        for item in tree.get_children():

            tree.delete(item)

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    id,
                    title,
                    priority,
                    status,
                    due_date,
                    due_time
                FROM tasks
                WHERE user_id = %s
                ORDER BY id DESC
            """

            cursor.execute(
                query,
                (current_user_id,)
            )

            records = cursor.fetchall()

            for record in records:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ADD TASK

    def add_task():

        title = task_title_entry.get().strip()
        priority = priority_combo.get()
        due_date = due_date_entry.get().strip()
        due_time = due_time_entry.get().strip()

        if title == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter task title."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO tasks
                (
                    user_id,
                    title,
                    priority,
                    status,
                    due_date,
                    due_time
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    'Pending',
                    %s,
                    %s
                )
            """

            cursor.execute(
                query,
                (
                    current_user_id,
                    title,
                    priority,
                    due_date,
                    due_time
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Task added successfully."
            )

            clear_form()
            load_tasks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # UPDATE TASK

    def update_task():

        task_id = selected_task_id.get()

        if task_id == "":

            messagebox.showwarning(
                "Select Task",
                "Please select a task first."
            )

            return

        title = task_title_entry.get().strip()
        priority = priority_combo.get()
        due_date = due_date_entry.get().strip()
        due_time = due_time_entry.get().strip()

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE tasks
                SET
                    title = %s,
                    priority = %s,
                    due_date = %s,
                    due_time = %s
                WHERE id = %s
                AND user_id = %s
            """

            cursor.execute(
                query,
                (
                    title,
                    priority,
                    due_date,
                    due_time,
                    task_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Task updated successfully."
            )

            clear_form()
            load_tasks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DELETE TASK

    def delete_task():

        task_id = selected_task_id.get()

        if task_id == "":

            messagebox.showwarning(
                "Select Task",
                "Please select a task first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?"
        )

        if not confirm:
            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                DELETE FROM tasks
                WHERE id = %s
                AND user_id = %s
            """

            cursor.execute(
                query,
                (
                    task_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Task deleted successfully."
            )

            clear_form()
            load_tasks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # COMPLETE TASK

    def complete_task():

        task_id = selected_task_id.get()

        if task_id == "":

            messagebox.showwarning(
                "Select Task",
                "Please select a task first."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE tasks
                SET status = 'Completed'
                WHERE id = %s
                AND user_id = %s
            """

            cursor.execute(
                query,
                (
                    task_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Task marked as completed."
            )

            load_tasks()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # BUTTONS

    button_frame = tk.Frame(
        form,
        bg="white"
    )

    button_frame.grid(
        row=2,
        column=0,
        columnspan=4,
        pady=15
    )

    tk.Button(
        button_frame,
        text="ADD TASK",
        bg="#243B6B",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=add_task
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="UPDATE",
        bg="#3A6EA5",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=update_task
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="COMPLETE",
        bg="#2E7D32",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=complete_task
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="DELETE",
        bg="#C62828",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=delete_task
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="CLEAR",
        bg="#777777",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=clear_form
    ).pack(
        side="left",
        padx=5
    )

    # TABLE

    table_frame = tk.Frame(
        main_frame,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True
    )

    columns = (
        "ID",
        "Title",
        "Priority",
        "Status",
        "Due Date",
        "Due Time"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=130
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # SELECT RECORD

    def select_task(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(
            selected,
            "values"
        )

        if values:

            selected_task_id.set(
                values[0]
            )

            task_title_entry.delete(
                0,
                tk.END
            )

            task_title_entry.insert(
                0,
                values[1]
            )

            priority_combo.set(
                values[2]
            )

            due_date_entry.delete(
                0,
                tk.END
            )

            due_date_entry.insert(
                0,
                values[4]
            )

            due_time_entry.delete(
                0,
                tk.END
            )

            due_time_entry.insert(
                0,
                values[5]
            )

    tree.bind(
        "<ButtonRelease-1>",
        select_task
    )

    load_tasks()




def open_goal_management():

    goal_window = tk.Toplevel(login_window)

    goal_window.title(
        "Daily Goals"
    )

    goal_window.geometry(
        "850x600"
    )

    goal_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        goal_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="DAILY GOALS",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=15
    )

    # FORM

    form = tk.Frame(
        goal_window,
        bg="white"
    )

    form.pack(
        fill="x",
        padx=15,
        pady=15
    )

    tk.Label(
        form,
        text="Goal",
        font=("Arial", 10, "bold"),
        bg="white"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=15
    )

    goal_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 10)
    )

    goal_entry.grid(
        row=0,
        column=1,
        padx=10
    )

    selected_goal_id = tk.StringVar()

    # LOAD GOALS

    def load_goals():

        for item in tree.get_children():
            tree.delete(item)

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    id,
                    goal,
                    status,
                    goal_date
                FROM goals
                WHERE user_id = %s
                ORDER BY id DESC
            """

            cursor.execute(
                query,
                (current_user_id,)
            )

            records = cursor.fetchall()

            for record in records:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ADD GOAL

    def add_goal():

        goal = goal_entry.get().strip()

        if goal == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter a goal."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO goals
                (
                    user_id,
                    goal,
                    status,
                    goal_date
                )
                VALUES
                (
                    %s,
                    %s,
                    'Pending',
                    CURDATE()
                )
            """

            cursor.execute(
                query,
                (
                    current_user_id,
                    goal
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Daily goal added."
            )

            goal_entry.delete(
                0,
                tk.END
            )

            load_goals()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # COMPLETE GOAL

    def complete_goal():

        goal_id = selected_goal_id.get()

        if goal_id == "":

            messagebox.showwarning(
                "Select Goal",
                "Please select a goal."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE goals
                SET status = 'Completed'
                WHERE id = %s
                AND user_id = %s
            """

            cursor.execute(
                query,
                (
                    goal_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Goal completed."
            )

            load_goals()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DELETE GOAL

    def delete_goal():

        goal_id = selected_goal_id.get()

        if goal_id == "":
            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM goals
                WHERE id = %s
                AND user_id = %s
                """,
                (
                    goal_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            load_goals()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # BUTTONS

    tk.Button(
        form,
        text="ADD GOAL",
        bg="#243B6B",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=add_goal
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    tk.Button(
        form,
        text="COMPLETE",
        bg="#2E7D32",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=complete_goal
    ).grid(
        row=0,
        column=3,
        padx=5
    )

    tk.Button(
        form,
        text="DELETE",
        bg="#C62828",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=delete_goal
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    # TABLE

    table_frame = tk.Frame(
        goal_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )

    columns = (
        "ID",
        "Goal",
        "Status",
        "Date"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def select_goal(event):

        selected = tree.focus()

        if selected:

            values = tree.item(
                selected,
                "values"
            )

            selected_goal_id.set(
                values[0]
            )

    tree.bind(
        "<ButtonRelease-1>",
        select_goal
    )

    load_goals()




def open_habit_management():

    habit_window = tk.Toplevel(login_window)

    habit_window.title(
        "Habit Tracking"
    )

    habit_window.geometry(
        "850x600"
    )

    habit_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        habit_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="HABIT TRACKING",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=15
    )

    # FORM

    form = tk.Frame(
        habit_window,
        bg="white"
    )

    form.pack(
        fill="x",
        padx=15,
        pady=15
    )

    tk.Label(
        form,
        text="Habit Name",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(
        side="left",
        padx=10
    )

    habit_entry = tk.Entry(
        form,
        width=35,
        font=("Arial", 10)
    )

    habit_entry.pack(
        side="left",
        padx=10,
        ipady=5
    )

    selected_habit_id = tk.StringVar()

    # LOAD

    def load_habits():

        for item in tree.get_children():
            tree.delete(item)

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    habit_name,
                    status,
                    habit_date
                FROM habits
                WHERE user_id = %s
                ORDER BY id DESC
                """,
                (current_user_id,)
            )

            records = cursor.fetchall()

            for record in records:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ADD

    def add_habit():

        habit = habit_entry.get().strip()

        if habit == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter habit name."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO habits
                (
                    user_id,
                    habit_name,
                    status,
                    habit_date
                )
                VALUES
                (
                    %s,
                    %s,
                    'Pending',
                    CURDATE()
                )
                """,
                (
                    current_user_id,
                    habit
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            habit_entry.delete(
                0,
                tk.END
            )

            load_habits()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # COMPLETE

    def complete_habit():

        habit_id = selected_habit_id.get()

        if habit_id == "":
            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE habits
                SET status = 'Completed'
                WHERE id = %s
                AND user_id = %s
                """,
                (
                    habit_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            load_habits()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DELETE

    def delete_habit():

        habit_id = selected_habit_id.get()

        if habit_id == "":
            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM habits
                WHERE id = %s
                AND user_id = %s
                """,
                (
                    habit_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            load_habits()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # BUTTONS

    tk.Button(
        form,
        text="ADD HABIT",
        bg="#243B6B",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12,
        pady=7,
        command=add_habit
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        form,
        text="COMPLETE",
        bg="#2E7D32",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12,
        pady=7,
        command=complete_habit
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        form,
        text="DELETE",
        bg="#C62828",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=12,
        pady=7,
        command=delete_habit
    ).pack(
        side="left",
        padx=5
    )

    # TABLE

    table_frame = tk.Frame(
        habit_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    columns = (
        "ID",
        "Habit",
        "Status",
        "Date"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def select_habit(event):

        selected = tree.focus()

        if selected:

            values = tree.item(
                selected,
                "values"
            )

            selected_habit_id.set(
                values[0]
            )

    tree.bind(
        "<ButtonRelease-1>",
        select_habit
    )

    load_habits()




def open_activity_management():

    activity_window = tk.Toplevel(login_window)

    activity_window.title(
        "Daily Activity Management"
    )

    activity_window.geometry(
        "950x650"
    )

    activity_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        activity_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="DAILY ACTIVITY MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=15
    )

    # FORM

    form = tk.Frame(
        activity_window,
        bg="white"
    )

    form.pack(
        fill="x",
        padx=15,
        pady=15
    )

    tk.Label(
        form,
        text="Activity",
        bg="white",
        font=("Arial", 10, "bold")
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    activity_entry = tk.Entry(
        form,
        width=25
    )

    activity_entry.grid(
        row=0,
        column=1
    )

    tk.Label(
        form,
        text="Category",
        bg="white",
        font=("Arial", 10, "bold")
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    category_combo = ttk.Combobox(
        form,
        values=[
            "Study",
            "Work",
            "Exercise",
            "Personal",
            "Other"
        ],
        state="readonly",
        width=15
    )

    category_combo.set("Study")

    category_combo.grid(
        row=0,
        column=3
    )

    selected_activity_id = tk.StringVar()

    # LOAD

    def load_activities():

        for item in tree.get_children():
            tree.delete(item)

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    activity,
                    category,
                    activity_date
                FROM activities
                WHERE user_id = %s
                ORDER BY id DESC
                """,
                (current_user_id,)
            )

            records = cursor.fetchall()

            for record in records:

                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ADD

    def add_activity():

        activity = activity_entry.get().strip()
        category = category_combo.get()

        if activity == "":

            messagebox.showwarning(
                "Missing Information",
                "Please enter activity."
            )

            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO activities
                (
                    user_id,
                    activity,
                    category,
                    activity_date
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    CURDATE()
                )
                """,
                (
                    current_user_id,
                    activity,
                    category
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            activity_entry.delete(
                0,
                tk.END
            )

            load_activities()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DELETE

    def delete_activity():

        activity_id = selected_activity_id.get()

        if activity_id == "":
            return

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM activities
                WHERE id = %s
                AND user_id = %s
                """,
                (
                    activity_id,
                    current_user_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            load_activities()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        form,
        text="ADD ACTIVITY",
        bg="#243B6B",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=add_activity
    ).grid(
        row=0,
        column=4,
        padx=10
    )

    tk.Button(
        form,
        text="DELETE",
        bg="#C62828",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=15,
        pady=7,
        command=delete_activity
    ).grid(
        row=0,
        column=5,
        padx=5
    )

    # TABLE

    table_frame = tk.Frame(
        activity_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    columns = (
        "ID",
        "Activity",
        "Category",
        "Date"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=200
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def select_activity(event):

        selected = tree.focus()

        if selected:

            values = tree.item(
                selected,
                "values"
            )

            selected_activity_id.set(
                values[0]
            )

    tree.bind(
        "<ButtonRelease-1>",
        select_activity
    )

    load_activities()




def open_statistics():

    statistics_window = tk.Toplevel(login_window)

    statistics_window.title(
        "Productivity Statistics"
    )

    statistics_window.geometry(
        "700x550"
    )

    statistics_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        statistics_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="PRODUCTIVITY STATISTICS",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=15
    )

    # STATISTICS CARD

    card = tk.Frame(
        statistics_window,
        bg="white"
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0
    total_goals = 0
    completed_goals = 0
    total_habits = 0
    completed_habits = 0
    total_activities = 0

    connection = connect_database()

    if connection:

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                """,
                (current_user_id,)
            )

            total_tasks = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                AND status = 'Completed'
                """,
                (current_user_id,)
            )

            completed_tasks = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                AND status = 'Pending'
                """,
                (current_user_id,)
            )

            pending_tasks = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM goals
                WHERE user_id = %s
                """,
                (current_user_id,)
            )

            total_goals = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM goals
                WHERE user_id = %s
                AND status = 'Completed'
                """,
                (current_user_id,)
            )

            completed_goals = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM habits
                WHERE user_id = %s
                """,
                (current_user_id,)
            )

            total_habits = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM habits
                WHERE user_id = %s
                AND status = 'Completed'
                """,
                (current_user_id,)
            )

            completed_habits = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM activities
                WHERE user_id = %s
                """,
                (current_user_id,)
            )

            total_activities = cursor.fetchone()[0]

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Statistics Error",
                str(e)
            )

            return

    # CALCULATE PRODUCTIVITY

    if total_tasks > 0:

        productivity = (
            completed_tasks / total_tasks
        ) * 100

    else:

        productivity = 0

    # LABELS

    statistics = [
        ("Total Tasks", total_tasks),
        ("Completed Tasks", completed_tasks),
        ("Pending Tasks", pending_tasks),
        ("Total Goals", total_goals),
        ("Completed Goals", completed_goals),
        ("Total Habits", total_habits),
        ("Completed Habits", completed_habits),
        ("Total Activities", total_activities),
        (
            "Productivity",
            str(round(productivity, 2)) + "%"
        )
    ]

    for index, item in enumerate(statistics):

        label = tk.Label(
            card,
            text=item[0],
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#444444"
        )

        label.grid(
            row=index,
            column=0,
            sticky="w",
            padx=40,
            pady=8
        )

        value = tk.Label(
            card,
            text=str(item[1]),
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#243B6B"
        )

        value.grid(
            row=index,
            column=1,
            padx=40,
            pady=8
        )




def open_profile():

    profile_window = tk.Toplevel(login_window)

    profile_window.title(
        "User Profile"
    )

    profile_window.geometry(
        "500x450"
    )

    profile_window.configure(
        bg="#F4F7FB"
    )

    # HEADER

    header = tk.Frame(
        profile_window,
        bg="#243B6B"
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="USER PROFILE",
        font=("Arial", 20, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=20
    )

    # CARD

    card = tk.Frame(
        profile_window,
        bg="white"
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=30
    )

    connection = connect_database()

    full_name = ""
    username = ""

    if connection:

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT full_name, username
                FROM users
                WHERE id = %s
                """,
                (current_user_id,)
            )

            record = cursor.fetchone()

            if record:

                full_name = record[0]
                username = record[1]

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Label(
        card,
        text="Full Name",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(
        anchor="w",
        padx=30,
        pady=(40, 5)
    )

    tk.Label(
        card,
        text=full_name,
        font=("Arial", 12),
        bg="white",
        fg="#555555"
    ).pack(
        anchor="w",
        padx=30
    )

    tk.Label(
        card,
        text="Username",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        card,
        text=username,
        font=("Arial", 12),
        bg="white",
        fg="#555555"
    ).pack(
        anchor="w",
        padx=30
    )




def open_dashboard():

    dashboard = tk.Toplevel(login_window)

    dashboard.title(
        "Personal Productivity Activity Management System"
    )

    dashboard.geometry(
        "1100x700"
    )

    dashboard.configure(
        bg="#F4F7FB"
    )

    

    header = tk.Frame(
        dashboard,
        bg="#243B6B",
        height=100
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(
        False
    )

    tk.Label(
        header,
        text="PERSONAL PRODUCTIVITY",
        font=("Arial", 22, "bold"),
        bg="#243B6B",
        fg="white"
    ).pack(
        pady=(15, 2)
    )

    tk.Label(
        header,
        text="ACTIVITY MANAGEMENT SYSTEM",
        font=("Arial", 11, "bold"),
        bg="#243B6B",
        fg="#DCE6FF"
    ).pack()

    

    welcome = tk.Label(
        dashboard,
        text="Welcome, " + current_username,
        font=("Arial", 16, "bold"),
        bg="#F4F7FB",
        fg="#243B6B"
    )

    welcome.pack(
        anchor="w",
        padx=30,
        pady=20
    )

    


    stats_frame = tk.Frame(
        dashboard,
        bg="#F4F7FB"
    )

    stats_frame.pack(
        fill="x",
        padx=25
    )

    # VARIABLES

    total_tasks = tk.StringVar(
        value="0"
    )

    completed_tasks = tk.StringVar(
        value="0"
    )

    pending_tasks = tk.StringVar(
        value="0"
    )

    total_goals = tk.StringVar(
        value="0"
    )

    # CARD FUNCTION

    def create_stat_card(
        parent,
        title,
        variable,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=200,
            height=100
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        card.grid_propagate(
            False
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#666666"
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            card,
            textvariable=variable,
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#243B6B"
        ).pack()

    create_stat_card(
        stats_frame,
        "TOTAL TASKS",
        total_tasks,
        0
    )

    create_stat_card(
        stats_frame,
        "COMPLETED",
        completed_tasks,
        1
    )

    create_stat_card(
        stats_frame,
        "PENDING",
        pending_tasks,
        2
    )

    create_stat_card(
        stats_frame,
        "DAILY GOALS",
        total_goals,
        3
    )

    quick_title = tk.Label(
        dashboard,
        text="QUICK ACCESS",
        font=("Arial", 15, "bold"),
        bg="#F4F7FB",
        fg="#243B6B"
    )

    quick_title.pack(
        anchor="w",
        padx=30,
        pady=(30, 15)
    )

    button_frame = tk.Frame(
        dashboard,
        bg="#F4F7FB"
    )

    button_frame.pack(
        padx=25,
        fill="x"
    )

    # ROW 1

    tk.Button(
        button_frame,
        text="TASK MANAGEMENT",
        font=("Arial", 11, "bold"),
        bg="#243B6B",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_task_management
    ).grid(
        row=0,
        column=0,
        padx=8,
        pady=8
    )

    tk.Button(
        button_frame,
        text="DAILY GOALS",
        font=("Arial", 11, "bold"),
        bg="#3A6EA5",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_goal_management
    ).grid(
        row=0,
        column=1,
        padx=8,
        pady=8
    )

    tk.Button(
        button_frame,
        text="HABIT TRACKING",
        font=("Arial", 11, "bold"),
        bg="#4B6584",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_habit_management
    ).grid(
        row=0,
        column=2,
        padx=8,
        pady=8
    )

    # ROW 2

    tk.Button(
        button_frame,
        text="DAILY ACTIVITIES",
        font=("Arial", 11, "bold"),
        bg="#5C6BC0",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_activity_management
    ).grid(
        row=1,
        column=0,
        padx=8,
        pady=8
    )

    tk.Button(
        button_frame,
        text="STATISTICS",
        font=("Arial", 11, "bold"),
        bg="#607D8B",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_statistics
    ).grid(
        row=1,
        column=1,
        padx=8,
        pady=8
    )

    tk.Button(
        button_frame,
        text="MY PROFILE",
        font=("Arial", 11, "bold"),
        bg="#455A64",
        fg="white",
        relief="flat",
        width=22,
        height=3,
        command=open_profile
    ).grid(
        row=1,
        column=2,
        padx=8,
        pady=8
    )

    
    def load_dashboard_data():

        connection = connect_database()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                """,
                (current_user_id,)
            )

            total_tasks.set(
                str(cursor.fetchone()[0])
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                AND status = 'Completed'
                """,
                (current_user_id,)
            )

            completed_tasks.set(
                str(cursor.fetchone()[0])
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM tasks
                WHERE user_id = %s
                AND status = 'Pending'
                """,
                (current_user_id,)
            )

            pending_tasks.set(
                str(cursor.fetchone()[0])
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM goals
                WHERE user_id = %s
                AND goal_date = CURDATE()
                """,
                (current_user_id,)
            )

            total_goals.set(
                str(cursor.fetchone()[0])
            )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Dashboard Error",
                str(e)
            )

    load_dashboard_data()

    
    def logout():

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if confirm:

            dashboard.destroy()

    tk.Button(
        dashboard,
        text="LOGOUT",
        font=("Arial", 10, "bold"),
        bg="#C62828",
        fg="white",
        relief="flat",
        padx=30,
        pady=8,
        command=logout
    ).pack(
        pady=30
    )



login_window = tk.Tk()

login_window.title(
    "Personal Productivity Activity Management System"
)

login_window.geometry(
    "550x700"
)

login_window.configure(
    bg="#EAF0FF"
)

login_window.resizable(
    False,
    False
)



header = tk.Frame(
    login_window,
    bg="#243B6B",
    height=190
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)

tk.Label(
    header,
    text="PERSONAL PRODUCTIVITY",
    font=("Arial", 24, "bold"),
    bg="#243B6B",
    fg="white"
).pack(
    pady=(25, 5)
)

tk.Label(
    header,
    text="ACTIVITY MANAGEMENT SYSTEM",
    font=("Arial", 13, "bold"),
    bg="#243B6B",
    fg="#DCE6FF"
).pack()



card = tk.Frame(
    login_window,
    bg="white"
)

card.pack(
    padx=45,
    pady=35,
    fill="both",
    expand=True
)


tk.Label(
    card,
    text="LOGIN",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#243B6B"
).pack(
    pady=(35, 30)
)



tk.Label(
    card,
    text="Username",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#444444"
).pack(
    anchor="w",
    padx=45
)

username_entry = tk.Entry(
    card,
    font=("Arial", 12),
    bg="#F4F7FB",
    relief="flat"
)

username_entry.pack(
    padx=45,
    pady=(8, 20),
    fill="x",
    ipady=9
)



tk.Label(
    card,
    text="Password",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#444444"
).pack(
    anchor="w",
    padx=45
)

password_entry = tk.Entry(
    card,
    font=("Arial", 12),
    bg="#F4F7FB",
    relief="flat",
    show="*"
)

password_entry.pack(
    padx=45,
    pady=(8, 25),
    fill="x",
    ipady=9
)



button_frame = tk.Frame(
    card,
    bg="white"
)

button_frame.pack(
    pady=10
)


tk.Button(
    button_frame,
    text="LOGIN",
    font=("Arial", 11, "bold"),
    bg="#243B6B",
    fg="white",
    activebackground="#35569A",
    activeforeground="white",
    relief="flat",
    padx=30,
    pady=10,
    command=login
).pack(
    side="left",
    padx=5
)


tk.Button(
    button_frame,
    text="CLEAR",
    font=("Arial", 11, "bold"),
    bg="#E8ECF5",
    fg="#243B6B",
    relief="flat",
    padx=30,
    pady=10,
    command=clear_login
).pack(
    side="left",
    padx=5
)



tk.Button(
    card,
    text="CREATE NEW ACCOUNT",
    font=("Arial", 10, "bold"),
    bg="#3A6EA5",
    fg="white",
    relief="flat",
    padx=20,
    pady=8,
    command=open_registration
).pack(
    pady=20
)



tk.Label(
    card,
    text="Personal Productivity Management System",
    font=("Arial", 9),
    bg="white",
    fg="#888888"
).pack(
    side="bottom",
    pady=20
)



username_entry.focus()



login_window.mainloop()
