import tkinter as tk

def switch_to_main_ui(root, name):
    root.destroy() # Properly destroy the current Tkinter window
    # Import the Main UI code
    from MainUI import main_ui_code
    
    # Create a new window for the second page
    main_ui = tk.Tk()
    main_ui.title("Smart Mirror Main UI")

    # Execute the second page code
    main_ui_code(main_ui, name)


def calendarPage(root, name):
    root.title("Weekly Schedule")

    # Create a frame to hold the schedule
    frame = tk.Frame(root)
    frame.pack(pady=20, padx=20)

    # Create the title and day columns
    days = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for day in days:
        lbl = tk.Label(frame, text=day, font=('Helvetica 12 bold'), bd=1, relief="solid", padx=10, pady=5)
        lbl.grid(row=0, column=days.index(day), sticky="nsew")

    # Create the time rows and empty columns for schedule
    times = [f"{i:02d}:00AM" if i < 12 else (f"{i-12:02d}:00PM" if i > 12 else "12:00PM") for i in range(24)]

    for time in times:
        lbl_time = tk.Label(frame, text=time, font=('Helvetica 12'), bd=1, relief="solid", padx=10, pady=5)
        lbl_time.grid(row=times.index(time) + 1, column=0, sticky="nsew")
        for i in range(1, 8):
            lbl_empty = tk.Label(frame, font=('Helvetica 12'), bd=1, relief="solid", padx=10, pady=5)
            lbl_empty.grid(row=times.index(time) + 1, column=i, sticky="nsew")

    # Configuring column weights so they are all equal
    for col in range(8):
        frame.grid_columnconfigure(col, weight=1)

    # Configuring row weights so they are all equal
    for row in range(25):
        frame.grid_rowconfigure(row, weight=1)

    # Button to trigger the transition to the second page
    switch_button = tk.Button(frame, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, name)).grid(row=26, column=0,padx= (10, 0), pady=(5, 2))

    if(True):
        root.mainloop()