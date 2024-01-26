from tkinter import *
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from datetime import datetime, timezone
from email.header import decode_header
from nylas import APIClient
from weather import *
from micInput import *

CALENDAR_ID = ""
#Calendar func
nylas = APIClient(
   "",
   "",
   ""
)

def convert_to_unix_timestamp(timedate):
    tempdate = timedate.split(",")
    dt = datetime(tempdate[0], tempdate[1], tempdate[2], tempdate[3], tempdate[4], 0, tzinfo=timezone.utc)
    timestamp = int(dt.timestamp())
    return timestamp

def read_calendar_events():
    events = nylas.events.where(calendar_id=CALENDAR_ID).all(limit=5)
    for event in events:
        print("Title: {} | When: {} | Participants: {}".format(
        event.title, event.when, event.participants
    ))
    
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

root = Tk()  # create root window
root.title("Smart Mirror Main")  # title of the GUI window
root.geometry("1060x1300")  # specify the max size the window can expand to
root.config(bg="black")  # specify background color


root.wm_attributes('-transparentcolor', '#ab23ff')

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
Label(Name_frame, text= "{Name}", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (65, 0), pady=(0, 10))


Calendar_frame = Frame(left_frame, width=230, height=570, bg='blue')
Calendar_frame.grid(row=1, column=0, padx=10, pady=5, sticky=NSEW)

Label(Calendar_frame, text= "Daily View", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0, column=0, padx= (45, 25),  pady=(5,15))


Label(Calendar_frame, text= "Temp Calendar 1", font= ('Helvetica 15'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (10, 0), pady=(10, 2))
Label(Calendar_frame, text= "Placeholder time", font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=2, column=0,padx= (28, 0), pady=(0, 30), sticky=W)

Label(Calendar_frame, text= "Temp Calendar 1", font= ('Helvetica 15'), fg='black', bg= 'blue').grid(row=3, column=0,padx= (10, 0), pady=(10, 2))
Label(Calendar_frame, text= "Placeholder time", font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=4, column=0,padx= (28, 0), pady=(0, 30), sticky=W)

Label(Calendar_frame, text= "Temp Calendar 1", font= ('Helvetica 15'), fg='black', bg= 'blue').grid(row=5, column=0,padx= (10, 0), pady=(10, 2))
Label(Calendar_frame, text= "Placeholder time", font= ('Helvetica 10'), fg='black', bg= 'blue').grid(row=6, column=0,padx= (28, 0), pady=(0, 60), sticky=W)

Reminder_frame = Frame(left_frame, width=230, height=250, bg='blue')
Reminder_frame.grid(row=2, column=0, padx=10, pady=5, sticky=NSEW)
var1 = IntVar()

Label(Reminder_frame, text= "Reminders", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0,  column=0, padx= (35, 25),  pady=(5,10))

Checkbutton(Reminder_frame, text='Reminder 1',font=('Helvetica 12'),fg='black', bg= 'blue', variable=var1, onvalue=1, offvalue=0).grid(row=1,  column=0, padx= (20 ,15),  pady=(5,15), sticky=W)



#Right
Clock_frame = Frame(right_frame, width=230, height=400, bg='blue')
Clock_frame.grid(row=0, column=0, padx=10, pady=5, sticky=NSEW)

clock_label = Label(Clock_frame, font= ('Helvetica 30'), fg='black', bg= 'blue')
clock_label.grid(row=0, column=0,padx=35, pady=25, sticky=NSEW)

Weather_frame = Frame(right_frame, width=230, height=200, bg='blue')
Weather_frame = updateGUI(getForecast("Toronto"), Weather_frame)
Weather_frame.grid(row=1, column=0, padx=10, pady=5, sticky=NSEW)

Maps_frame = Frame(right_frame, width=230, height=490, bg='blue')
Maps_frame.grid(row=3, column=0, padx=10, pady=5, sticky=NSEW)

Tasks_frame = Frame(right_frame, width=230, height=120, bg='blue')
Tasks_frame.grid(row=4, column=0, padx=10, pady=5, sticky=NSEW)

Label(Tasks_frame, text= "Quick Tasks", font= ('Helvetica 20'), fg='black', bg= 'blue').grid(row=0, column=0, padx= (35, 25),  pady=(5,0))

Label(Tasks_frame, text= "How long to work", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=1, column=0,padx= (10, 0), pady=(5, 2))
Label(Tasks_frame, text= "Weather tonight", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=2, column=0,padx= (10, 0), pady=(5, 2))
Label(Tasks_frame, text= "Set reminder to do work", font= ('Helvetica 12'), fg='black', bg= 'blue').grid(row=3, column=0,padx= (10, 0), pady=(5, 2))

#MIC INPUT
def runMic():
    while True:
        print("in while loop")
        if(listen()):
            getVoiceCommand()
            response = transcribeCommand()
            print(response["text"])

            if("bye" in response["text"].lower()):
                print("goodbye sire")
                break

#if statement which constantly returns true to make the timer refresh and tick
if __name__ == "__main__":
    update_time()
    root.after(0, runMic)
    root.mainloop()
    
