import tkinter as tk

root = tk.Tk()
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

root.mainloop()