from tkinter import *
# import tkinter as tk
from datetime import time, date
from tkinter.ttk import Label
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas



def iexit():
    result=messagebox.askyesno('Confirm','Exit?')
    if result:
        root.destroy()
    else:
        pass
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist = []
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)
        table=pandas.DataFrame(newlist,columns=['ID','Name','Phone','Email','Gender','Course','Added Date','Added Time'])
        table.to_csv(url,index=False)
        messagebox.showinfo('Success','Data Saved')


def toplevel_data(title, button_text, command):
    global idEntry, nameEntry, phoneEntry, emailEntry, genderEntry, courseEntry, screen
    screen = Toplevel()
    screen.grab_set()
    screen.title(title)
    screen.resizable(False, False)
    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=20, pady=10, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, padx=10, pady=15)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=20, pady=10, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, padx=10, pady=15)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=20, pady=10, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, padx=10, pady=15)

    emailLabel = Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=20, pady=10, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, padx=10, pady=15)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=4, column=0, padx=20, pady=10, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=4, column=1, padx=10, pady=15)

    courseLabel = Label(screen, text='Course', font=('times new roman', 20, 'bold'))
    courseLabel.grid(row=5, column=0, padx=20, pady=10, sticky=W)
    courseEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    courseEntry.grid(row=5, column=1, padx=10, pady=15)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=6, column=1, pady=10)

    if title=='Update Student':

        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        phoneEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        genderEntry.insert(0, listdata[4])
        courseEntry.insert(0, listdata[5])


def update_data():
    query = 'update student set name=%s,phone=%s,email=%s,gender=%s,course=%s,date=%s,time=%s where ' \
            'id=%s'
    mycursor.execute(query, (
        nameEntry.get(), phoneEntry.get(), emailEntry.get(), genderEntry.get(), courseEntry.get(), currentdate,
        currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id{idEntry.get()} updated successfully', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'deleted{content_id}successfully')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    query = 'select *from student where Id=%s or name=%s or gender=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), genderEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if idEntry.get() == '' or nameEntry.get == '' or phoneEntry.get() == '' or emailEntry.get() == '' or genderEntry.get() == '' or courseEntry.get() == '':
        messagebox.showerror('Error', 'All Fields are required', parent=screen)

    else:
        currentdate = time.strftime('%d/%m/%Y')
        currenttime = time.strftime('%H:%M:%S')
    try:
        query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(query, (
            idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), genderEntry.get(),
            courseEntry.get(), currentdate, currenttime))
        con.commit()
        result = messagebox.askyesno('Data added successfully.Clear form?')
        if result:
            idEntry.delete(0, END)
            nameEntry.delete(0, END)
            phoneEntry.delete(0, END)
            emailEntry.delete(0, END)
            genderEntry.delete(0, END)
            courseEntry.delete(0, END)
        else:
            pass
    except:
        messagebox.showerror('Error' 'Id Already exist', parent=screen)
        return
    query = 'select *from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='19971686')
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Database Connection is successful', parent=connectwindow)
            connectwindow.destroy()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectwindow)
            return
        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key, name varchar(30),phone varchar(10),' \
                    'email varchar(30),' \
                    'gender varchar(20),course varchar(20),date varchar(50), time varchar(50))'
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)

            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)
            exportstudentButton.config(state=NORMAL)
            showstudentcourseButton.config(state=NORMAL)
            exitButton.config(state=NORMAL)

    connectwindow = Toplevel()
    connectwindow.geometry('470x250+730+230')
    connectwindow.title('Database Connection')
    connectwindow.resizable(0, 0)

    hostnameLabel = Label(connectwindow, text='HostName', font=('calibri', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectwindow, font=('roman', 15, 'bold'))
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectwindow, text='UserName', font=('calibri', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectwindow, font=('roman', 15, 'bold'))
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectwindow, text='Password', font=('calibri', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectwindow, font=('roman', 15, 'bold'))
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    ConnectButton = ttk.Button(connectwindow, text='Connect', command=connect)
    ConnectButton.grid(row=3, columnspan=2)


currentdate = None
def clock():
    global currentdate, currenttime
    currentdate = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')






root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root.geometry('1174x680+0+0')
root.title('Student Management System')

label = Label(root, text='Student Management System', font=('helvetica', 14))
label.pack(ipadx=10, ipady=10)

connectButton = ttk.Button(root, text='Connect Database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)
logo_image = PhotoImage(file='education (1).png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student', 'Add', command=add_data))
addstudentButton.grid(row=1, column=0, pady=15)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'Search', command=search_data))
searchstudentButton.grid(row=2, column=0, pady=15)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=15)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'Update', command=update_data))
updatestudentButton.grid(row=4, column=0, pady=15)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=15)

showstudentcourseButton = ttk.Button(leftFrame, text='courses', width=25, state=DISABLED)
showstudentcourseButton.grid(row=6, column=0, pady=15)

exportstudentButton = ttk.Button(leftFrame, text='Export data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=7, column=0, pady=15)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, state=DISABLED,command=iexit)
exitButton.grid(row=8, column=0, pady=15)

rightFrame = Frame(root)
rightFrame.place(x=300, y=70, width=820, height=550)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Phone', 'Email', 'Gender', 'Course',
                                                 'Added Date', 'Added Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)
studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=300, anchor=CENTER)
studentTable.column('Phone', width=200, anchor=CENTER)
studentTable.column('Email', width=400, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('Course', width=200, anchor=CENTER)
studentTable.column('Added Date', width=100, anchor=CENTER)
studentTable.column('Added Time', width=100, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('calibri', 12, 'bold'), background='white', fieldbackground='white')
style.configure('Treeview.Heading', font=('calibri', 12, 'bold'))
studentTable.config(show='headings')

studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Phone', text='Phone')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('Course', text='Course')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('Id', width=50, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Email', width=300, anchor=CENTER)
studentTable.column('Phone', width=200, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('Course', width=300, anchor=CENTER)
studentTable.column('Added Date', width=200, anchor=CENTER)
studentTable.column('Added Time', width=200, anchor=CENTER)

root.mainloop()
