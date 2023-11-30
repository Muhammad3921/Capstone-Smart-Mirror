from tkinter import Tk, Frame, Label, Checkbutton, IntVar

root = Tk()
root.title("Reminders")
root.geometry("300x400")
root.config(bg="white")

# Main Frame for Reminders
main_frame = Frame(root, bg="white")
main_frame.pack(pady=20, padx=20)

# Title
Label(main_frame, text="Reminders", font=('Helvetica 24'), bg='white').pack(pady=10)

# Incomplete Section
Label(main_frame, text="Incomplete", font=('Helvetica 18'), bg='white').pack(anchor="w", pady=(20, 10), padx=10)

incomplete_tasks = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit." for _ in range(6)]

# Create checkbuttons for incomplete tasks
for task in incomplete_tasks:
    Checkbutton(main_frame, text=task, bg='white', font=('Helvetica 12')).pack(anchor="w", padx=20)

# Complete Section
Label(main_frame, text="Complete", font=('Helvetica 18'), bg='white').pack(anchor="w", pady=(20, 10), padx=10)

complete_tasks = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit." for _ in range(4)]

# Create labels for completed tasks
for task in complete_tasks:
    Label(main_frame, text=task, bg='white', font=('Helvetica 12')).pack(anchor="w", padx=20, pady=5)

root.mainloop()