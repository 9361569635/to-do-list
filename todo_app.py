import tkinter as tk
from tkinter import messagebox
import sqlite3

# ----------------- Database Setup -----------------
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
''')
conn.commit()

# ----------------- Functions -----------------
def refresh_tasks():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT id, task, completed FROM tasks")
    for row in cursor.fetchall():
        status = "✅" if row[2] else "⭕"
        listbox.insert(tk.END, f"{row[0]}. {status} {row[1]}")

def add_task():
    task = entry.get()
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        entry.delete(0, tk.END)
        refresh_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_id = int(listbox.get(selected).split('.')[0])
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        refresh_tasks()

def mark_completed():
    selected = listbox.curselection()
    if selected:
        task_id = int(listbox.get(selected).split('.')[0])
        cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
        conn.commit()
        refresh_tasks()

def clear_all():
    if messagebox.askyesno("Clear All", "Are you sure you want to delete all tasks?"):
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        refresh_tasks()

# ----------------- GUI Setup -----------------
root = tk.Tk()
root.title("ARTTIFAI TECH - To-Do LIST")
root.geometry("600x600")
root.config(bg="#20232a")

# ----------------- Styles -----------------
BG_COLOR = "#282c34"
BOX_COLOR = "#3c4049"
BTN_COLOR = "#61dafb"
TEXT_COLOR = "#ffffff"
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_BODY = ("Segoe UI", 12)

# Title
title = tk.Label(root, text="🌟 To-Do LIST", font=FONT_TITLE, fg=TEXT_COLOR, bg=BG_COLOR)
title.pack(pady=20)

# Entry Section
entry_frame = tk.Frame(root, bg=BG_COLOR)
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=35, font=("Segoe UI", 13), bg=BOX_COLOR, fg=TEXT_COLOR, insertbackground="white", relief=tk.FLAT)
entry.pack(side=tk.LEFT, padx=10, ipady=6)

add_btn = tk.Button(entry_frame, text="➕ Add", font=FONT_BODY, bg=BTN_COLOR, fg="black", width=10, command=add_task, relief=tk.FLAT, activebackground="#21a1f1")
add_btn.pack(side=tk.LEFT, padx=5)

# Listbox Section
list_frame = tk.Frame(root, bg=BG_COLOR)
list_frame.pack(pady=10)

listbox = tk.Listbox(list_frame, width=60, height=15, font=("Consolas", 11), bg=BOX_COLOR, fg=TEXT_COLOR, selectbackground="#61dafb", selectforeground="black", bd=0, relief=tk.FLAT)
listbox.pack(padx=10)

# Buttons Section
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=20)

complete_btn = tk.Button(btn_frame, text="✅ Mark Done", bg=BTN_COLOR, fg="black", font=FONT_BODY, width=20, command=mark_completed, relief=tk.FLAT)
complete_btn.grid(row=0, column=0, padx=10, pady=5)

delete_btn = tk.Button(btn_frame, text="🗑️ Delete Task", bg="#f05454", fg="white", font=FONT_BODY, width=20, command=delete_task, relief=tk.FLAT)
delete_btn.grid(row=0, column=1, padx=10, pady=5)

clear_btn = tk.Button(btn_frame, text="❌ Clear All", bg="#6a0572", fg="white", font=FONT_BODY, width=43, command=clear_all, relief=tk.FLAT)
clear_btn.grid(row=1, column=0, columnspan=2, pady=10)

# Initialize task list
refresh_tasks()
root.mainloop()
