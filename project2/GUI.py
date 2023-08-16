from tkinter import *
import random
import csv

from tkinter.ttk import Treeview
from tkinter import messagebox as mess
import cv2,os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import tkinter.simpledialog as tsd
import time

#function
#ham tao duong dan luu thong tin
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
#thong tin thoi gian
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)
#kiem tra duong dan co ton tai k
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        root.destroy()

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Không có mật khẩu', 'Vui lòng nhập mật khẩu mới', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

###################################################################################

def change_pass():
    global master
    master = Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")
    lbl4 = Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = Label(master, text='   Nhập mật khẩu', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = Label(master, text='Xác nhận mật khẩu', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

#save profile
def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Đặt mật khẩu', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Thành công', message='Đặt mật khẩu thành công')
            return
    password = tsd.askstring('Mật khẩu', 'Vui lòng nhập mật khẩu', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Sai mật khẩu', message='Bạn nhập sai vui lòng nhập lại')
#clear
def clear():
    txt.delete(0, 'end')
    res = "1)Lấy ảnh  >>>  2)Lưu thông tin"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Lấy ảnh  >>>  2)Lưu thông tin"
    message1.configure(text=res)
#lay khuon mat tu camera
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # tạo biến đếm ảnh
                sampleNum = sampleNum + 1

                #Lưu ảnh huấn luyện khuôn mặt đã chụp được vào folder tên TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # hiển thị khung hình
                cv2.imshow('Dang lay anh khuon mat', img)
            # chờ 100s
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # thoát nếu biến đếm chụp ảnh hơn 100 ảnh
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Ảnh khuôn mặt cho mã số : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Vui lòng nhập thông tin"
            message.configure(text=res)
#train face
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Lưu thông tin thành công"
    message1.configure(text=res)
    message.configure(text='Số lượng khuôn mặt hiện có  : ' + str(ID[0]))
#lay nhan
def getImagesAndLabels(path):

    #lấy đường dẫn cho tất cả file trong folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []

    #lặp tất cả các ảnh trong đường dẫn và load mã ID và ảnh
    for imagePath in imagePaths:
        # load ảnh và chuyển sang trắng đen
        pilImage = Image.open(imagePath).convert('L')
        # chuyển đổi ảnh sang dạng numpy array
        imageNp = np.array(pilImage, 'uint8')
        # lấy ID từ ảnh
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # trích xuât khuôn mặt từ dữ liệu huấn luyện
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids
#quet khuon mat nhan dang
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Thiếu dữ liệu', message='Vui lòng nhập Lưu thông tin để lấy khuôn mặt!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        #mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        root.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Dang nhan dang khuon mat', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
#user stuft
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }
######GUI#######
root=Tk()
root.title("Nhan dien khuon mat")
root.geometry('1000x860')
#icon
root.iconbitmap('C:\\Users\\buidu\\OneDrive\\Máy tính\\code2\\aconda\\face_test\\icon_img\\OIP.ico')
root.resizable(False,False)
#background
#Add image file

bg=PhotoImage(file='C:\\Users\\buidu\\OneDrive\\Máy tính\\code2\\aconda\\face_test\\icon_img\\OIP.png')
label1 = Label(root, image = bg)
label1.place(x = 0,y = 0)
#thanh tieu de
colors=['red','green','blue','yellow','pink','red2','gold2','gray','brown']
def introcolor():
    fg= random.choice(colors)
    sliderLaber.config(fg=fg)
    sliderLaber.after(20,introcolor)
def IntroLabelTick():
    global count,text
    if(count>=len(aa)):
        count =-1
        text=''
        sliderLaber.config(text=text)
    else:
        text = text + aa[count]
        sliderLaber.config(text=text)
        count +=1
    sliderLaber.after(100,IntroLabelTick)

aa=' PHẦN MỀM NHẬN DIỆN KHUÔN MẶT!! '
count =0
text =''
sliderLaber = Label(root,text=aa,font=('Arial',25,'italic bold'))
sliderLaber.pack(side=TOP)
IntroLabelTick()
introcolor()
#cua so nhan dang khuon mat
#khuon mat moi

frame1 = Frame(root, bg="#40FF19")

frame1.place(relx=0.01, rely=0.17, relwidth=0.52, relheight=0.60)
imgFrame=ImageTk.PhotoImage(Image.open(r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\icon31.png'))
frame2 = Frame(root, bg="#00aeff")
frame2.place(relx=0.53, rely=0.17, relwidth=0.52, relheight=0.60)

frame3 = Frame(root, bg="#809545")
frame3.place(relx=0.20, rely=0.09, relwidth=0.25, relheight=0.07)

frame4 = Frame(root, bg="#c4c6ce")
frame4.place(relx=0.50, rely=0.09, relwidth=0.30, relheight=0.07)

datef = Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

clock = Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = Label(frame2, text="Nhập thông tin khuôn mặt mới", fg="black",bg="#CE2626" ,font=('times', 17, ' bold ') )
head2.place(x=100,y=0.2)

head1 = Label(frame1, text="Khuôn mặt đã tồn tại", fg="black",bg="#CE2626" ,font=('times', 17, ' bold ') )
head1.place(x=150,y=0.2)

lbl = Label(frame2, text="Nhập ID",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold ') )
lbl.place(x=30, y=55)

txt = Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=20, y=88)

lbl2 = Label(frame2, text="Nhập Tên",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold '))
lbl2.place(x=30, y=140)

txt2 = Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=20, y=173)

message1 = Label(frame2, text="       1)Lấy hình ảnh\n     2)Lưu thông tin" ,bg="#00aeff" ,fg="black"  ,width=39 ,height=5, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=200)

message = Label(frame2, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

imglb=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\iconLB.png')
lblimg1=Label(root,image=imglb,width=100,height=108)
lblimg1.place(x=50,y=35)

imglb2=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\R.png')
lblimg2=Label(root,image=imglb2)
lblimg2.place(x=850,y=35)

imglb3=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\takeFace.png')
lblimg3=Label(root,image=imglb3,width=40,height=34)
lblimg3.place(x=50,y=195)

lbl3 = Label(frame1, text="Thông tin khuôn mặt",width=20  ,fg="black"  ,bg="#00aeff"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Số lượng khuôn mặt hiên có  : '+str(res))

#TREEVIEW

tv= Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

#SCROLLBAR

scroll=Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)
#button
clearButton = Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=355, y=86)
clearButton2 = Button(frame2, text="Clear" , command=clear2,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=355, y=172)
takepic1=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\takepic.png')
takeImgIcon=Label(root,image=takepic1,width=40,height=34)
takeImgIcon.place(x=550,y=448)
takeImg = Button(frame2, text="Lấy ảnh"  ,command=TakeImages,fg="white"  ,bg="blue"  ,width=25  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=65, y=300)
saveinfpic=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\saveinf.png')
saveimgIcon=Label(root,image=saveinfpic,width=40,height=40)
saveimgIcon.place(x=550,y=522)
trainImg = Button(frame2, text="Lưu thông tin" ,command=psw,fg="white"  ,bg="blue"  ,width=25  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=65, y=380)


trackImg = Button(frame1, text="Lấy thông tin khuôn mặt", command=TrackImages ,fg="black"  ,bg="yellow"  ,width=25  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=100,y=50)
Exitpic=PhotoImage(file=r'C:\Users\buidu\OneDrive\Máy tính\code2\aconda\face_test\icon_img\exit.png')
ExitimgIcon=Label(root,image=Exitpic,width=40,height=40)
ExitimgIcon.place(x=420,y=595)
quitWindow = Button(frame1, text="Thoát chương trình", command=root.destroy,fg="black"  ,bg="red"  ,width=30 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)



root.mainloop()
