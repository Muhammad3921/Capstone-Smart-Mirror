from tkinter import *
from tkinter import messagebox
import json
import os

def load_reminders(username):
    reminders_filename = f"reminders/{username}/{username}_reminders.json"
    if not os.path.exists(reminders_filename):
        return [], []  # Returns empty lists if the file does not exist
    with open(reminders_filename, 'r') as file:
        data = json.load(file)
    return data.get('incomplete', []), data.get('complete', [])

def save_reminders(username, incomplete_reminders, complete_reminders):
    directory_path = f"reminders/{username}"  # Define the directory path
    reminders_filename = f"{directory_path}/{username}_reminders.json"
    data = {'incomplete': incomplete_reminders, 'complete': complete_reminders}
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    with open(reminders_filename, 'w') as file:
        json.dump(data, file, indent=4)

def switch_to_main_ui(root, masterFrame, name):
    masterFrame.destroy()
    from MainUI import main_ui_code
    root.title("Smart Mirror Main UI")
    main_ui_code(root, name)

def add_task(username, incomplete_tasks, complete_tasks, task_entry, update_tasks_display):
    task = task_entry.get()
    if task:
        incomplete_tasks.append(task)
        task_entry.delete(0, END)
        update_tasks_display(incomplete_tasks, complete_tasks)
        save_reminders(username, incomplete_tasks, complete_tasks)  # Save reminders after adding a task
    else:
        messagebox.showwarning("Warning", "The task cannot be empty.")

def complete_task(username, incomplete_tasks, complete_tasks, task, update_tasks_display):
    if task in incomplete_tasks:
        incomplete_tasks.remove(task)
        complete_tasks.append(task)
        update_tasks_display(incomplete_tasks, complete_tasks)
        save_reminders(username, incomplete_tasks, complete_tasks)  # Save reminders after completing a task

def reminderPage(root, name):
    global incomplete_tasks, complete_tasks, task_entry
    incomplete_tasks, complete_tasks = load_reminders(name)  # Pass the username to load user-specific reminders

    root.title("Reminders")
    root.geometry("500x700")

    main_frame = Frame(root, bg="white")
    main_frame.pack(pady=20, padx=20)

    from MainUI import sharedqueue
    cock = (root, main_frame, name)
    sharedqueue.put(cock)

    Label(main_frame, text="Reminders", font=('Helvetica 24'), bg='white').pack(pady=10)

    task_entry = Entry(main_frame)
    task_entry.pack(pady=10)

    add_task_button = Button(main_frame, text="Add Task",
                             command=lambda: add_task(name, incomplete_tasks, complete_tasks, task_entry,
                                                      update_tasks_display))
    add_task_button.pack(pady=10)

    incomplete_frame = Frame(main_frame, bg='white')
    complete_frame = Frame(main_frame, bg='white')

    Label(main_frame, text="Incomplete", font=('Helvetica 18'), bg='white').pack(anchor="w", pady=(20, 10), padx=10)
    incomplete_frame.pack()

    Label(main_frame, text="Complete", font=('Helvetica 18'), bg='white').pack(anchor="w", pady=(20, 10), padx=10)
    complete_frame.pack()

    def update_tasks_display(incomplete_tasks, complete_tasks):
        for widget in incomplete_frame.winfo_children():
            widget.destroy()
        for widget in complete_frame.winfo_children():
            widget.destroy()

        for task in incomplete_tasks:
            cb = Checkbutton(incomplete_frame, text=task, font=('Helvetica 12'),
                             command=lambda t=task: complete_task(name, incomplete_tasks, complete_tasks, t,
                                                                  update_tasks_display))
            cb.pack(anchor="w", padx=20, pady=2)

        for task in complete_tasks:
            label = Label(complete_frame, text=task, font=('Helvetica 12'))
            label.pack(anchor="w", padx=20, pady=2)

    update_tasks_display(incomplete_tasks, complete_tasks)

    switch_button = Button(main_frame, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, main_frame, name))
    switch_button.pack(pady=10)

    

if __name__ == "__main__":
    root = Tk()
    reminderPage(root, "User")