import tkinter as tk
from tkinter import Frame, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from html.parser import HTMLParser
class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = ""

    def handle_data(self, data):
        self.output += data

def switch_to_main_ui(root, masterFrame, name):
    #destroy current frame
    masterFrame.destroy()
    # Import the Main UI code
    from MainUI import main_ui_code
    
    # Create a new window for the second page
    root.title("Smart Mirror Main UI")

    # Execute the second page code
    main_ui_code(root, name)


def mapsPage(root, name):
    def build_static_map_url(location1, location2, api_key):
        base_url = "https://maps.googleapis.com/maps/api/staticmap?"
        encoded_location1 = "+".join(location1.split())
        encoded_location2 = "+".join(location2.split())
        parameters = {
            "center": f"{encoded_location1}|{encoded_location2}",
            "size": "500x500",
            "zoom": 10,
            "markers": f"{encoded_location1}|{encoded_location2}",
            "path": f"color:red|{encoded_location1}|{encoded_location2}",
            "key": api_key
        }
        url = base_url + "&".join([f"{key}={value}" for key, value in parameters.items()])
        return url

    def display_static_map(location1, location2, api_key):
        static_map_url = build_static_map_url(location1, location2, api_key)
        response = requests.get(static_map_url)
        image = Image.open(BytesIO(response.content))
        map_image = ImageTk.PhotoImage(image)
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=map_image)
        canvas.image = map_image

    def get_directions(origin, destination, api_key, mode, **kwargs):
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "key": api_key,
            "mode": mode,
            **kwargs
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None

    def format_directions(raw_directions):
        parser = HTMLStripper()
        formatted_directions = []
        for step in raw_directions:
            parser.feed(step["html_instructions"])
            formatted_directions.append(parser.output)
            parser.output = ""
        return formatted_directions

    def show_directions():
        origin = origin_entry.get()
        destination = destination_entry.get()
        transit_mode = transit_mode_var.get()
        api_key = "INSERTAPIKEY"
        
        # Display static map
        display_static_map(origin, destination, api_key)
        
        # Get and display directions
        directions = get_directions(origin, destination, api_key, mode=transit_mode)
        if directions:
            steps = directions["routes"][0]["legs"][0]["steps"]
            formatted_steps = format_directions(steps)
            directions_text.delete("1.0", tk.END)
            for step in formatted_steps:
                directions_text.insert(tk.END, step + "\n")
        else:
            directions_text.insert(tk.END, "Failed to fetch directions.")
    root.title("Maps")
    root.geometry("800x800")

    masterFrame = Frame(root, height =800, width=800, bg="black")
    masterFrame.pack()

    from MainUI import sharedqueue
    cock = (root, masterFrame, name)
    sharedqueue.put(cock)
    # Create a label with the word "Maps"
    label = tk.Label(masterFrame, text="Maps", font=('Helvetica', 14))
    label.pack(pady=2)

    # Button to trigger the transition to the second page
    switch_button = tk.Button(masterFrame, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, masterFrame, name))
    switch_button.pack(pady=10)
    
    # Frame for map and directions
    frame = ttk.Frame(masterFrame)
    frame.pack(fill=tk.BOTH, expand=True)

    # Canvas to display the map
    canvas = tk.Canvas(frame, width=500, height=500)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Text widget to display directions
    directions_text = tk.Text(frame, wrap=tk.WORD)
    directions_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Entry widgets for origin and destination
    origin_label = ttk.Label(masterFrame, text="Origin:")
    origin_label.pack(pady=5)
    origin_entry = ttk.Entry(masterFrame, width=50)
    origin_entry.pack(pady=5)

    destination_label = ttk.Label(masterFrame, text="Destination:")
    destination_label.pack(pady=5)
    destination_entry = ttk.Entry(masterFrame, width=50)
    destination_entry.pack(pady=5)

    # Dropdown menu for transit mode
    transit_mode_var = tk.StringVar()
    transit_mode_label = ttk.Label(masterFrame, text="Transit Mode:")
    transit_mode_label.pack(pady=5)
    transit_mode_menu = ttk.OptionMenu(masterFrame, transit_mode_var, "transit", "driving", "transit", "walking", "bicycling")
    transit_mode_menu.pack(pady=5)

    # Button to show directions
    show_directions_button = ttk.Button(masterFrame, text="Show Directions", command=show_directions)
    show_directions_button.pack(pady=5)
   
    #if(True):
        #root.mainloop()