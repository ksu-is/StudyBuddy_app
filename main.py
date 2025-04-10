import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading

DATA_FILE = "tasks.json"

class StudyBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StudyBuddy - Enhanced")
        self.root.geometry("640x600")
        self.root.configure(bg="#e6f2ff")

        self.tasks = []
        self.check_vars = []

        self.load_tasks()

        # UI Elements
        title = ttk.Label(root, text="🎓 StudyBuddy", font=("Segoe UI", 16, "bold"), background="#e6f2ff", foreground="#003366")
        title.pack(pady=10)

        self.task_frame = tk.Frame(root, bg="#e6f2ff")
        self.task_frame.pack(pady=10)

        button_frame = tk.Frame(root, bg="#e6f2ff")
        button_frame.pack()

        ttk.Button(button_frame, text="➕ Add Task", command=self.add_task).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="📈 Show Progress", command=self.show_progress).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(button_frame, text="❌ Delete Completed Tasks", command=self.delete_completed_tasks).grid(row=0, column=2, padx=10, pady=5)
        ttk.Button(button_frame, text="💾 Save", command=self.save_tasks).grid(row=0, column=3, padx=10, pady=5)
        ttk.Button(button_frame, text="⏳ Start Focus Timer", command=self.start_focus_timer).grid(row=0, column=4, padx=10, pady=5)

        self.status_label = ttk.Label(root, text="", background="#e6f2ff", foreground="#003366")
        self.status_label.pack(pady=5)

        self.update_task_list()

    def add_task(self):
        task_text = simpledialog.askstring("New Task", "Enter your task:")
        if task_text:
            self.tasks.append({"task": task_text, "done": False, "date": ""})
            self.save_tasks()
            self.update_task_list()

    def toggle_task(self, index):
        task = self.tasks[index]
        task["done"] = self.check_vars[index].get()
        if task["done"]:
            task["date"] = str(datetime.now().date())
        else:
            task["date"] = ""
        self.save_tasks()

    def delete_completed_tasks(self):
        completed_tasks = [task for task in self.tasks if task["done"]]
        if not completed_tasks:
            messagebox.showinfo("Delete Tasks", "No completed tasks to delete!")
            return
        self.tasks = [task for task in self.tasks if not task["done"]]
        self.save_tasks()
        self.update_task_list()
        messagebox.showinfo("Delete Tasks", "Completed tasks deleted successfully!")

    def update_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        self.check_vars = []
        for i, task in enumerate(self.tasks):
            var = tk.BooleanVar(value=task["done"])
            cb = tk.Checkbutton(self.task_frame, text=task["task"], variable=var,
                                command=lambda i=i: self.toggle_task(i),
                                font=("Segoe UI", 11), bg="#e6f2ff", fg="#003366",
                                activebackground="#e6f2ff", selectcolor="#b3d9ff")
            cb.pack(anchor="w", padx=20, pady=2)
            self.check_vars.append(var)

    def show_progress(self):
        dates = {}
        for task in self.tasks:
            if task["done"] and task["date"]:
                dates[task["date"]] = dates.get(task["date"], 0) + 1

        if not dates:
            messagebox.showinfo("Progress", "No completed tasks yet!")
            return

        fig, ax = plt.subplots()
        ax.bar(dates.keys(), dates.values(), color="#3399ff")
        ax.set_title("Tasks Completed Per Day")
        ax.set_ylabel("Tasks Done")
        ax.set_xlabel("Date")
        fig.autofmt_xdate()

        top = tk.Toplevel(self.root)
        top.title("Progress Chart")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    content = f.read().strip()
                    self.tasks = json.loads(content) if content else []
            except json.JSONDecodeError:
                self.tasks = []

    def save_tasks(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)
        self.status_label.config(text="Tasks saved successfully.")

    def start_focus_timer(self):
        # Create a top-level timer window
        top = tk.Toplevel(self.root)
        top.title("⏰ Focus Timer")
        top.geometry("300x150")
        top.configure(bg="#e6f2ff")

        label = ttk.Label(top, text="25:00", font=("Segoe UI", 32, "bold"), foreground="#003366", background="#e6f2ff")
        label.pack(pady=20)

        def countdown(t):
            while t >= 0:
                mins, secs = divmod(t, 60)
                time_str = f"{mins:02}:{secs:02}"
                label.config(text=time_str)
                top.update()
                time.sleep(1)
                t -= 1
            messagebox.showinfo("Time's up!", "Great job! Take a 5-minute break.")
            top.destroy()

        threading.Thread(target=lambda: countdown(25 * 60), daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyBuddyApp(root)
    root.mainloop()
