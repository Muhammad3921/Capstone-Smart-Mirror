import tkinter as tk
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from nylas import APIClient
import pytz


load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")
#Calendar func
nylas = APIClient(
   os.getenv("NYLAS1"),
   os.getenv("NYLAS2"),
   os.getenv("NYLAS3")
)

def compare_24_hour_times(time_str1, time_str2):
    # Convert time strings to datetime objects for comparison
    time_format = "%H:%M"

    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)

    # Perform the comparison and return the result
    if time1 < time2:
        return 0
    elif time1 > time2:
        return 1
    else:
        return 2
    
def convert_to_24_hour_time(time_str):
    # Convert time string to datetime object
    time_format_12_hour = "%I:%M%p"
    datetime_object = datetime.strptime(time_str, time_format_12_hour)

    # Format the datetime object in 24-hour format
    time_format_24_hour = "%H:%M"
    time_24_hour = datetime_object.strftime(time_format_24_hour)

    return time_24_hour

def read_weekly_calendar_events(start_date):
    end_date = start_date + timedelta(days=6)  # Calculate the end date of the week

    events_list = []
    events = nylas.events.where(calendar_id=CALENDAR_ID).all(limit=100)  # Fetch all events

    for event in events:
        utc_datetime = datetime.utcfromtimestamp(event.when['start_time'])

        # Set the UTC time zone
        utc_timezone = pytz.timezone('UTC')
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to Eastern Time (EST)
        est_timezone = pytz.timezone('US/Eastern')
        est_datetime = utc_datetime.astimezone(est_timezone)
        event_start_date = est_datetime.date()

        # Check if the event occurs within the specified week
        if start_date <= event_start_date <= end_date:
            event_dict = {
                "Title": event.title,
                "When": event.when,
                "Participants": event.participants
            }
            events_list.append(event_dict)

    return events_list

def convert_to_12_hour_time(input_datetime):
    # Use strftime to format the time in 12-hour format
    return input_datetime.strftime("%I:%M%p")


def get_previous_monday(date):
    # Calculate the difference in days between the target date and the nearest Monday
    days_to_monday = (date.weekday() - 0) % 7
    
    # Subtract the difference to get the previous Monday
    start_of_week = date - timedelta(days=days_to_monday)
    
    return start_of_week

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

    start_date_of_week = get_previous_monday(datetime.now().date())

    weekly_events = read_weekly_calendar_events(start_date_of_week)

    print(weekly_events)
    # Create a frame to hold the schedule
    masterFrame = tk.Frame(root)
    masterFrame.pack(pady=20, padx=20)

    # Create the title and day columns
    days = ['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for day in days:
        lbl = tk.Label(masterFrame, text=day, font=('Helvetica 12 bold'), bd=1, relief="solid", padx=10, pady=5)
        lbl.grid(row=0, column=days.index(day), sticky="nsew")

    # Create the time rows and empty columns for schedule
    times = [f"{i:02d}:00AM" if i < 12 else (f"{i-12:02d}:00PM" if i > 12 else "12:00PM") for i in range(24)]

    for time in times:
        lbl_time = tk.Label(masterFrame, text=time, font=('Helvetica 12'), bd=1, relief="solid", padx=10, pady=5)
        lbl_time.grid(row=times.index(time) + 1, column=0, sticky="nsew")
        for i in range(1, 8):
            # Find events for the corresponding day and time

            events_for_cell = []

            for event in weekly_events:
                utc_datetime2 = datetime.utcfromtimestamp(event["When"]["start_time"])
                utc_datetime3 = datetime.utcfromtimestamp(event["When"]["end_time"])

                # Set the UTC time zone
                utc_timezone = pytz.timezone('UTC')
                utc_datetime2 = utc_timezone.localize(utc_datetime2)
                utc_datetime3 = utc_timezone.localize(utc_datetime3)

                # Convert to Eastern Time (EST)
                est_timezone = pytz.timezone('US/Eastern')
                est_datetime2 = utc_datetime2.astimezone(est_timezone)
                est_datetime3 = utc_datetime3.astimezone(est_timezone)

                tempstart = est_datetime2.replace(minute = 0,second=0, microsecond=0)
                tempend = est_datetime3.replace(second=0, microsecond=0)

                if (tempend.minute != 0):
                    tempend = (tempend + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
                

                if (time == "00:00AM"):
                    start_date_condition = est_datetime2.date() == start_date_of_week + timedelta(days=i - 1)
                    start_time_condition = compare_24_hour_times(convert_to_24_hour_time(convert_to_12_hour_time(tempstart)),convert_to_24_hour_time("12:00AM"))
                    end_time_condition = compare_24_hour_times(convert_to_24_hour_time(convert_to_12_hour_time(tempend)),convert_to_24_hour_time("12:00AM"))
                else:
                    start_date_condition = est_datetime2.date() == start_date_of_week + timedelta(days=i - 1)
                    start_time_condition = compare_24_hour_times(convert_to_24_hour_time(convert_to_12_hour_time(tempstart)),convert_to_24_hour_time(time))
                    end_time_condition = compare_24_hour_times(convert_to_24_hour_time(convert_to_12_hour_time(tempend)),convert_to_24_hour_time(time))
                if(start_date_condition):
                    print(convert_to_12_hour_time(tempstart))
                    print(convert_to_24_hour_time(convert_to_12_hour_time(tempend)))
                    print("curr"+time)
                    print(start_time_condition)
                    print(end_time_condition)
                pmandam = 0
                if (("AM" in convert_to_12_hour_time(tempstart)) and ("AM" in time)) or (("PM" in convert_to_12_hour_time(tempstart)) and ("PM" in time)):
                    pmandam = 1

                if start_date_condition and (start_time_condition == 0 or start_time_condition == 2 ) and (end_time_condition == 1 or end_time_condition == 2) and pmandam == 1:
                    
                    events_for_cell.append(event["Title"])


            # Display events in the label
            lbl_cell = tk.Label(masterFrame, text="\n".join(events_for_cell), font=('Helvetica 12'), bd=1, relief="solid", padx=10, pady=5)
            lbl_cell.grid(row=times.index(time) + 1, column=i, sticky="nsew")

    # Configuring column weights so they are all equal
    for col in range(8):
        masterFrame.grid_columnconfigure(col, weight=1)

    # Configuring row weights so they are all equal
    for row in range(25):
        masterFrame.grid_rowconfigure(row, weight=1)

    # Button to trigger the transition to the second page
    switch_button = tk.Button(masterFrame, text="Switch to Main UI", command=lambda: switch_to_main_ui(root, name)).grid(row=26, column=0,padx= (10, 0), pady=(5, 2))
