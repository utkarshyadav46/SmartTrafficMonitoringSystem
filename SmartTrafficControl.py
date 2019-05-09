import cv2
delay = -1
car_cascade = cv2.CascadeClassifier('cars.xml')
def veh_count(img_path,winname):
    img = cv2.imread(img_path)
    count = 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 3)
    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        count = count + 1
    #cv2.imshow(winname, img)
    return count


def stos_image(l, r, f, b):
    global delay
    if delay==0:
        delay = 1
    d = dict()
    d["l"]=l
    d["r"]=r
    d["f"]=f
    d["b"]=b
    mx = max(l, r, f, b)
    mn = min(l, r, f, b)
    avg = (l+r+f+b)//4
    print("Avg:",avg)
    l1q = 5
    l2q = 10
    l3q = 20
    screenshot_time = (l+f+r+b)//2
    delay = screenshot_time
    print("\n\nNext screen shot after {}sec".format(delay))
    if (avg<=l1q):
        print("No traffic jam, Allow all roads\n")
    elif (avg>l1q and avg<=l2q):
        lst = [l,f,r,b]
        x = screenshot_time
        while screenshot_time>0: 
            lst.sort()
            val = lst[0]
            lst.pop(0)
            screenshot_time = screenshot_time - val
            if val == d['l'] and x-d['l']>0:
                print("1Allow Left road for {}sec".format(min(d['l'],x)))
                x = x-d['l']
            elif val == d['r']:
                print("1Allow Right road for {}sec".format(min(d['r'],x)))
                x = x-d['r']
            elif val == d['f']:
                print("1Allow Front road for {}sec".format(min(d['f'],x)))
                x = x-d['f']
            else:
                print("1Allow Behind road for {}sec".format(min(d['b'],x)))
                x = x-d['b']
            
                
    elif (avg>l2q and avg<=l3q):
        lst = [l,f,r,b]
        while screenshot_time>0:
            lst.sort()
            val = lst[-1]
            lst.pop(-1)
            screenshot_time = screenshot_time - val//2
            if val == d['l']:
                print("2Allow Left road for {}sec".format(d['l']//2))
            elif val == d['r']:
                print("2Allow Right road for {}sec".format(d['r']//2))
            elif val == d['f']:
                print("2Allow Front road for {}sec".format(d['f']//2))
            else:
                print("2Allow Behind road for {}sec".format(d['b']//2))
            
        print("\n\n\n")

def stos_video(vidl, vidr, vidf, vidb):
    global delay
    l, r, f, b, c = 0, 0, 0, 0, 0
    a = c
    left = cv2.VideoCapture(vidl)
    front = cv2.VideoCapture(vidf)
    right = cv2.VideoCapture(vidr)
    behind = cv2.VideoCapture(vidb)
    cv2.namedWindow('left',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('left',600,350)
    cv2.moveWindow("left", 0,0); 
    cv2.namedWindow('front',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('front',600,350)
    cv2.moveWindow("front", 700,0); 
    cv2.namedWindow('right',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('right',600,350)
    cv2.moveWindow("right", 700,400); 
    cv2.namedWindow('behind',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('behind',600,350)
    cv2.moveWindow("behind", 0,400);
    while True:
        ret, frame = left.read()
        ret1, frame1 = front.read()
        ret2, frame2 = right.read()
        ret3, frame3 = behind.read()
        if c==0: #For first time
            #cv2.imwrite('Violated\speeding_%s.png' %c, frame)
            cv2.imwrite("Screenshots/snap_left_{}.png".format(c),frame)
            cv2.imwrite("Screenshots/snap_front_{}.png".format(c),frame1)
            cv2.imwrite("Screenshots/snap_right_{}.png".format(c),frame2)
            cv2.imwrite("Screenshots/snap_behind_{}.png".format(c),frame3)
            
            l = veh_count("Screenshots/snap_left_{}.png".format(c),"left")
            r = veh_count("Screenshots/snap_right_{}.png".format(c),"right")
            f = veh_count("Screenshots/snap_front_{}.png".format(c),"front")
            b = veh_count("Screenshots/snap_behind_{}.png".format(c),"behind")
            print(l, r, f, b)
            stos_image(l, r, f, b)
        
        if c==a+delay: 
            a = c
            #cv2.imwrite('Violated\speeding_%s.png' %c, frame)
            cv2.imwrite("Screenshots/snap_left_{}.png".format(a),frame)
            cv2.imwrite("Screenshots/snap_front_{}.png".format(a),frame1)
            cv2.imwrite("Screenshots/snap_right_{}.png".format(a),frame2)
            cv2.imwrite("Screenshots/snap_behind_{}.png".format(a),frame3)
            
            l = veh_count("Screenshots/snap_left_{}.png".format(a),"left")
            r = veh_count("Screenshots/snap_right_{}.png".format(a),"right")
            f = veh_count("Screenshots/snap_front_{}.png".format(a),"front")
            b = veh_count("Screenshots/snap_behind_{}.png".format(a),"behind")
            print(l, r, f, b)
            stos_image(l, r, f, b)
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)
        car_left = car_cascade.detectMultiScale(gray, 1.1, 3)
        car_front = car_cascade.detectMultiScale(gray1, 1.1, 3)
        car_right = car_cascade.detectMultiScale(gray2, 1.1, 3)
        car_behind = car_cascade.detectMultiScale(gray3, 1.1, 3)
        for (x,y,w,h) in car_left:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,0),4)
            l = l+1
        for (x,y,w,h) in car_front:
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,0,0),4)
            f = f+1
        for (x,y,w,h) in car_right:
            cv2.rectangle(frame2,(x,y),(x+w,y+h),(0,0,0),4)
            r = r+1
        for (x,y,w,h) in car_behind:
            cv2.rectangle(frame3,(x,y),(x+w,y+h),(0,0,0),4)
            b = b+1
        cv2.imshow('left', frame)
        cv2.imshow('front', frame1)
        cv2.imshow('right', frame2)
        cv2.imshow('behind', frame3)
        c = c+1
        print(c,delay)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        
vidl = "Videos/left.mp4"
vidf = "Videos/front.mp4"
vidr = "Videos/right.mp4"
vidb = "Videos/behind.mp4"
stos_video(vidl, vidr, vidf, vidb)
