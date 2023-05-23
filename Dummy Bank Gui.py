import cv2
import numpy as np
import face_recognition
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import os
import mysql.connector
win=Tk()
win.title('Banking Appliction')
#win.iconbitmap('sbi.ico')
win.geometry('1368x768+0+0')

def finish_cap_img(a):    
    cam=cv2.VideoCapture(0)
    cv2.namedWindow("Webcam Image capture")
    img_counter=0
    while True:
       ret,frame=cam.read()
       if not ret:
           print("Failed to grab frame")
           break
       cv2.imshow("Webcam",frame)
       k=cv2.waitKey(1)
       if k%256==27:
           print("Escape Pressed Closing the Window")
           break
       elif k%256==32:
           img_name=a+"_{}.jpg".format(img_counter)
           cv2.imwrite("C:\\Users\\asus\\AppData\\Local\\Programs\\Python\\Python310\\Captured_Stored_Pictures/"+img_name, frame)
           #cv2.imwrite(img_name,frame)
           print("Image Captured Successfully")
           img_counter+=1
           break
    
    cam.release()
    cv2.destroyAllWindows()
    login()

def cap_img():
    screen=Toplevel(win)
    screen.geometry('1368x768+0+0')
    a=input("Enter Your Name To Be Saves On Picture")
    finish_cap_img(a)
    #Button(screen,text='TO Capture',font=('calibri',12),command=finish_cap_img(a)).grid(row=2)
    #notif=Label(screen,font=('Calibri',12))
    #notif.grid(row=3,sticky=N)

def finish_check():
    path='C:\\Users\\asus\\AppData\\Local\\Programs\\Python\\Python310\\Captured_Stored_Pictures'
    images=[]
    classNames=[]
    mylist=os.listdir(path)
    #print(mylist)
    for cl in mylist:        
        curImg=cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0]) 
    #print(classNames)
    def findEncodings(images):
        encodelist=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            #faceLoc = face_recognition.face_locations(img_saved)
            #cv2.rectangle(img_saved,(faceLoc[3],faceLoc[0],faceLoc[1],faceLoc[2]),(255,0,255),2)
            encodelist.append(encode) 
        return encodelist
    
    encodeListKnown=findEncodings(images)
    #findEncodings(images)
    print(len(encodeListKnown))
    print("Encoding Complete")
    cap=cv2.VideoCapture(0)
    while True:        
        success,img=cap.read()
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)           
        facesCurFrame=face_recognition.face_locations(imgS)
        encodesCurFrame=face_recognition.face_encodings(imgS,facesCurFrame) 
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            matchIndex=np.argmin(faceDis)
            print(matchIndex)
            if(matchIndex>=0):
                name=classNames[matchIndex].upper()
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

                print("You are Identified as a Valid User")          
            cv2.imshow('WebCam',img)
            cv2.waitKey(1)
            
            break;
        break;        
    cap.release()
    cv2.destroyAllWindows()
    funct()
            
def check():
    screen=Toplevel(win)
    screen.geometry('1368x768+0+0')
    finish_check()
    #Button(screen,text='Execute',font=('calibri',12),command=finish_check).grid(row=1)
    #notif=Label(screen,font=('Calibri',12))
    #notif.grid(row=2,sticky=N)


def finish_openacc():
    name=temp_name.get()
    accno=temp_accno.get()
    dob=temp_dob.get()
    address=temp_address.get()
    contact=temp_contact.get()
    openbal=temp_openbal.get()
    all_accounts=os.listdir()
    for i in all_accounts:
        if name==i:
            notif.config(fg='red',text='Account Already Exist!')
            return
    if name=="" or accno=="" or dob=="" or address=="" or contact=="" or openbal=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        data1=(name,accno,dob,address,contact,openbal)
        sql1=('insert into account values(%s,%s,%s,%s,%s,%s)')
        data2=(name,accno,openbal)
        sql2=('insert into amount values(%s,%s,%s)')
        x=mydb.cursor()
        x.execute(sql1,data1)
        x.execute(sql2,data2)
        mydb.commit()
        print('Data entered successfully')
    funct()    
def openacc():
    global temp_name
    global temp_accno
    global temp_dob
    global temp_address
    global temp_contact
    global temp_openbal
    global notif
    temp_name=StringVar()
    temp_accno=StringVar()
    temp_dob=StringVar()
    temp_address=StringVar()
    temp_contact=StringVar()
    temp_openbal=StringVar()
    screen=Toplevel(win)
    screen.title('Create New Account Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    # Calculate the x and y position to center the screen
    x_position = int((screen_width - 1368) / 2)
    y_position = int((screen_height - 768) / 2)
    # Set the screen position and size
    screen.geometry(f'1368x768+{x_position}+{y_position}')
    
    Label(screen,text='Please Enter Your Details below For Registeration',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Name',font=('calibri',12)).grid(row=2,sticky=W)
    Label(screen,text='AccNo',font=('calibri',12)).grid(row=3,sticky=W)
    Label(screen,text='DOB',font=('calibri',12)).grid(row=4,sticky=W)
    Label(screen,text='Address',font=('calibri',12)).grid(row=5,sticky=W)
    Label(screen,text='Contact',font=('calibri',12)).grid(row=6,sticky=W)
    Label(screen,text='Openbal',font=('calibri',12)).grid(row=7,sticky=W) 
    Entry(screen,textvariable=temp_name).grid(row=2)
    Entry(screen,textvariable=temp_accno).grid(row=3)
    Entry(screen,textvariable=temp_dob).grid(row=4)
    Entry(screen,textvariable=temp_address).grid(row=5)
    Entry(screen,textvariable=temp_contact).grid(row=6)
    Entry(screen,textvariable=temp_openbal).grid(row=7)
    Button(screen,text='Create New Account',font=('calibri',12),command=finish_openacc).grid(row=8)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=9)

def finish_depamt():    
    accno=temp_accno.get()
    amount=temp_amount.get()
    all_accounts=os.listdir()   
    if accno=="" or amount=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        a='select bal from amount where accno=%s'
        data=(accno,)
        x=mydb.cursor()
        x.execute(a,data)
        result=x.fetchone()
        t=result[0]+int(amount)
        sql=('update amount set bal=%s where accno=%s')
        d=(t,accno)
        x.execute(sql,d)
        mydb.commit()
        print('Amount Depoisted Successfully :: Transaction Completed')
    funct()    
def depamt():    
    global temp_accno
    global temp_amount
    global notif
    temp_accno=StringVar()
    temp_amount=StringVar()
    screen=Toplevel(win)
    screen.title('Deposit Amount Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your Account Details For Transaction Such As "Account No" and "Deposit Amount"',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Account Number',font=('calibri',12)).grid(row=2,sticky=W)
    Label(screen,text='Deposit Amount',font=('calibri',12)).grid(row=3,sticky=W)    
    Entry(screen,textvariable=temp_accno).grid(row=2)
    Entry(screen,textvariable=temp_amount).grid(row=3)
    Button(screen,text='Deposit Account',font=('calibri',12),command=finish_depamt).grid(row=4)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=5)

def finish_wtdamt():    
    accno=temp_accno.get()
    amount=temp_amount.get()
    all_accounts=os.listdir()   
    if accno=="" or amount=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        a='select bal from amount where accno=%s'
        data=(accno,)
        x=mydb.cursor()
        x.execute(a,data)
        result=x.fetchone()
        t=result[0]-int(amount)
        sql=('update amount set bal=%s where accno=%s')
        d=(t,accno)
        x.execute(sql,d)
        mydb.commit()
        print('Amount Withdraw Successfully :: Transaction Completed')
    funct()    
def wtdamt():    
    global temp_accno
    global temp_amount
    global notif
    temp_accno=StringVar()
    temp_amount=StringVar()
    screen=Toplevel(win)
    screen.title('Widthdraw Amount Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your Account Details Such As "Account No" and "Withdraw Amount" For Withdrawing Amount',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Account Number',font=('calibri',12)).grid(row=2,sticky=W)
    Label(screen,text='Withdraw Amount',font=('calibri',12)).grid(row=3,sticky=W)    
    Entry(screen,textvariable=temp_accno).grid(row=2)
    Entry(screen,textvariable=temp_amount).grid(row=3)
    Button(screen,text='Withdraw Amount',font=('calibri',12),command=finish_wtdamt).grid(row=4)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=5)

def finish_balenq():    
    accno=temp_accno.get()    
    all_accounts=os.listdir()   
    if accno=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        a='select bal from amount where accno=%s'
        data=(accno,)
        x=mydb.cursor()
        x.execute(a,data)
        result=x.fetchone()        
        mydb.commit()
        print("Your account balance is:", result)
    funct()    
def balenq():    
    global temp_accno    
    global notif
    temp_accno=StringVar()    
    screen=Toplevel(win)
    screen.title('Balance Enquiry Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your Account Details i.e "Account No" for balance enquiry',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Account Number',font=('calibri',12)).grid(row=2,sticky=W)   
    Entry(screen,textvariable=temp_accno).grid(row=2)   
    Button(screen,text='Balance Enquiry',font=('calibri',12),command=finish_balenq).grid(row=3)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=4)

def finish_displaydetails():    
    accno=temp_accno.get()    
    all_accounts=os.listdir()   
    if accno=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        a='select * from account where accno=%s'
        data=(accno,)
        x=mydb.cursor()
        x.execute(a,data)
        result=x.fetchone()        
        mydb.commit()
        print("Customer Details are:",result)
    funct()    
def displaydetails():    
    global temp_accno    
    global notif
    temp_accno=StringVar()    
    screen=Toplevel(win)
    screen.title('Account Details  Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your "Account No" for Viewing Your Account Details',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Account Number',font=('calibri',12)).grid(row=2,sticky=W)   
    Entry(screen,textvariable=temp_accno).grid(row=2)   
    Button(screen,text='Dispaly Customer Details',font=('calibri',12),command=finish_displaydetails).grid(row=3)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=4)

def finish_closeacc():    
    accno=temp_accno.get()    
    all_accounts=os.listdir()   
    if accno=="":
        notif.config(foreground='red',text='All Field is required!')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        a='delete from amount where accno=%s'
        b='delete from account where accno=%s'
        data=(accno,)
        x=mydb.cursor()
        x.execute(a,data)
        result=x.fetchone()        
        mydb.commit()
        print("Your Account is Deleted Now:",result)
    funct()    
def closeacc():    
    global temp_accno    
    global notif
    temp_accno=StringVar()    
    screen=Toplevel(win)
    screen.title('Closing Account Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your "Account No" for Closing Your Account',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Account Number',font=('calibri',12)).grid(row=2,sticky=W)   
    Entry(screen,textvariable=temp_accno).grid(row=2)   
    Button(screen,text='Close Account',font=('calibri',12),command=finish_closeacc).grid(row=3)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=4)
    
def finish_login():
    name=temp_name.get()
    password=temp_password.get()
    all_accounts=os.listdir()
    if name=="" or password=="":
        notif.config(foreground='red',text='All Field is required!')
        return        
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        x=mydb.cursor()
        x.execute('select * from register where name=%s and password=%s',(name,password))
        result=x.fetchone()
        if result==None:
            return
        else:
            notif.config(foreground='green',text='Correct Cereditials!')
            mydb.commit()
    check()

def login():
    global temp_name
    global temp_password
    global notif
    temp_name = StringVar()
    temp_password = StringVar()
    screen = Toplevel(win)
    screen.title('SBI Login Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    
    # Create a style object for customizing ttk widgets
    style = ttk.Style(screen)
    
    # Configure the style properties
    style.configure('TLabel', font=('Calibri', 12))
    style.configure('TEntry', font=('Calibri', 12))
    style.configure('TButton', font=('Calibri', 12))
    style.configure('TLabel', foreground='#333333')
    style.configure('TEntry', foreground='#666666')
    
    # Create and grid the labels
    ttk.Label(screen, text='Please Enter Your Credentials To Login').grid(row=1, sticky=N)
    ttk.Label(screen, text='Name').grid(row=2, sticky=W)
    ttk.Label(screen, text='Password').grid(row=3, sticky=W)
    
    # Create and grid the entry fields
    name_entry = ttk.Entry(screen, textvariable=temp_name, style='TEntry')
    name_entry.grid(row=2)
    password_entry = ttk.Entry(screen, textvariable=temp_password, show='*', style='TEntry')
    password_entry.grid(row=3)
    
    # Create and grid the login button
    ttk.Button(screen, text='Login', command=finish_login).grid(row=4)
    
    # Create and grid the notification label
    notif = ttk.Label(screen, font=('Calibri', 12))
    notif.grid(row=5, sticky=N)
    
def finish_reg():
    name=temp_name.get()
    password=temp_password.get()
    all_accounts=os.listdir()
    for i in all_accounts:
        if name==i and password==i:
            notif.config(foreground='red',text='Already Registered!')
            return
    if name=="" or password=="":
        notif.config(foreground='Red',text='All Field is required')
        return    
    else:
        mydb=mysql.connector.connect(host='localhost',user='root',password='himanshu5050',database='bank')
        data1=(name,password)
        sql1=('insert into register values(%s,%s)')
        x=mydb.cursor()
        x.execute(sql1,data1)
        mydb.commit()
        notif.config(foreground='green',text='You Have Been Successfully Registered')
    cap_img()

def reg():
    global temp_name
    global temp_password
    global notif
    temp_name=StringVar()
    temp_password=StringVar()
    screen=Toplevel(win)
    screen.title('SBI Registeration Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')
    Label(screen,text='Please Enter Your Details below For Registeration',font=('calibri',12)).grid(row=1,sticky=N)
    Label(screen,text='Name',font=('calibri',12)).grid(row=2,sticky=W)
    Label(screen,text='Password',font=('calibri',12)).grid(row=3,sticky=W)    
    Entry(screen,textvariable=temp_name).grid(row=2)
    Entry(screen,textvariable=temp_password,show='*').grid(row=3)
    Button(screen,text='Register',font=('calibri',12),command=finish_reg).grid(row=4)
    notif=Label(screen,font=('Calibri',12))
    notif.grid(row=5)   
def funct():          
    screen=Toplevel(win)
    screen.title('SBI Login Page')
    screen.iconbitmap('sbi.ico')
    screen.geometry('1368x768+0+0')


    button_style = ttk.Style()
    button_style.configure('TButton', font=('calibri', 12), width=30, foreground='black', background='#D9D9D9')

    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()

    # Calculate the x and y position to center the screen
    x_position = int((screen_width - 1368) / 2)
    y_position = int((screen_height - 768) / 2)
    # Set the screen position
    screen.geometry(f'1368x768+{x_position}+{y_position}')
    screen.columnconfigure(0, weight=1)
    
    Button(screen,text='Open Account',font=('calibri',12),width=30,command=openacc).grid(row=3)
    Button(screen,text='Deposit Amount',font=('calibri',12),width=30,command=depamt).grid(row=4)
    Button(screen,text='Withdraw Amount',font=('calibri',12),width=30,command=wtdamt).grid(row=5)
    Button(screen,text='Balance Enquiry',font=('calibri',12),width=30,command=balenq).grid(row=6)
    Button(screen,text='Customer Details',font=('calibri',12),width=30,command=displaydetails).grid(row=7)
    Button(screen,text='Close Account',font=('calibri',12),width=30,command=closeacc).grid(row=8)
    

# Set window title
win.title('Banking Application')

# Set window background color
win.configure(background='#f2f2f2')

# Set custom fonts
title_font = ('Calibri', 20, 'bold')
subtitle_font = ('Calibri', 16)
button_font = ('Calibri', 12)

# Create and grid the labels
Label(win, text='Customer-Client Banking Services', font=title_font, fg='#333333', bg='#f2f2f2').grid(row=0, sticky=N)
Label(win, text='The Most Secure Bank With Face Recognition Feature', font=subtitle_font, fg='#666666', bg='#f2f2f2').grid(row=1, sticky=N)

# Load and resize the image
img = Image.open('Banking.png')
img = img.resize((1550, 600))
img = ImageTk.PhotoImage(img)

# Create and grid the image label
Label(win, image=img).grid(row=2, sticky=N)

# Create and grid the buttons
Button(win, text='Register', font=button_font, width=30, command=reg, bg='#4CAF50', fg='white').grid(row=3, pady=10)
Button(win, text='Login', font=button_font, width=30, command=login, bg='#333333', fg='white').grid(row=4, pady=10)

# Run the window
win.mainloop()


