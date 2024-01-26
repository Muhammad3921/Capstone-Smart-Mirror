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


def mapsPage(root,name):
    root.title("Maps")
    root.geometry("500x500")

    # Create a label with the word "Maps"
    label = tk.Label(root, text="Maps", font=('Helvetica', 24))
    label.pack(pady=100)

    # Button to trigger the transition to the second page
    switch_button = tk.Button(root, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, name))
    switch_button.pack(pady=10)
   
    if(True):
        root.mainloop()