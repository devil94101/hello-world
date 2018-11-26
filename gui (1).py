from tkinter import *
from tkinter import messagebox
import sqlite3

# ****************************** Database part *******************************

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS Auth(
            Uid TEXT PRIMARY KEY,
            Utype TEXT,
            Name TEXT,
            Course TEXT,
            Email TEXT,
            Passwd TEXT,
            Status TEXT,
            Link TEXT)""")
conn.commit()


# Database Query Function Definations

def cngpass():
    def submit():
        c.execute("UPDATE Auth SET Passwd=? WHERE Uid=?", (entry2.get(), cuserid))
        conn.commit()
        messagebox.showinfo('Confirmation', 'Password changed Successfully!')
        w.destroy()

    w = window('Change Password', '640x380+400+150')
    frame = Frame(w, bd=6, relief='raised')
    frame.pack(side='top', pady=70)

    falselabel = Label(frame, text='This is a false frame.', fg='lightgray')
    falselabel.grid(row=0, column=0)

    lab2 = Label(frame, text='Old Password :', font=('arial', 15))
    lab2.grid(row=1, column=0, sticky='e')
    entry1 = Entry(frame, show='*')
    entry1.grid(row=1, column=1, sticky='w')

    lab3 = Label(frame, text='New Password :', font=('arial', 15))
    lab3.grid(row=2, column=0, sticky='e', pady=20)
    entry2 = Entry(frame)
    entry2.grid(row=2, column=1, sticky='w')

    button = Button(frame, text='Submit', font=('arial', 15), command=submit, width=10, bg='black', fg='lightgray')
    button.grid(row=3, column=0, columnspan=2, padx=160, pady=10)

def getname():
    c.execute("SELECT Name FROM Auth WHERE Uid=?", (cuserid,))
    nm = c.fetchone()
    return nm[0]

def validate(utype, uid, passwd):
    global cuserid
    cuserid = uid
    c.execute("SELECT Passwd FROM Auth WHERE Utype=? AND Uid=?", (utype, uid))
    p = c.fetchone()
    if p is None:
        return 'dexist'
    else:
        if p[0] == passwd:
            return 'valid'
        else:
            return 'invalid'


def add_user(utype, name, uid, course, email, passwd):
    c.execute("INSERT INTO Auth VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (uid, utype, name, course, email, passwd, 'norequest', 'nolink'))
    conn.commit()
    print("Values inserted successfully")

# ************************************** Tkinter part *************************************

# Function Definations


def window(title, geo):
    window1 = Toplevel(root)
    window1.title(title)
    window1.state('normal')
    window1.overrideredirect()
    window1.geometry(geo)
    window1.resizable(False, False)
    window1.iconify()
    window1.configure(background='black', bd=6, relief='sunken')
    return window1


def student():

    def chkstatus():
        greetlab1.pack_forget()
        greetlab2.pack_forget()
        rightframe.pack_forget()
        frame2.pack_forget()
        frame1.pack(side='left', fill='both')


    def req():
        greetlab1.pack_forget()
        greetlab2.pack_forget()
        rightframe.pack_forget()
        frame1.pack_forget()
        frame2.pack(side='left', fill='both')


    def logout():
        k = messagebox.askyesno('Confirmation', 'Are you sure you want to Log Out?')
        if k==True:
            leftframe.destroy()
            rightframe.destroy()
            frame1.destroy()
            frame2.destroy()
        mainframe.pack(side='top', fill='both')

    leftframe = Frame(root, bd=6, relief='raised', bg='black')
    leftframe.pack(side='left', fill='y')

    rightframe = Frame(root, bd=6, relief='sunken')
    rightframe.pack(side='left', fill='both')

    falselab = Label(leftframe, text='false label', bg='black', fg='black', bd=4)
    falselab.pack(pady=26)

    button1 = Button(leftframe, text='Request For Supervisor', command=req,
                     width=20, height=2, bd=4, font=('arial', 13))
    button1.pack(padx=30, pady=20)

    button2 = Button(leftframe, text='Check Status', command=chkstatus, width=20, height=2, bd=4, font=('arial', 13))
    button2.pack(padx=30, pady=20)

    button3 = Button(leftframe, text='Change Password', width=20, height=2, bd=4, command=cngpass, font=('arial', 13))
    button3.pack(padx=30, pady=20)

    button3 = Button(leftframe, text='Log Out', width=20, height=2, bd=4, font=('arial', 13), command=logout)
    button3.pack(padx=30, pady=20)

    greet = 'Hi, ' + str(getname())
    greetlab1 = Label(rightframe, text=greet, font=('arial', 22))
    greetlab1.pack(pady=150)

    greetlab2 = Label(rightframe, text='Please choose an option from left pane.', font=('arial', 12))
    greetlab2.pack(padx=380)

    # ************************** Frame 1 in student for check status *******************************

    frame1 = Frame(root, bd=6, relief='sunken')
    frame1.pack(side='left', fill='both')

    tframe1 = Frame(frame1, bd=6, relief='raised')
    tframe1.pack(side='top', fill=X)

    bframe1 = Frame(frame1, bd=6, relief='raised')
    bframe1.pack(fill='both')

    c.execute("SELECT * FROM Auth WHERE Utype=? AND Link=?", ('Supervisor', cuserid))
    dat = c.fetchone()
    c.execute("SELECT Status FROM Auth WHERE Uid=?", (cuserid,))
    key = c.fetchone()

    falseframe1 = Label(tframe1, text='Hi working', fg='lightgray')
    falseframe1.pack(side='bottom', padx=480)

    wframe1 = Frame(tframe1)
    wframe1.pack(pady=85, side='left', padx=100)

    lab1 = Label(wframe1, text='You are currently under supervision of :', font=('arial', 15))
    lab1.grid(row=0, column=0, pady=50)

    if dat == None:
        lab1.config(text='You have not been allotted any supervisor.')
    else:
        id1 = 'User Id : ' + str(dat[0])
        idlabel1 = Label(wframe1, text=id1, font=('arial', 12))
        idlabel1.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        name1 = 'Name : ' + str(dat[2])
        namelabel1 = Label(wframe1, text=name1, font=('arial', 12))
        namelabel1.grid(row=2, column=0, pady=10, padx=10, sticky='w')

        course1 = 'Course : ' + str(dat[3])
        courselabel1 = Label(wframe1, text=course1, font=('arial', 12))
        courselabel1.grid(row=3, column=0, pady=10, padx=10, sticky='w')

        email1 = 'E-Mail : ' + str(dat[4])
        emaillabel1 = Label(wframe1, text=email1, font=('arial', 12))
        emaillabel1.grid(row=4, column=0, pady=10, padx=10, sticky='w')

    if key[0] == 'accepted':
        stat = 'Status : Accepted'
        label1 = Label(bframe1, text=stat, font=('arial', 15))
        label1.grid(row=5, column=1, sticky='e', pady=30, padx=50)
    elif key[0] == 'pending':
        stat = 'Status : Pending'
        label1 = Label(bframe1, text=stat, font=('arial', 15))
        label1.grid(row=5, column=1, sticky='e', pady=30, padx=50)
    elif key[0] == 'norequest':
        stat = 'Status : No request initiated'
        label1 = Label(bframe1, text=stat, font=('arial', 15))
        label1.grid(row=5, column=1, sticky='e', pady=30, padx=50)
    else:
        stat = 'Status : Rejected'
        label1 = Label(bframe1, text=stat, font=('arial', 15))
        label1.grid(row=5, column=1, sticky='e', pady=30, padx=50)

    frame1.pack_forget()

    # *************************** Frame 2 in student for request ********************************

    frame2 = Frame(root, bd=6, relief='sunken')
    frame2.pack(side='left', fill='both')

    tframe2 = Frame(frame2, bd=6, relief='raised')
    tframe2.pack(side='top', fill=X)

    bframe2 = Frame(frame2, bd=6, relief='raised')
    bframe2.pack(fill='both')

    falselab2 = Label(tframe2, text='false label', fg='lightgray')
    falselab2.grid(row=1, column=0, padx=50)

    label2 = Label(tframe2, text='View Supervisors :', font=('arial', 15))
    label2.grid(row=1, column=1, sticky='e', pady=20, padx=50)

    c.execute("SELECT Name FROM Auth WHERE Utype=?", ('Supervisor',))
    suplist = c.fetchall()
    suplist = list(m[0] for m in suplist)
    sups = StringVar()
    sups.set('Choose a Supervisor')
    menu1 = OptionMenu(tframe2, sups, *suplist)
    menu1.grid(row=1, column=2, sticky='w')


    def view():
        c.execute("SELECT * FROM Auth WHERE Name=?", (sups.get(),))
        l = c.fetchone()
        id = 'User Id : ' + str(l[0])
        idlabel2.config(text=id, fg='black')
        name = 'Name : ' + str(l[2])
        namelabel2.config(text=name, fg='black')
        course = 'Course : ' + str(l[3])
        courselabel2.config(text=course, fg='black')
        email = 'E-Mail : ' + str(l[4])
        emaillabel2.config(text=email, fg='black')
        status = 'Status : Available'
        statuslabel2.config(text=status, fg='black')

    button1 = Button(tframe2, text='View Details', bd=4, font=('arial', 13), command=view)
    button1.grid(row=1, column=3, columnspan=4, sticky='e', padx=70)

    l = Label(bframe2, text='Hi working', fg='lightgray')
    l.pack(side='bottom', padx=480)

    wframe2 = Frame(bframe2)
    wframe2.pack(pady=100)

    def reqsup():
        c.execute("UPDATE Auth SET Status=?, Link=? WHERE Name=? AND Utype=?", ('request', cuserid, sups.get(), 'Supervisor'))
        c.execute("UPDATE Auth SET Status=?, Link=? WHERE Uid=? AND Utype=?", ('pending', sups.get(), cuserid, 'Student'))
        conn.commit()
        messagebox.showinfo('Confirmation', 'Request successfully sent to supervisor!')

    button2 = Button(bframe2, text='Request for Supervisor', height=2, bd=6, font=('arial', 13), command=reqsup)
    button2.pack()

    idlabel2 = Label(wframe2, text='User Id', font=('arial', 12), fg='lightgray')
    idlabel2.grid(row=0, column=0, pady=10, sticky='w')

    namelabel2 = Label(wframe2, text='Name', font=('arial', 12), fg='lightgray')
    namelabel2.grid(row=1, column=0, pady=10, sticky='w')

    courselabel2 = Label(wframe2, text='Course', font=('arial', 12), fg='lightgray')
    courselabel2.grid(row=2, column=0, pady=10, sticky='w')

    emaillabel2 = Label(wframe2, text='E-Mail', font=('arial', 12), fg='lightgray')
    emaillabel2.grid(row=3, column=0, pady=10, sticky='w')

    statuslabel2 = Label(wframe2, text='Status', font=('arial', 12), fg='lightgray')
    statuslabel2.grid(row=4, column=0, pady=10, sticky='w')

    frame2.pack_forget()


def supervisor():
    def select():
        greetlab1.pack_forget()
        greetlab2.pack_forget()
        rightframe.pack_forget()
        frame1.pack_forget()
        frame2.pack(side='left', fill='both')


    def ongp():
        greetlab1.pack_forget()
        greetlab2.pack_forget()
        rightframe.pack_forget()
        frame2.pack_forget()
        frame1.pack(side='left', fill='both')


    def logout():
        k = messagebox.askyesno('Confirmation', 'Are you sure you want to Log Out?')
        if k==True:
            leftframe.destroy()
            rightframe.destroy()
            frame1.destroy()
            frame2.destroy()
        mainframe.pack(side='top', fill='both')

    leftframe = Frame(root, bd=6, relief='raised', bg='black')
    leftframe.pack(side='left', fill='y')

    rightframe = Frame(root, bd=6, relief='sunken')
    rightframe.pack(side='left', fill='both')

    falselab = Label(leftframe, text='false label', bg='black', fg='black', bd=4)
    falselab.pack(pady=26)

    button1 = Button(leftframe, text='Ongoing Projects', command=ongp, width=20, height=2, bd=4, font=('arial', 13))
    button1.pack(padx=30, pady=20)

    button2 = Button(leftframe, text='Select Students', command=select, width=20, height=2, bd=4, font=('arial', 13))
    button2.pack(padx=30, pady=20)

    button3 = Button(leftframe, text='Change Password', width=20, height=2, bd=4, command=cngpass, font=('arial', 13))
    button3.pack(padx=30, pady=20)

    button3 = Button(leftframe, text='Log Out', width=20, height=2, bd=4, font=('arial', 13), command=logout)
    button3.pack(padx=30, pady=20)

    greet = 'Hi, ' + str(getname())
    greetlab1 = Label(rightframe, text=greet, font=('arial', 22))
    greetlab1.pack(pady=150)

    greetlab2 = Label(rightframe, text='Please choose an option from left pane.', font=('arial', 12))
    greetlab2.pack(padx=380)

    # ************************** frame1 for supervisor for ongoing projects module ***********************

    frame1 = Frame(root, bd=6, relief='sunken')
    frame1.pack(side='left', fill='both')

    tframe1 = Frame(frame1, bd=6, relief='raised')
    tframe1.pack(side='top', fill=X)

    bframe1 = Frame(frame1, bd=6, relief='raised')
    bframe1.pack(fill='both')

    c.execute("SELECT * FROM Auth WHERE Status=? AND Link=?", ('accepted', cuserid,))
    dat1 = c.fetchone()

    falselabel1 = Label(tframe1, text='This is a false label', fg='lightgray')
    falselabel1.pack(side='bottom', padx=480)

    wframe1 = Frame(tframe1)
    wframe1.pack(pady=85, side='left', padx=100)

    lab1 = Label(wframe1, text='You are Supervising the following student :', font=('arial', 15))
    lab1.grid(row=0, column=0, pady=50)

    if dat1 == None:
        lab1.config(text='You have no ongoing projects.')
    else:
        id1 = 'User Id : ' + str(dat1[0])
        idlabel1 = Label(wframe1, text=id1, font=('arial', 12))
        idlabel1.grid(row=1, column=0, pady=10, padx=10, sticky='w')

        name1 = 'Name : ' + str(dat1[2])
        namelabel1 = Label(wframe1, text=name1, font=('arial', 12))
        namelabel1.grid(row=2, column=0, pady=10, padx=10, sticky='w')

        course1 = 'Course : ' + str(dat1[3])
        courselabel1 = Label(wframe1, text=course1, font=('arial', 12))
        courselabel1.grid(row=3, column=0, pady=10, padx=10, sticky='w')

        email1 = 'E-Mail : ' + str(dat1[5])
        emaillabel1 = Label(wframe1, text=email1, font=('arial', 12))
        emaillabel1.grid(row=4, column=0, pady=10, padx=10, sticky='w')

    label1 = Label(bframe1, text='Ongoing Project : Capstone Managment', font=('arial', 15))
    label1.grid(row=5, column=1, sticky='e', pady=30, padx=50)

    if dat1 == None:
        label1.config(text='Ongoing Project : None')

    frame1.pack_forget()

    # ************************ frame2 for select student module in supervisor **********************

    frame2 = Frame(root, bd=6, relief='sunken')
    frame2.pack(side='left', fill='both')

    tframe2 = Frame(frame2, bd=6, relief='raised')
    tframe2.pack(side='top', fill=X)

    bframe2 = Frame(frame2, bd=6, relief='raised')
    bframe2.pack(fill='both')

    falselab2 = Label(tframe2, text='false label', fg='lightgray')
    falselab2.grid(row=1, column=0, padx=50)

    label2 = Label(tframe2, text='View Requests :', font=('arial', 15))
    label2.grid(row=1, column=1, sticky='e', pady=20, padx=50)

    c.execute("SELECT Name FROM Auth WHERE Utype=?", ('Student',))
    suplist = c.fetchall()
    suplist = list(m[0] for m in suplist)
    sups = StringVar()
    sups.set('Choose a Student')
    menu2 = OptionMenu(tframe2, sups, *suplist)
    menu2.grid(row=1, column=2, sticky='w')

    def view():
        c.execute("SELECT * FROM Auth WHERE Name=?", (sups.get(),))
        l = c.fetchone()
        id = 'User Id : ' + str(l[0])
        idlabel2.config(text=id, fg='black')
        name = 'Name : ' + str(l[2])
        namelabel2.config(text=name, fg='black')
        course = 'Course : ' + str(l[3])
        courselabel2.config(text=course, fg='black')
        email = 'Email : ' + str(l[4])
        emaillabel2.config(text=email, fg='black')

    button1 = Button(tframe2, text='View Details', bd=4, font=('arial', 13), command=view)
    button1.grid(row=1, column=3, columnspan=4, sticky='e', padx=70)

    l2 = Label(bframe2, text='Hi working', fg='lightgray')
    l2.pack(side='bottom', padx=480)

    wframe2 = Frame(bframe2)
    wframe2.pack(pady=130)

    def sel():
        c.execute("UPDATE Auth SET Status=?, Link=? WHERE Name=?",('accepted', cuserid, sups.get()))
        conn.commit()
        messagebox.showinfo('Confirmation', 'Student selected successfully!')

    def rej():
        c.execute("UPDATE Auth SET Status=?, Link=? WHERE Name=?", ('norequest', 'nolink', sups.get()))
        c.execute("UPDATE Auth SET Status=?, Link=? WHERE Uid=?", ('norequest', 'nolink', cuserid))
        messagebox.showinfo('Confirmation', 'Request Rejected!')
        conn.commit()


    button2 = Button(bframe2, text='Select Student', height=2, bd=6, font=('arial', 13), command=sel)
    button2.pack(side='left', padx=220)

    button3 = Button(bframe2, text='Reject Student', height=2, bd=6, font=('arial', 13), command=rej)
    button3.pack(side='left', padx=50)

    idlabel2 = Label(wframe2, text='id', font=('arial', 12), fg='lightgray')
    idlabel2.grid(row=0, column=0, pady=10, sticky='w')

    namelabel2 = Label(wframe2, text='Name', font=('arial', 12), fg='lightgray')
    namelabel2.grid(row=1, column=0, pady=10, sticky='w')

    courselabel2 = Label(wframe2, text='course', font=('arial', 12), fg='lightgray')
    courselabel2.grid(row=2, column=0, pady=10, sticky='w')

    emaillabel2 = Label(wframe2, text='email', font=('arial', 12), fg='lightgray')
    emaillabel2.grid(row=3, column=0, pady=10, sticky='w')

    frame2.pack_forget()


def login():
    def submit():
        status = validate(usertype.get(), entry1.get(), entry2.get())
        if status == 'valid':
            win.destroy()
            mainframe.pack_forget()
            if usertype.get() == 'Student':
                student()
            else:
                supervisor()
        elif status == 'dexist':
            messagebox.showwarning('Warning!', 'Username does not exists.')
        else:
            messagebox.showwarning('Warning!', 'Invalid Credentials')

    win = window('Login Form', '800x500+285+160')
    topframe = Frame(win, bd=6, relief='raised')
    topframe.pack(side='top', pady=50)
    botframe = Frame(win, bd=6, relief='raised')
    botframe.pack(side='top')

    lab = Label(topframe, text='LOGIN', font=('arial', 22))
    lab.pack(padx=220, pady=10)

    lab1 = Label(botframe, text='User Type :', font=('arial', 15))
    lab1.grid(row=0, column=0, pady=20, sticky='e')

    usertype = StringVar()
    usertype.set('Choose User')
    dm = OptionMenu(botframe, usertype, 'Student', 'Supervisor')
    dm.grid(row=0, column=1, sticky='w')

    lab2 = Label(botframe, text='ID Number :', font=('arial', 15))
    lab2.grid(row=1, column=0, sticky='e')
    entry1 = Entry(botframe)
    entry1.grid(row=1, column=1, sticky='w')

    lab3 = Label(botframe, text='Password :', font=('arial', 15))
    lab3.grid(row=2, column=0, sticky='e', pady=20)
    entry2 = Entry(botframe, show='*')
    entry2.grid(row=2, column=1, sticky='w')

    button = Button(botframe, text='Submit', font=('arial', 15), command=submit, width=10, bg='black', fg='lightgray')
    button.grid(row=3, column=0, columnspan=2, padx=160, pady=10)


def newuser():

    win = window('New User Form', '800x600+285+90')

    def submit():
        add_user(usertype.get(), entry1.get(), entry2.get(), course.get(), entry3.get(), entry4.get())
        messagebox.showinfo('Confirmation', 'User Created Successfully !')
        win.destroy()

    topframe = Frame(win, bd=6, relief='raised')
    topframe.pack(side='top', pady=50)
    botframe = Frame(win, bd=6, relief='raised')
    botframe.pack(side='top')

    lab = Label(topframe, text='NEW USER', font=('arial', 22))
    lab.pack(padx=180, pady=10)

    lab1 = Label(botframe, text='User Type :', font=('arial', 15))
    lab1.grid(row=0, column=0, pady=10, sticky='e')

    usertype = StringVar()
    usertype.set('Choose User')
    dm = OptionMenu(botframe, usertype, 'Student', 'Supervisor')
    dm.grid(row=0, column=1, sticky='w')

    lab2 = Label(botframe, text='Full Name :', font=('arial', 15))
    lab2.grid(row=1, column=0, sticky='e', pady=10)
    entry1 = Entry(botframe)
    entry1.grid(row=1, column=1, sticky='w')

    lab3 = Label(botframe, text='ID No. :', font=('arial', 15))
    lab3.grid(row=2, column=0, sticky='e', pady=10)
    entry2 = Entry(botframe)
    entry2.grid(row=2, column=1, sticky='w')

    lab4 = Label(botframe, text='Course :', font=('arial', 15))
    lab4.grid(row=3, column=0, sticky='e', pady=10)

    course = StringVar()
    course.set('Choose Course')
    dm = OptionMenu(botframe, course, 'CSE', 'ME', 'ECE', 'IT', 'EEE')
    dm.grid(row=3, column=1, sticky='w')

    lab5 = Label(botframe, text='Email :', font=('arial', 15))
    lab5.grid(row=4, column=0, sticky='e', pady=10)
    entry3 = Entry(botframe)
    entry3.grid(row=4, column=1, sticky='w')

    lab6 = Label(botframe, text='Choose Password :', font=('arial', 15))
    lab6.grid(row=5, column=0, sticky='e', pady=10)
    entry4 = Entry(botframe)
    entry4.grid(row=5, column=1, sticky='w')

    button = Button(botframe, text='Submit', font=('arial', 15), command=submit, width=10, bg='black', fg='lightgray')
    button.grid(row=6, column=0, columnspan=2, padx=160, pady=20)


# Initialize [root] and geometry configurations.

root = Tk()
root.title('Capstone Registration')
root.overrideredirect()
root.geometry('{0}x{1}+0+0'.format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.iconify()

# headFrame is the frame common to all pages and is used for head labels.

headFrame = Frame(root, bd=6, relief='raised')
headFrame.pack(side='top', fill='both')

headLabel = Label(headFrame, text='LPU Capstone Project Assignment Portal', font=('arial', 25))
headLabel.pack(pady=25)

# mainFrame is the frame in very first page used for various widgets.

mainframe = Frame(root, bd=6, bg='black', relief='raised')
mainframe.pack(side='top', fill='both')

innerframe = Frame(mainframe, bd=8, relief='sunken')
innerframe.pack(pady=150)

login_button = Button(innerframe, height=2, width=20, bg='black', fg='white', text='LOGIN',
                      command=login,font=('arial', 18), bd=6, relief='raised')
login_button.pack(padx=70, pady=100, side=LEFT)

newuser_button = Button(innerframe, height=2, width=20, bg='black', fg='white', text='NEW USER',
                        command=newuser, font=('arial', 18), bd=6, relief='raised')
newuser_button.pack(padx=70, pady=100, side=LEFT)

root.mainloop()
conn.close()

