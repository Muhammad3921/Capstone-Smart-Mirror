from tkinter import *

def switch_to_main_ui(root, name):
    root.destroy() # Properly destroy the current Tkinter window
    # Import the Main UI code
    from MainUI import main_ui_code
    
    # Create a new window for the second page
    main_ui = Tk()
    main_ui.title("Smart Mirror Main UI")

    # Execute the second page code
    main_ui_code(main_ui, name)

def reminderPage(root,name):
    root.title("Reminders")
    root.geometry("500x700")
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

    # Button to trigger the transition to the second page
    switch_button = Button(main_frame, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, name))
    switch_button.pack(pady=10)

    if(True):
        root.mainloop()