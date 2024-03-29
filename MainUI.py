from tkinter import *
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from datetime import datetime, timezone
from email.header import decode_header
from nylas import APIClient
from weather import *
import os
from dotenv import load_dotenv
import pytz
from reminder import load_reminders  # Import the load_reminders function


load_dotenv()



CALENDAR_ID = os.getenv("CALENDAR_ID")
#Calendar func
nylas = APIClient(
   os.getenv("NYLAS1"),
   os.getenv("NYLAS2"),
   os.getenv("NYLAS3")
)



def convert_to_unix_timestamp(timedate):
    tempdate = timedate.split(",")
    dt = datetime(tempdate[0], tempdate[1], tempdate[2], tempdate[3], tempdate[4], 0, tzinfo=timezone.utc)
    timestamp = int(dt.timestamp())
    return timestamp


def read_calendar_events(today):
    events_list = []
    events = nylas.events.where(calendar_id=CALENDAR_ID).all(limit=5)
    for event in events:
        utc_datetime = datetime.utcfromtimestamp(event.when['start_time'])

        utc_timezone = pytz.timezone('UTC')
        utc_datetime = utc_timezone.localize(utc_datetime)

        # Convert to Eastern Time (EST)
        est_timezone = pytz.timezone('US/Eastern')
        est_datetime = utc_datetime.astimezone(est_timezone)

        event_start_date = est_datetime.date()

                # Set the UTC time zone
        
        if event_start_date == today:
            event_dict = {
            "Title": event.title,
            "When": event.when,
            "Participants": event.participants
            }
            events_list.append(event_dict)
    return events_list
    
def create_new_calendar_event(title,loc,strt,end):
    event = nylas.events.create()
    event.title = title
    event.location = loc
    starttime = strt
    endtime = end
    newstrt = convert_to_unix_timestamp(starttime)
    newend = convert_to_unix_timestamp(endtime) #implement the participants
    event.when = {"start_time": newstrt, "end_time": newend}
    event.participants = [{"name": "My Nylas Friend", 'email': 'swag@nylas.com'}]


    event.calendar_id = CALENDAR_ID

    event.save(notify_participants=True)   


def switch_to_calendar(root, name):
    root.destroy() # Properly destroy the current Tkinter window
    # Import the Main UI code
    from calendarpage import calendarPage
    
    # Create a new window for the second page
    cal = Tk()

    # Execute the second page code
    calendarPage(cal, name)

def switch_to_maps(root, name):
    root.destroy() # Properly destroy the current Tkinter window
    # Import the Main UI code
    from maps import mapsPage
    
    # Create a new window for the second page
    map = Tk()

    # Execute the second page code
    mapsPage(map, name)

def switch_to_remin(root, name):
    root.destroy()  # Destroy the current window
    from reminder import reminderPage
    rem = Tk()
    reminderPage(rem, name)  # Pass the username to the reminder page


def main_ui_code(root, welcome_name):
    root.title("Smart Mirror Main")  # title of the GUI window
    root.geometry("1060x1300")  # specify the max size the window can expand to
    root.config(bg="black")  # specify background color
    root.wm_attributes('-transparentcolor', '#ab23ff')

    #create_new_calendar_event()
    #read_calendar_events()
        
    #email functionality

    # Gmail account details for sending
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    email_address = 'shawnb.nimal22@gmail.com'  # Replace with your Gmail address
    password = ''  # Replace with your Gmail password or App Password

    # Gmail account details for receiving
    imap_server = 'imap.gmail.com'
    imap_port = 993

    # Function to send an email
    def send_email():
        subject = 'Hello from Python'
        message = 'This is a test email from Python.'
        sender = email_address
        receiver = 'shawn.nimal@gmail.com'  # Replace with the recipient's email address

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_address, password)
            server.sendmail(sender, receiver, msg.as_string())
            print('Email sent successfully')
            server.quit()
        except Exception as e:
            print(f'Error sending email: {str(e)}')

    # Function to receive and display the first 5 emails from newest to oldest
    def receive_and_display_emails():
        try:
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(email_address, password)
        except Exception as e:
            print(f'Error connecting to the IMAP server: {str(e)}')
            exit(1)

        mailbox = "INBOX"
        mail.select(mailbox)

        status, email_ids = mail.search(None, "ALL")

        if status == "OK":
            email_id_list = email_ids[0].split()
            # Display only the first 5 emails
            for email_id in email_id_list[-5:]:
                status, email_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    subject_header = msg["Subject"]
                    subject = ""
                    if subject_header:
                        subject, _ = decode_header(subject_header)[0]

                    sender_header = msg["From"]
                    sender = ""
                    if sender_header:
                        sender, _ = decode_header(sender_header)[0]

                    print(f"Subject: {subject}")
                    print(f"From: {sender}")
                    print("\n")

        mail.close()
        mail.logout()

    #use of send email and receive email functions

    def update_time():
        current_time = time.strftime('%H:%M:%S')
        clock_label.config(text=current_time)
        root.after(1000, update_time)  # Update every 1000 milliseconds (1 second)

    events = read_calendar_events(datetime.now().date())

    #Main layout frames
    left_frame = Frame(root, width=250, height=950, bg='grey')
    left_frame.grid(row=0, column=0, padx=10, pady=5,sticky=NSEW )


    mid_frame = Frame(root, width=500, height=950, bg='grey')
    mid_frame.grid(row=0, column=2, padx=10, pady=5, sticky=NSEW)

    right_frame = Frame(root, width=250, height=1050, bg='grey')
    right_frame.grid(row=0, column=3, padx=10, pady=5, sticky=NSEW)

    #Individual components 
    #left
    Name_frame = Frame(left_frame, width=230, height=100, bg='blue')
    Name_frame.grid(row=0, column=0, padx=10, pady=5, sticky=NSEW)

    Label(Name_frame, text= "Welcome", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0, column=0,padx= (15, 0), pady=(10, 2))
    Label(Name_frame, text= welcome_name, font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (65, 0), pady=(0, 10))


    Calendar_frame = Frame(left_frame, width=230, height=570, bg='blue')
    Calendar_frame.grid(row=1, column=0, padx=10, pady=5, sticky=NSEW)

    Label(Calendar_frame, text= "Daily View", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0, column=0, padx= (35, 25),  pady=(5,15))
    if len(events) == 0:
        Label(Calendar_frame, text= "EMPTY", font= ('Helvetica 15'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (10, 0), pady=(10, 2))
    titlemark = 1
    timemark1 = 2
    timemark2 = 3
    timemark3 = 4
    timemark4 = 5
    timemark5 = 6
    for x in events: 
        print(x)
        if(titlemark == 17):
            break

        temp1 = datetime.utcfromtimestamp(x["When"]['start_time'])
        temp2 = datetime.utcfromtimestamp(x["When"]['end_time'])

        utc_timezone = pytz.timezone('UTC')
        utc_datetime1 = utc_timezone.localize(temp1)
        utc_datetime2 = utc_timezone.localize(temp2)

            # Convert to Eastern Time (EST)
        est_timezone = pytz.timezone('US/Eastern')
        est_datetime1 = utc_datetime1.astimezone(est_timezone)
        est_datetime2 = utc_datetime2.astimezone(est_timezone)

        strt = str(est_datetime1).split(" ")
        end = str(est_datetime2).split(" ")
        
        Label(Calendar_frame, text= x["Title"], font= ('Helvetica 15'), fg='black', bg= 'blue').grid(row=titlemark, column=0,padx= (10, 0), pady=(10, 2))
        Label(Calendar_frame, text=  strt[0], font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=timemark1, column=0,padx= (10, 0) )
        Label(Calendar_frame, text=  strt[1], font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=timemark2, column=0,padx= (10, 0) )
        Label(Calendar_frame, text=  "to", font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=timemark3, column=0,padx= (10, 0) )
        Label(Calendar_frame, text=  end[0], font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=timemark4, column=0,padx= (10, 0) )
        Label(Calendar_frame, text=  end[1], font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=timemark5, column=0,padx= (10, 0), pady=(0, 20) )
        titlemark = titlemark + 6
        timemark1 = timemark1 + 6
        timemark2 = timemark2 + 6
        timemark3 = timemark3 + 6
        timemark4 = timemark4 + 6
        timemark5 = timemark5 + 6


    Reminder_frame = Frame(left_frame, width=230, height=250, bg='blue')
    Reminder_frame.grid(row=2, column=0, padx=10, pady=5, sticky=NSEW)

    # Reminder frame code
    Reminder_frame = Frame(left_frame, width=230, height=250, bg='blue')
    Reminder_frame.grid(row=2, column=0, padx=10, pady=5, sticky=NSEW)

    Label(Reminder_frame, text="Reminders", font=('Helvetica 20'), fg='black', bg='blue').grid(row=0, column=0,
                                                                                               padx=(35, 25),
                                                                                               pady=(5, 10))

    # Load incomplete reminders
    # Correction in MainUI.py to pass the 'username' argument to 'load_reminders'
    incomplete_reminders, _ = load_reminders(welcome_name)

    # Dynamically create a checkbutton for each incomplete reminder
    for i, reminder in enumerate(incomplete_reminders):
        var = IntVar()
        Checkbutton(Reminder_frame, text=reminder, font=('Helvetica 12'), fg='black', bg='blue', variable=var,
                    onvalue=1, offvalue=0).grid(row=i + 1, column=0, padx=(20, 15), pady=(5, 15), sticky=W)




    #Right
    Clock_frame = Frame(right_frame, width=230, height=400, bg='blue')
    Clock_frame.grid(row=0, column=0, padx=10, pady=5, sticky=NSEW)

    clock_label = Label(Clock_frame, font= ('Helvetica 30'), fg='black', bg= 'blue')
    clock_label.grid(row=0, column=0,padx=35, pady=25, sticky=NSEW)

    Weather_frame = Frame(right_frame, width=230, height=200, bg='blue')
    #Weather_frame = updateGUI(getForecast("Toronto"), Weather_frame)
    Weather_frame.grid(row=1, column=0, padx=10, pady=5, sticky=NSEW)

    Maps_frame = Frame(right_frame, width=230, height=490, bg='blue')
    Maps_frame.grid(row=3, column=0, padx=10, pady=5, sticky=NSEW)

    Tasks_frame = Frame(right_frame, width=230, height=120, bg='blue')
    Tasks_frame.grid(row=4, column=0, padx=10, pady=5, sticky=NSEW)

    Label(Tasks_frame, text= "Quick Tasks", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0, column=0, padx= (35, 25),  pady=(5,0))

    Label(Tasks_frame, text= "How long to work", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (10, 0), pady=(5, 2))
    Label(Tasks_frame, text= "Weather tonight", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=2, column=0,padx= (10, 0), pady=(5, 2))
    Label(Tasks_frame, text= "Set reminder to do work", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=3, column=0,padx= (10, 0), pady=(5, 2))


    switch_button = Button(left_frame, text="Switch to calendar", command=lambda: switch_to_calendar(root, welcome_name)).grid(row=4, column=0,padx= (10, 0), pady=(5, 2))
    switch_button1 = Button(left_frame, text="Switch to reminders", command=lambda: switch_to_remin(root, welcome_name)).grid(row=5, column=0,padx= (10, 0), pady=(5, 2))
    switch_button1 = Button(left_frame, text="Switch to maps", command=lambda: switch_to_maps(root, welcome_name)).grid(row=6, column=0,padx= (10, 0), pady=(5, 2))
    #if statement which constantly returns true to make the timer refresh and tick
    if True:
        update_time()
        root.mainloop()

# Create the Tkinter root window
#root = Tk()  # create root window
#root.title("Smart Mirror Main")  # title of the GUI window
#root.geometry("1060x1300")  # specify the max size the window can expand to
#root.config(bg="black")  # specify background color
#root.wm_attributes('-transparentcolor', '#ab23ff')

# Call the main_ui_code function with the root window as an argument
#main_ui_code(root)