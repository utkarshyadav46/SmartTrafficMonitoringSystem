import cv2
import threading
import tkinter as tk
from PIL import Image, ImageTk
import requests
import base64
import json
import time
import os
import csv
window = tk.Tk()  #Makes main window
window.wm_title("SMART TRAFFIC MANAGEMENT")
window.columnconfigure(0, {'minsize': 1020})
window.columnconfigure(1, {'minsize': 335})

RLV_case = 0 
c=0

frame=tk.Frame(window)
frame.grid(row=0,column=0,rowspan=5,sticky='N',pady=10)

frame2=tk.Frame(window)
frame2.grid(row=0,column=1)

frame3=tk.Frame(window)
frame3.grid(row=1,column=1)

frame4=tk.Frame(window)
frame4.grid(row=2,column=1)

frame5=tk.Frame(window)
frame5.grid(row=3,column=1)

frame2.rowconfigure(1, {'minsize': 250})
frame3.rowconfigure(1, {'minsize': 80})
frame4.rowconfigure(1, {'minsize': 150})
frame5.rowconfigure(1, {'minsize': 50})

global mode
global snap
snap=1
mode=1
def speedmode():
    global mode
    mode=1
def redlightmode():
    global mode
    mode=2

def screenshot():
    global snap
    snap=0
    print("yo")

lbl1 = tk.Label(frame,text='Vehicle Detection And Tracking',font = "verdana 12 bold")
lbl1.pack(side='top')
tk.Button(frame,text='Screenshot',command=screenshot).pack(side='left')
tk.Button(frame,text='OverSpeed',command=speedmode).pack(side='left')
tk.Button(frame,text='RedlightCrossing',command=redlightmode).pack(side='left')
lbl2 = tk.Label(frame2,text='Vehicle Breaking Traffic Rule',font = "verdana 10 bold")
lbl2.grid(row=0,column=0,sticky ='S',pady=10)

lbl3 = tk.Label(frame3,text='Veicle Speed',font = "verdana 10 bold")
lbl3.grid(row=0,column=0,sticky ='S',pady=10)


lbl4 = tk.Label(frame4,text='Detected License Plate',font = "verdana 10 bold")
lbl4.grid(row=0,column=0)

lbl5 = tk.Label(frame5,text='Extracted License Plate Number',font = "verdana 10 bold")
lbl5.grid(row=0,column=0)

display1 = tk.Label(frame)
display1.pack(side='bottom')  #Display 1

display2 = tk.Label(frame2)
display2.grid(row=1,column=0) #Display 2


display3 = tk.Label(frame3,text="UTKARSH",font = "verdana 14 bold",fg='violet')
display3.grid(row=1,column=0)

display4 = tk.Label(frame4)
display4.grid(row=1,column=0)

display5 = tk.Label(frame5,text="",font = "verdana 24 bold",fg='blue')
display5.grid(row=1,column=0)
masterframe=None
started= False


cap=cv2.VideoCapture('s3.mp4')
frames_count, fps, width, height = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS), cap.get(
    cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

width = int(width)
height = int(height)
print(frames_count, fps, width, height)
sub = cv2.createBackgroundSubtractorMOG2()  # create background subtractor
ret,imgF=cap.read(0)
imgF=Image.fromarray(imgF)
im_width, im_height = imgF.size
xl1=0
xl2=im_width-1
yl1=im_height*0.5
yl2=yl1
ml1=(yl2-yl1)/(xl2-xl1)
intcptl1=yl1-ml1*xl1

count=0
xl3=0
xl4=im_width-1
yl3=im_height*0.25
yl4=yl3
ml2=(yl4-yl3)/(xl4-xl3)
intcptl2=yl3-ml2*xl3

xl5=0
xl6=im_width-1
yl5=im_height*0.1
yl6=yl5
ml3=(yl6-yl5)/(xl6-xl5)
intcptl3=yl5-ml3*xl5
ret=True
start=time.time()
SECRET_KEY ='sk_d0c0bbf04efa9eed87183e89'
url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY) 
    
def getlicence(filename2,label,label1,label2):
    global c
    print("Gl")
    s = set()
    with open('violation.csv', 'r') as csvr:
        reader = csv.DictReader(csvr)
        for row in reader:
            s.add(row['Vid'])
    print(s)
    
    if filename2 in s:
        print("Already exist\n")
        with open('violation.csv', 'r') as csvr:
            reader = csv.DictReader(csvr)
            for row in reader:
                if (filename2==row['Vid']):
                    label2.config(text=(row['LP']))
        fname = filename2[:-4]
        if int(fname.strip("Redlight ")) <= c:
            vehicle_path = "VD/"+filename2[:-4]+".png"
            frame_image = ImageTk.PhotoImage(Image.open(vehicle_path).resize((200,200), Image.ANTIALIAS))
            label.config(image=frame_image)
            label.image = frame_image
            lic_path = "LPD/"+filename2[:-4]+"_lpd.png"
            frame_image1 = ImageTk.PhotoImage(Image.open(lic_path).resize((150,30), Image.ANTIALIAS))
            label1.config(image=frame_image1)
            label1.image = frame_image1
            time.sleep(2)
                
    else:
        with open('violation.csv', 'a') as csvw:
            with open('Violated/'+filename2, 'rb') as i:
                img_base64 = base64.b64encode(i.read())
                r = requests.post(url, data = img_base64)
                y= json.dumps(r.json(), indent=2)
                js = json.loads(y)
                print(type(js),filename2)
                try:
                    lx1=js['results'][0]['coordinates'][0]['x']
                    ly1=js['results'][0]['coordinates'][0]['y']
                    lx2=js['results'][0]['coordinates'][2]['x']
                    ly2=js['results'][0]['coordinates'][2]['y']
                    LP=js['results'][0]['plate']
                    vh= js['results'][0]['vehicle_region']['height']
                    vw= js['results'][0]['vehicle_region']['width']
                    vx=js['results'][0]['vehicle_region']['x']
                    vy=js['results'][0]['vehicle_region']['y']
                    row = [filename2, LP, lx1,ly1,lx2,ly2,vx,vy,vh,vw]
                    s.add(filename2)
                    img = cv2.imread("Violated/"+filename2)
                    crop_img = img[vy:vy+vh, vx:vx+vw]
                    vehicle_path = "VD/"+filename2[:-4]+".png"
                    cv2.imwrite(vehicle_path,crop_img)
                    crop_lic = img[ly1:ly2, lx1:lx2]
                    lic_path = "LPD/"+filename2[:-4]+"_lpd.png"
                    cv2.imwrite(lic_path,crop_lic)
                    writer = csv.writer(csvw)
                    writer.writerow(row)
                    print("write on csv file")
                    vehicle_path = "VD/"+filename2[:-4]+".png"
                    frame_image = ImageTk.PhotoImage(Image.open(vehicle_path).resize((200,200), Image.ANTIALIAS))
                    label.config(image=frame_image)
                    label.image = frame_image
                    lic_path = "LPD/"+filename2[:-4]+"_lpd.png"
                    frame_image1 = ImageTk.PhotoImage(Image.open(lic_path).resize((150,30), Image.ANTIALIAS))
                    label1.config(image=frame_image1)
                    label1.image = frame_image1
                    label2.config(text=(LP))
                    print("Succefully caught  ")
                    time.sleep(2)
                except:
                    pass
                csvw.close()
#except:
     #   pass        
def ShowViolatedcase():
    global c
    while True:
        for file in os.listdir("Violated/"):
            getlicence(file,display2,display4,display5)
        time.sleep(1)


def stream(label):
    global snap,c
    while True:
        _,iframe = cap.read()
        if(snap%2==0):
            cv2.imwrite("Violated/Redlight {}.png".format(c),iframe)
            s=s+1
            snap=1
        if(mode==1):
            cv2.line(iframe, (int(xl1),int(yl1)), (int(xl2),int(yl2)), (0,255,0),3)
            cv2.line(iframe, (int(xl3),int(yl3)), (int(xl4),int(yl4)), (0,0,255),3)
            cv2.line(iframe, (int(xl5),int(yl5)), (int(xl6),int(yl6)), (255,0,0),3)
        else:
            cv2.line(iframe, (int(xl3),int(yl3)), (int(xl4),int(yl4)), (0,0,255),3)
        frame=cv2.resize(iframe,(700,500))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        display1.imgtk = imgtk #Shows frame for display 
        display1.configure(image=imgtk)
        c=c+1
        print(c)
        time.sleep(0.7)
              
thread = threading.Thread(target=stream, args=(display1,))
thread1 = threading.Thread(target=ShowViolatedcase)
thread1.daemon = 1
thread1.start()
thread.daemon = 1
thread.start()

window.mainloop()  #Starts GUI


 