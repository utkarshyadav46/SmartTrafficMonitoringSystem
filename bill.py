import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import csv
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import *
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from oauth2client import file
import qrcode


root = tk.Tk()
root.title("Smart Traffic Management System")
root.geometry('{}x{}'.format(1600, 800))
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret_926951424301-tpkkkohkg7mqle9kvq71n9s4d19b5ruh.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Gmail API Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    if attachmentFile:
        message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
    else: 
        message1 = CreateMessageHtml(sender, to, subject, msgHtml, msgPlain)
    result = SendMessageInternal(service, "me", message1)
    return result

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        tkMessageBox.showinfo("Notification sent", "\nYour Mail has been sent\n")
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def CreateMessageHtml(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_string().encode('UTF-8')).decode('ascii')}

def createMessageWithAttachment(
    sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients          
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(attachmentFile)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode((message.as_string()).encode('UTF-8')).decode('ascii')}
Lic_inp = StringVar()
email_inp= StringVar()
def send_mail():
    print("to email :",email_inp.get())
    lic=Lic_inp.get()
    to = email_inp.get()
    sender = "psdnavinash2@gmail.com"
    msgHtml = "Hello,<br><br> This mail is sended by us to inform you that as you have violated the act you have to pay the penalty.For more Clarification or proof of your work wrong dues we have attached the qrcode just scan it and access to your proof for self satisfaction<br>Thanking You,<br><br><b>UAY Traffic Management System(UTMS)\n  "
    subject = "RE: IMPOSING FINE ON THE VIOLATION OF TRAFFIC RULES"
    msgPlain = "Car No :"+lic
    #SendMessage(sender, to, subject, msgHtml, msgPlain)
    # Send message with attachment: 
    SendMessage(sender, to, subject, msgHtml, msgPlain, 'code.png')




###################################################################################################
####################################################################################################

def read():
    tree.delete(*tree.get_children())
    with open('violation.csv', 'r') as csvr:
        reader = csv.DictReader(csvr)
        for row in reader:
            tree.insert('', 'end', values=(row['Vid'], row['LP']))
    csvr.close()

# create all of the main containers
top_frame = tk.Frame(root, width=1600, height=50, pady=10)
label_info = tk.Label(top_frame, font = ('arial',40,'bold'), text ="Smart Traffic Management System", fg = "blue", bd = 10, anchor = 'w',padx=80)
label_info.grid(row=0,column=5)
center = tk.Frame(root, bg='gray2', width=50, height=40, padx=3, pady=3)
btm_frame = tk.Frame(root, width=450, height=45, pady=3)
email = tk.Entry(btm_frame,font=('arial',10,'bold'), textvariable=email_inp, bd=10, insertwidth =4,bg = "white", justify ='right')
email.place(width=400)
img3 = ImageTk.PhotoImage(Image.open('snapbutton/emaili.jpg').resize((50,30), Image.ANTIALIAS))
panel = tk.Button(btm_frame, image = img3,command = send_mail)
panel.grid(row=0,column=20)
btm_frame2 = tk.Frame(root, bg='lavender', width=450, height=60, pady=3)
btn_read = tk.Button(top_frame, width=10, text="Show Files",command = read)
btn_read.grid(row=1,column=10)
# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")
btm_frame2.grid(row=4, sticky="ew")


def showinfo():
    with open('violation.csv', 'r') as csvr:
        reader = csv.DictReader(csvr)
        for row in reader:
            if row['LP']==Lic_inp.get():
                scr_name = row['Vid']
                print(scr_name)
                LPN.config(text ='License Plate Number:'+(row['LP']))
                Make.config(text ='\tMake: '+(row['make']))
                #Color.config(text = (row['color']))
                #Body.config(text = (row['body_type']))
                #Model.config(text = (row['model']))
                frame_image11 = ImageTk.PhotoImage(Image.open("Violated/"+scr_name).resize((250,250), Image.ANTIALIAS))
                img_label11.config(image=frame_image11)
                img_label11.image = frame_image11
                frame_image12 = ImageTk.PhotoImage(Image.open("VD/"+scr_name).resize((250,250), Image.ANTIALIAS))
                img_label12.config(image=frame_image12)
                img_label12.image = frame_image12
                frame_image13 = ImageTk.PhotoImage(Image.open("LPD/"+scr_name[:-4]+'_lpd.png').resize((250,50), Image.ANTIALIAS))
                img_label13.config(image=frame_image13)
                img_label13.image = frame_image13
                url = qrcode.make(''+'\nDEVLOPED BY Smart Traffic Management System\n'+'License Plate Number :'+Lic_inp.get()+'\n'+'State :Rajasthan'+'\nCity:Jaipur')
                url.save('code.png')
                frame_image2 = ImageTk.PhotoImage(Image.open("code.png").resize((160,160), Image.ANTIALIAS))
                img_label.config(image=frame_image2)
                img_label.image = frame_image2
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = tk.Frame(center, bg='blue', width=500, height=190)
ctr_mid = tk.Frame(center, width=450, height=190, padx=3, pady=3)
ctr_right = tk.Frame(center, bg='white', width=400, height=190, padx=3, pady=3)
tk.Label(ctr_left, font = ('arial',14,'bold'), text ="License Plate No.", fg = "White",bg='Blue', bd = 10, anchor = 'w').grid(row=0,column=0)
lic_no = tk.Entry(ctr_left,font=('arial',10,'bold'), textvariable=Lic_inp, bd=10, insertwidth =4,bg = "powder blue", justify ='right')
lic_no.grid(row=1,column=0)
btn_read = tk.Button(ctr_left, width=10, text="Show Info.",bd=10,command = showinfo)
btn_read.grid(row=1,column=2)

ctr_left.grid(row=0, column=0, sticky="ns")
img_label = tk.Label(ctr_left,bg='blue', anchor = 'w')
img_label.grid(row=4,column=0)
img_label11 = tk.Label(ctr_mid, anchor = 'w')
img_label11.grid(row=5,column=0)
img_label12 = tk.Label(ctr_mid, anchor = 'w')
img_label12.grid(row=5,column=1)
img_label13 = tk.Label(ctr_mid, anchor = 'w')
img_label13.grid(row=6,column=1)
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")
tk.Label(ctr_mid, font = ('arial',18,'bold'), text ="Detail Box", fg = "Black", bd = 10, anchor = 'w').grid(row=0,column=0)
LPN = tk.Label(ctr_mid, font = ('arial',10,'bold'), text ="", fg = "blue", bd = 10, anchor = 'w')
LPN.grid(row=1,column=0)
Make = tk.Label(ctr_mid, font = ('arial',10,'bold'), text ="", fg = "blue",  bd = 10, anchor = 'w')
Make.grid(row=1,column=1)
Color=tk.Label(ctr_mid, font = ('arial',10,'bold'), text ="", fg = "blue",  bd = 10, anchor = 'w')
Color.grid(row=2,column=0)
Body = tk.Label(ctr_mid, font = ('arial',10,'bold'), text ="", fg = "blue",  bd = 10, anchor = 'w')
Body.grid(row=2,column=1)
Model = tk.Label(ctr_mid, font = ('arial',10,'bold'), text ="", fg = "blue",  bd = 10, anchor = 'w')
Model.grid(row=3,column=0)


##############################################################################################################
#############################################################################################################



scrollbary = tk.Scrollbar(ctr_right, orient='vertical')
scrollbarx = tk.Scrollbar(ctr_right, orient='horizontal')
tree = ttk.Treeview(ctr_right, columns=("Screenshot", "License_Plate","category"), selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side='right')
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side='bottom')
tree.heading('Screenshot', text="Screenshot")
tree.heading('License_Plate', text="License_Plate")
tree.heading('category', text="Category")
tree.column('#0', stretch='no', minwidth=0, width=0)
tree.column('#1', stretch='no', minwidth=0, width=80)
tree.column('#2', stretch='no', minwidth=0, width=100)
tree.pack()
root.mainloop()




def Send_email():
    global e
    global License
    e=e.get()
    plateno=License.get()
    print(plateno)
    state = plateno[0:4] 
    print(state)# now t points to the new string 'll'
    with open('RTO.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['RegNo'] == state:
                print(row['Place'],"\n",row['State'])
                break;
    to = e
    sender = "psdnavinash2@gmail.com"
    msgHtml = "Hello,<br><br> This mail is sended by us to inform you that as you have violated the act you have to pay the penalty.For more Clarification or proof of your work wrong dues we have attached the qrcode just scan it and access to your proof for self satisfaction<br>Thanking You,<br><br><b>UAY Traffic Management System(UTMS)\n  "
    subject = "RE: IMPOSING FINE ON THE VIOLATION OF TRAFFIC RULES"
    msgPlain = "Hi\nPlain Email"
    #SendMessage(sender, to, subject, msgHtml, msgPlain)
    # Send message with attachment: 
    SendMessage(sender, to, subject, msgHtml, msgPlain, 'code.png')
