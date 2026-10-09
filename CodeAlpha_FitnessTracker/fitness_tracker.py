# =====================================================================
# TASK 3: FITNESS TRACKER APP  (beginner-friendly version)
# =====================================================================
# What this app does:
#   - You log activities: exercise type, workout minutes, calories, steps.
#   - A Dashboard shows today's progress (progress bars)
#     and the last 7 days (bar chart).
#   - Data is saved in a SQLite database file (fitness.db).
#
# How to run:   python fitness_tracker.py
#
# SQL words used in this file (SQL = the language databases understand):
#   CREATE TABLE  - make a new table (like a spreadsheet)
#   INSERT INTO   - add a new row
#   SELECT        - read rows
#   DELETE        - remove rows
#   WHERE         - only the rows that match a condition
#   SUM           - add numbers together
#   ORDER BY      - sort the rows
# =====================================================================


# ---------------------------------------------------------------------
# 1. IMPORTS
# ---------------------------------------------------------------------
import sqlite3                                   # database that lives in one file
import tkinter as tk                             # windows and buttons
from tkinter import ttk                          # extra widgets: tabs, progress bars, drop-down lists
from tkinter import messagebox                   # pop-up messages
from datetime import date, datetime, timedelta   # work with dates


# ---------------------------------------------------------------------
# 2. SETTINGS
# ---------------------------------------------------------------------
DB_NAME = "fitness.db"

# Daily goals. The progress bars show "today's total compared to the goal".
STEPS_GOAL = 10000
CALORIES_GOAL = 500
MINUTES_GOAL = 45

EXERCISES = ["Walking", "Running", "Cycling", "Swimming", "Gym", "Yoga", "HIIT", "Sports", "Other"]

# The database id of each row shown in the "recent entries" list.
# We need it so we know WHICH row to delete when the user clicks Delete.
row_ids = []


# ---------------------------------------------------------------------
# 3. DATABASE FUNCTIONS
# ---------------------------------------------------------------------
# Every database function follows the same 4 steps:
#   1) connect   2) execute SQL   3) commit (save)   4) close

def create_table():
    """Make the 'activities' table if it does not exist yet."""
    connection = sqlite3.connect(DB_NAME)        # open (or create) the database file
    cursor = connection.cursor()                 # a cursor is the "pen" that runs SQL commands
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date TEXT,
            exercise TEXT,
            minutes  INTEGER,
            calories INTEGER,
            steps    INTEGER
        )
    """)
    connection.commit()                          # commit = save the changes for real
    connection.close()


def add_activity(log_date, exercise, minutes, calories, steps):
    """Add one new row to the table."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # The ? marks are placeholders. SQLite puts our values there safely.
    # (Never join SQL and values together with + , it can be unsafe.)
    cursor.execute("INSERT INTO activities (log_date, exercise, minutes, calories, steps) VALUES (?, ?, ?, ?, ?)",
                   (log_date, exercise, minutes, calories, steps))
    connection.commit()
    connection.close()


def delete_activity(row_id):
    """Delete the row that has this id."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM activities WHERE id = ?", (row_id,))   # (row_id,) = a tuple with ONE item
    connection.commit()
    connection.close()


def get_recent_rows():
    """Return the 40 newest rows."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id, log_date, exercise, minutes, calories, steps "
                   "FROM activities ORDER BY log_date DESC, id DESC LIMIT 40")
    rows = cursor.fetchall()                     # fetchall() = get ALL the rows as a list
    connection.close()
    return rows


def get_day_totals(day):
    """Add up minutes, calories and steps for one day (a text like '2026-10-05').
    Returns three numbers."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(minutes), SUM(calories), SUM(steps) FROM activities WHERE log_date = ?", (day,))
    row = cursor.fetchone()                      # fetchone() = just one row, e.g. (30, 250, 5000)
    connection.close()

    minutes = row[0]
    calories = row[1]
    steps = row[2]

    # If nothing was logged that day, SUM gives None (nothing). We want 0 instead.
    if minutes is None:
        minutes = 0
    if calories is None:
        calories = 0
    if steps is None:
        steps = 0

    return minutes, calories, steps              # a function can return several values at once


# ---------------------------------------------------------------------
# 4. DASHBOARD FUNCTIONS
# ---------------------------------------------------------------------

def update_one_bar(bar, label, name, value, goal):
    """Fill ONE progress bar. We reuse this for steps, calories and minutes."""
    percent = value / goal * 100                 # for example 5000 / 10000 * 100 = 50
    if percent > 100:
        percent = 100                            # the bar can't be more than full
    bar["value"] = percent                       # set the bar's fill
    label.config(text=name + ": " + str(value) + " / " + str(goal) + "   (" + str(int(percent)) + "%)")


def update_today_bars():
    """Read today's totals from the database and update the 3 progress bars."""
    today = date.today().isoformat()             # today's date as text, like '2026-10-05'
    minutes, calories, steps = get_day_totals(today)       # receive the three returned values

    update_one_bar(steps_bar, steps_label, "Steps", steps, STEPS_GOAL)
    update_one_bar(calories_bar, calories_label, "Calories burned", calories, CALORIES_GOAL)
    update_one_bar(minutes_bar, minutes_label, "Workout minutes", minutes, MINUTES_GOAL)


def draw_chart(event=None):
    """Draw a bar chart of the last 7 days.
    (event=None lets us call this function by hand AND from the drop-down list.)"""

    # --- Step 1: decide which number to chart and what the goal is ---
    choice = chart_choice.get()                  # text currently selected in the drop-down
    if choice == "Steps":
        goal = STEPS_GOAL
        bar_color = "#38bdf8"
    elif choice == "Calories burned":
        goal = CALORIES_GOAL
        bar_color = "#fb923c"
    else:
        goal = MINUTES_GOAL
        bar_color = "#4ade80"

    # --- Step 2: collect 7 days of data ---
    day_names = []                               # like "Mon", "Tue", ...
    values = []                                  # the number for each day
    for i in range(7):                           # i is 0, 1, 2, 3, 4, 5, 6
        days_ago = 6 - i                         # 6, 5, 4, 3, 2, 1, 0  (oldest day first)
        day = date.today() - timedelta(days=days_ago)
        minutes, calories, steps = get_day_totals(day.isoformat())

        if choice == "Steps":
            value = steps
        elif choice == "Calories burned":
            value = calories
        else:
            value = minutes

        day_names.append(day.strftime("%a"))     # %a = short weekday name
        values.append(value)

    # --- Step 3: find the biggest number so the tallest bar fits in the chart ---
    biggest = goal
    for value in values:
        if value > biggest:
            biggest = value

    # --- Step 4: draw ---
    # On a canvas, (0,0) is the TOP-LEFT corner. x goes right, y goes DOWN.
    canvas.delete("all")                         # erase the old drawing

    left = 60                                    # the chart area is the rectangle
    right = 680                                  # from (left, top) to (right, bottom)
    top = 30
    bottom = 220
    height = bottom - top                        # chart height in pixels
    slot_width = (right - left) / 7              # horizontal space for each day

    canvas.create_line(left, bottom, right, bottom)       # the bottom line (x axis)
    canvas.create_text(left, 12, text=choice, anchor="w", font=("Arial", 11, "bold"))

    # The red dashed goal line
    goal_y = bottom - (goal / biggest * height)
    canvas.create_line(left, goal_y, right, goal_y, fill="red", dash=(4, 3))
    canvas.create_text(left - 5, goal_y, text="Goal " + str(goal), anchor="e", fill="red", font=("Arial", 8))

    # One bar for each day
    total = 0
    days_reached = 0
    for i in range(7):
        value = values[i]
        total = total + value
        if value >= goal:
            days_reached = days_reached + 1

        bar_left = left + i * slot_width + 12            # where this bar starts (x)
        bar_right = left + (i + 1) * slot_width - 12     # where this bar ends (x)
        bar_top = bottom - (value / biggest * height)    # taller bar = smaller y
        canvas.create_rectangle(bar_left, bar_top, bar_right, bottom, fill=bar_color, outline="")
        middle = (bar_left + bar_right) / 2
        canvas.create_text(middle, bar_top - 8, text=str(value), font=("Arial", 9))
        canvas.create_text(middle, bottom + 14, text=day_names[i], font=("Arial", 10, "bold"))

    average = int(total / 7)
    summary_label.config(text="Weekly total: " + str(total) + "     Daily average: " + str(average) +
                              "     Goal reached: " + str(days_reached) + " of 7 days")


# ---------------------------------------------------------------------
# 5. LOG TAB FUNCTIONS
# ---------------------------------------------------------------------

def save_entry():
    """Check what the user typed. If it is OK, save it in the database."""

    # --- Check the date ---
    date_text = date_entry.get().strip()         # .get() reads the text from an Entry box
    try:
        datetime.strptime(date_text, "%Y-%m-%d")             # works only if the format is right
    except ValueError:                                       # ValueError = the format was wrong
        messagebox.showerror("Wrong date", "Write the date like this: 2026-10-05")
        return

    # --- Check the numbers ---
    try:
        minutes = int(minutes_entry.get())       # int() turns text into a whole number
        calories = int(calories_entry.get())
        steps = int(steps_entry.get())
    except ValueError:                           # happens if the user typed letters, like "abc"
        messagebox.showerror("Wrong number", "Minutes, calories and steps must be whole numbers.")
        return

    if minutes < 0 or calories < 0 or steps < 0:
        messagebox.showerror("Wrong number", "Numbers cannot be negative.")
        return

    if minutes == 0 and calories == 0 and steps == 0:
        messagebox.showwarning("Nothing to save", "Please enter at least one number bigger than 0.")
        return

    # --- Everything is fine: save it ---
    exercise = exercise_box.get()
    add_activity(date_text, exercise, minutes, calories, steps)

    # Put "0" back into the number boxes
    minutes_entry.delete(0, tk.END)              # delete(0, END) = clear the whole box
    minutes_entry.insert(0, "0")                 # insert(0, text) = write text at the start
    calories_entry.delete(0, tk.END)
    calories_entry.insert(0, "0")
    steps_entry.delete(0, tk.END)
    steps_entry.insert(0, "0")

    refresh_everything()
    messagebox.showinfo("Saved", "Activity saved!")


def refresh_list():
    """Fill the 'recent entries' list from the database."""
    global row_ids
    entries_list.delete(0, tk.END)               # clear the list
    row_ids = []                                 # and forget the old ids

    rows = get_recent_rows()
    for row in rows:                             # row looks like (id, date, exercise, minutes, calories, steps)
        text = (row[1] + "  |  " + row[2] + "  |  " + str(row[3]) + " min  |  " +
                str(row[4]) + " cal  |  " + str(row[5]) + " steps")
        entries_list.insert(tk.END, text)        # add a line at the END of the list
        row_ids.append(row[0])                   # keep the id in the same position


def delete_selected():
    """Delete the entry the user clicked in the list."""
    selected = entries_list.curselection()       # a tuple with the selected line numbers
    if len(selected) == 0:
        messagebox.showinfo("Delete", "Click an entry in the list first.")
        return

    sure = messagebox.askyesno("Delete", "Delete this entry?")
    if sure == False:
        return

    position = selected[0]                       # first selected line number
    delete_activity(row_ids[position])           # row_ids[position] = the database id of that line
    refresh_everything()


def refresh_everything():
    """Update the bars, the chart and the list."""
    update_today_bars()
    draw_chart()
    refresh_list()


def tab_changed(event):
    """Runs when the user switches tabs, so the dashboard is always up to date."""
    refresh_everything()


# ---------------------------------------------------------------------
# 6. BUILDING THE WINDOW
# ---------------------------------------------------------------------
create_table()                                   # make sure the database table exists

root = tk.Tk()
root.title("Fitness Tracker")
root.geometry("760x700")

# A Notebook is a set of tabs
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

dashboard_tab = tk.Frame(tabs)
log_tab = tk.Frame(tabs)
tabs.add(dashboard_tab, text="  Dashboard  ")
tabs.add(log_tab, text="  Log Activity  ")

# ---------- Dashboard tab ----------
tk.Label(dashboard_tab, text="Today's Progress", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=10)

# Three progress bars. Each has a label above it. (We write them out one by one to keep it simple.)
steps_label = tk.Label(dashboard_tab, text="", anchor="w")
steps_label.pack(fill="x", padx=15)
steps_bar = ttk.Progressbar(dashboard_tab, maximum=100)       # maximum=100 -> the value is a percentage
steps_bar.pack(fill="x", padx=15, pady=(0, 8))

calories_label = tk.Label(dashboard_tab, text="", anchor="w")
calories_label.pack(fill="x", padx=15)
calories_bar = ttk.Progressbar(dashboard_tab, maximum=100)
calories_bar.pack(fill="x", padx=15, pady=(0, 8))

minutes_label = tk.Label(dashboard_tab, text="", anchor="w")
minutes_label.pack(fill="x", padx=15)
minutes_bar = ttk.Progressbar(dashboard_tab, maximum=100)
minutes_bar.pack(fill="x", padx=15, pady=(0, 8))

# Title row for the chart with a drop-down list on the right
chart_title_row = tk.Frame(dashboard_tab)
chart_title_row.pack(fill="x", padx=15, pady=(15, 5))
tk.Label(chart_title_row, text="Last 7 Days", font=("Arial", 16, "bold")).pack(side="left")

chart_choice = ttk.Combobox(chart_title_row, values=["Steps", "Calories burned", "Workout minutes"],
                            state="readonly", width=18)       # readonly = choose from the list only
chart_choice.set("Steps")                                     # the starting choice
chart_choice.pack(side="right")
chart_choice.bind("<<ComboboxSelected>>", draw_chart)         # redraw the chart when the choice changes

# A Canvas is an empty area where we can draw shapes
canvas = tk.Canvas(dashboard_tab, width=700, height=260, bg="white")
canvas.pack(padx=15, pady=5)

summary_label = tk.Label(dashboard_tab, text="")
summary_label.pack(anchor="w", padx=15, pady=8)

# ---------- Log tab ----------
form = tk.LabelFrame(log_tab, text=" New entry ", padx=10, pady=10)
form.pack(fill="x", padx=15, pady=15)

# grid() places widgets in rows and columns, like a table
tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w", pady=4)
date_entry = tk.Entry(form, width=24)
date_entry.insert(0, date.today().isoformat())      # start with today's date
date_entry.grid(row=0, column=1, padx=10, pady=4)

tk.Label(form, text="Exercise type").grid(row=1, column=0, sticky="w", pady=4)
exercise_box = ttk.Combobox(form, values=EXERCISES, state="readonly", width=21)
exercise_box.set("Walking")
exercise_box.grid(row=1, column=1, padx=10, pady=4)

tk.Label(form, text="Workout time (minutes)").grid(row=2, column=0, sticky="w", pady=4)
minutes_entry = tk.Entry(form, width=24)
minutes_entry.insert(0, "0")
minutes_entry.grid(row=2, column=1, padx=10, pady=4)

tk.Label(form, text="Calories burned").grid(row=3, column=0, sticky="w", pady=4)
calories_entry = tk.Entry(form, width=24)
calories_entry.insert(0, "0")
calories_entry.grid(row=3, column=1, padx=10, pady=4)

tk.Label(form, text="Steps").grid(row=4, column=0, sticky="w", pady=4)
steps_entry = tk.Entry(form, width=24)
steps_entry.insert(0, "0")
steps_entry.grid(row=4, column=1, padx=10, pady=4)

tk.Button(form, text="Save Entry", width=16, command=save_entry).grid(row=5, column=0, columnspan=2, pady=10)

tk.Label(log_tab, text="Recent entries", font=("Arial", 12, "bold")).pack(anchor="w", padx=15)

# A Listbox shows a list of text lines. Courier is a font where all letters have equal width.
entries_list = tk.Listbox(log_tab, height=10, font=("Courier", 10))
entries_list.pack(fill="x", padx=15, pady=5)

tk.Button(log_tab, text="Delete Selected", command=delete_selected).pack(pady=5)

# Refresh when the user switches tabs
tabs.bind("<<NotebookTabChanged>>", tab_changed)

# Fill the dashboard for the first time
refresh_everything()


# ---------------------------------------------------------------------
# 7. STARTING THE APP
# ---------------------------------------------------------------------
if __name__ == "__main__":
    root.mainloop()
