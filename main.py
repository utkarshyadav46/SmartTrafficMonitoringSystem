# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 04:42:05 2019

@author: Utkarsh Yadav
"""

import tkinter as tk
from PIL import Image, ImageTk
root=tk.Tk()
root.title('Smart Traffic Management System (Using Image Processing)')
root.geometry('1000x800+0+0')
root.configure(bg='White')
lbl1 = tk.Label(root,text='Smart Traffic Management System (IMAGE PROCESSING)',font = "verdana 14 bold",bg='White',fg='Blue')
lbl1.pack(side='top')
def rule_breaker():
    root.destroy()

def  billing():
    root.destroy()
    import  bill.py
def  smto():
    root.destroy()
    print("smto")
    import  SmartTrafficControl.py
def red_light():
    root.destroy()
    import redlight1.py
def  toll():
    root.destroy()
    print("smto")
    import  toll.py

img = ImageTk.PhotoImage(Image.open('snapbutton/tl.jpg').resize((200,200), Image.ANTIALIAS))
panel = tk.Button(root, image = img,command=red_light)
panel.place(x=150,y=100)

img1 = ImageTk.PhotoImage(Image.open('snapbutton/toll.jpg').resize((200,200), Image.ANTIALIAS))
panel = tk.Button(root, image = img1,command=toll)
panel.place(x=400,y=100)

img2 = ImageTk.PhotoImage(Image.open('snapbutton/speed.jpg').resize((200,200), Image.ANTIALIAS))
panel = tk.Button(root, image = img2,command=rule_breaker)
panel.place(x=250,y=350)

img3 = ImageTk.PhotoImage(Image.open('snapbutton/stos.jpg').resize((200,200), Image.ANTIALIAS))
panel = tk.Button(root, image = img3,command=smto)
panel.place(x=650,y=100)
img4 = ImageTk.PhotoImage(Image.open('snapbutton/billing.png').resize((200,200), Image.ANTIALIAS))
panel = tk.Button(root, image = img4,command=billing)
panel.place(x=500,y=350)
lbl2 = tk.Label(root,text='PROJECT MEMBER :\nUtkarsh Yadav(1023)\n Avinash Chakravarthi(1020)\n Yogesh Kumar(1045)\n ',font = "verdana 10 bold",bg='White',fg='orange')
lbl2.place(x=700,y=600)
lbl3 = tk.Label(root,text='Mentor : Dr.Isha Pathak ',font = "verdana 10 bold",bg='White',fg='Blue')
lbl3.place(x=50,y=600)

root.mainloop()
