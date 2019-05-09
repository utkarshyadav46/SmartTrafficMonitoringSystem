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
b='white'
window.configure(bg=b)
RLV_case = 0 

car_cascade = cv2.CascadeClassifier('cars.xml')
frame=tk.Frame(window,bg=b)
frame.grid(row=0,column=0,rowspan=5,sticky='N',pady=10)


frame0=tk.Frame(window ,bg=b )
frame0.place(x=400,y=600)


frame2=tk.Frame(window ,bg=b )
frame2.grid(row=0,column=1)


frame3=tk.Frame(window,bg=b)
frame3.grid(row=1,column=1)

frame4=tk.Frame(window,bg=b)
frame4.grid(row=2,column=1)

frame5=tk.Frame(window,bg=b)
frame5.grid(row=3,column=1)

frame2.rowconfigure(1, {'minsize': 250})
frame3.rowconfigure(1, {'minsize': 80})
frame4.rowconfigure(1, {'minsize': 150})
frame5.rowconfigure(1, {'minsize': 50})

global mode,stop
global snap
global title1
snap=1
mode=1
stop=0
light=0
def screenshot():
    global snap
    snap=0
    print("yo")
def lightred():
    global light
    light=1
def lightgreen():
    global light
    light=0
def billing():
    global stop
    stop=1
    window.destroy()
    import main.py
lbl1 = tk.Label(frame,text='Traffic Light Violation System',font = "verdana 12 bold",bg=b)
lbl1.pack(side='top')
tk.Button(frame0,text='Billing',command=billing).pack(side='left')
tk.Button(frame0,text='Screenshot',command=screenshot).pack(side='left')
img1 = ImageTk.PhotoImage(Image.open('snapbutton/red.jpg').resize((50,50), Image.ANTIALIAS))
tk.Button(frame0,text='Red  ',bg='Red',image=img1,command=lightred).pack(side='left')
img2 = ImageTk.PhotoImage(Image.open('snapbutton/green.jpg').resize((50,50), Image.ANTIALIAS))
tk.Button(frame0,text='Green',bg='green',image=img2,command=lightgreen).pack(side='left')
lbl2 = tk.Label(frame2,text='Vehicle Breaking Traffic Rule',font = "verdana 10 bold",bg=b)
lbl2.grid(row=0,column=0,sticky ='S',pady=10)

lbl3 = tk.Label(frame3,text='Light Status',font = "verdana 10 bold",bg=b)
lbl3.grid(row=0,column=0,sticky ='S',pady=10)


lbl4 = tk.Label(frame4,text='Detected Vehicle ',font = "verdana 10 bold",bg=b)
lbl4.grid(row=0,column=0)

lbl5 = tk.Label(frame5,text='Extracted License Plate Number',font = "verdana 10 bold",bg=b)
lbl5.grid(row=0,column=0)

display1 = tk.Label(frame)
display1.pack(side='bottom')  #Display 1

display2 = tk.Label(frame2)
display2.grid(row=1,column=0) #Display 2


display3 = tk.Label(frame3,text="",font = "verdana 14 bold",fg='violet',bg=b)
display3.grid(row=1,column=0)

display4 = tk.Label(frame4)
display4.grid(row=1,column=0)

display5 = tk.Label(frame5,text="",font = "verdana 24 bold",fg='blue')
display5.grid(row=1,column=0)
masterframe=None
started= False


cap=cv2.VideoCapture('Videos/s3.mp4')
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
    
def getlicence(filename2):
    #try:
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
                    display5.config(text=(row['LP']))
        vehicle_path = "VD/"+filename2[:-4]+".png"
        frame_image = ImageTk.PhotoImage(Image.open(vehicle_path).resize((200,200), Image.ANTIALIAS))
        display2.config(image=frame_image)
        display2.image = frame_image
        lic_path = "LPD/"+filename2[:-4]+"_lpd.png"
        frame_image1 = ImageTk.PhotoImage(Image.open(lic_path).resize((150,30), Image.ANTIALIAS))
        display4.config(image=frame_image1)
        display4.image = frame_image1
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
                    display2.config(image=frame_image)
                    display2.image = frame_image
                    lic_path = "LPD/"+filename2[:-4]+"_lpd.png"
                    frame_image1 = ImageTk.PhotoImage(Image.open(lic_path).resize((150,30), Image.ANTIALIAS))
                    display4.config(image=frame_image1)
                    display4.image = frame_image1
                    display5.config(text=(LP))
                    print("Succefully caught  ")
                except:
                    print('Error\n')
                    os.remove('Violated/'+filename2)
                    print ('filedeleted')
                    pass
                csvw.close()

def Showrlviolation():
    global stop
    while True:
        if (stop==1):
            break
        if(light==1):           
            for file in os.listdir("TLV/"):
                imgtk1 = ImageTk.PhotoImage(Image.open('TLV/'+file).resize((200,200), Image.ANTIALIAS))
                display4.imgtk = imgtk1 #Shows frame for display 
                display4.configure(image=imgtk1)
                time.sleep(2)


def stream():
    global snap,light,stop
    global title1
    c=0
    v=0
    while True:
        if (stop==1):
            break
        _,iframe = cap.read()
        iframe1=iframe
        if(snap%2==0):
            cv2.imwrite("Violated/car {}.png".format(c),iframe)
            snap=1
        crop = iframe[int(yl4):int(yl2),int(xl5):int(xl6)]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        cars = car_cascade.detectMultiScale(gray, 1.1, 3)
        for (x,y,w,h) in cars:
            cv2.rectangle(crop,(x,y),(x+w,y+h),(0,255,0),2) 
            if (y>yl6 and y<yl1)  and (y+h>yl6 and y+h<yl1) and light==1:
                cv2.imwrite("TLV/car {}.png".format(c),iframe1)
                v=v+1
        cre = cv2.resize(crop,(300,200))
        cv2image1 = cv2.cvtColor(cre, cv2.COLOR_BGR2RGBA)
        img1 = Image.fromarray(cv2image1)
        imgtk1 = ImageTk.PhotoImage(image=img1)
        display2.imgtk = imgtk1 #Shows frame for display 
        display2.configure(image=imgtk1)

        if(light==1):
            cv2.rectangle(iframe, (int(xl3),int(yl4)),(int(xl4),int(yl2)),(0,0,255), thickness=5 , lineType=8, shift=0) 
            display3.configure(text="Red Light Is On",font = "verdana 14 bold",fg='Red')
        if(light==0):
            cv2.rectangle(iframe, (int(xl3),int(yl4)),(int(xl4),int(yl2)),(0,255,0), thickness=5 , lineType=8, shift=0)
            display3.configure(text="Green Light Is On",font = "verdana 14 bold",fg='Green')
        frame=cv2.resize(iframe,(700,500))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        display1.imgtk = imgtk #Shows frame for display 
        display1.configure(image=imgtk)
        c=c+1
        print(c)
        time.sleep(1)

        
        
thread = threading.Thread(target=stream)
thread.daemon = 1
thread.start()

thread1 = threading.Thread(target=Showrlviolation)
thread1.daemon = 1
thread1.start()

window.mainloop()  #Starts GUI


