from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
from PIL import ImageTk, Image

v1, v2 = 'Username', 'PIN'


def create():
    try:
        con = sql.connect("login.db")
        con.execute('''CREATE TABLE IF NOT EXISTS login (
                            username varchar(200) PRIMARY KEY NOT NULL,
                            password varchar(200) NOT NULL,
                            pin int(4) NOT NULL
                            );''')
        con.execute("INSERT INTO login (username, password,pin) VALUES('admin', 'root', 1234);")
        con.commit()
        con.close()
    except sql.IntegrityError:
        print("tables present")

    except:
        print("Errors are the key to success")
    else:
        print("Success")


def db():
    con = sql.connect('login.db')
    return con


def align(win):
    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    x1, y1 = int(h * .9), int(w * .9)
    x = int((h / 2) - (x1 / 2))
    y = int((w / 2) - (y1 / 2))
    win.geometry('{}x{}+{}+{}'.format(y1, x1, y, x - 20))


def hover(button, c1='#343434', x=0):
    if not x:
        button.bind('<Enter>', func=lambda e: button.config(background=c1))
        c = button['background']
        button.bind('<Leave>', func=lambda e: button.config(background=c))
    else:
        button.bind('<Enter>', func=lambda e: button.config(fg=c1))
        c = button['fg']
        button.bind('<Leave>', func=lambda e: button.config(fg=c))


def reset():
    v1, v2 = 'Username', 'PIN'

    def create():
        global v1, v2
        u, p = usr.get(), pwd.get()
        con = db()
        a = con.cursor()
        if v1 == "Username" and v2 == 'PIN':

            a.execute("select * from login where username='" + u + "'")
            r = a.fetchall()
            pss = r[0][2] if r else 0

            if str(pss) == pwd.get():
                v1, v2 = "Enter Password", "Re-Enter Password"
                e1.delete(0, "end")
                e1.config(fg='silver')
                e1.insert(0, v1)
                e1.bind('<FocusIn>',
                        lambda e: (e1.delete(0, "end"), e1.config(fg='black')) if usr.get() == v1 else None)
                e1.bind("<FocusOut>",
                        lambda e: (e1.insert(0, v1), e1.config(fg='silver')) if usr.get() == "" else None)
                e2.delete(0, "end")
                e2.config(fg='silver')
                e2.insert(0, v2)
                e2.bind('<FocusIn>',
                        lambda e: (e2.delete(0, "end"), e2.config(fg='black')) if pwd.get() == v2 else None)
                e2.bind("<FocusOut>",
                        lambda e: (e2.insert(0, v2), e2.config(fg='silver')) if pwd.get() == "" else None)
            else:
                messagebox.showinfo('Wrong', "Pin not Found")

            con.close()
        elif v1 == "Enter Password" and v2 == "Re-Enter Password":
            if usr.get() == pwd.get():
                a.execute("update login set password ='" + p + "' where username='" + u + "'")
                con.commit()
                con.close()
                messagebox.showinfo("Successfully", "Password Changed")
                win.destroy()
                first()
            else:
                messagebox.showerror("Error", "Password doesn't match")

    win = Tk()
    align(win)
    win.resizable(False, False)
    win.overrideredirect(True)
    img = Image.open("icon\\i1.png")
    x, y = int(win.winfo_screenwidth() * .9), int(win.winfo_screenheight() * .9)
    resized = img.resize((x, y))
    load = ImageTk.PhotoImage(resized, Image.ANTIALIAS)

    x = Label(win, image=load, bd=10)
    x.place(x=0, y=0, relheight=1, relwidth=1)

    frame = Frame(win, bg="white")
    frame.pack(pady=150)

    close = Button(frame, font=('Helvetica 9', 12, 'bold'), bg='white', text='X', fg="black", highlightcolor="white",
                   bd=0, command=win.destroy)
    close.grid(row=0, sticky='NE')

    text = Label(frame, text="Reset Password :", font=('Helvetica', 20, 'bold'), fg="Black", bg="White")
    text.grid(row=1, pady=25, ipady=5)

    usr = StringVar()
    e1 = Entry(frame, textvariable=usr, justify='center', font=('Helvetica 9', 12), fg='silver', width=35,
               highlightthickness=1, highlightbackground="silver", highlightcolor="#1976D2")
    e1.insert(0, v1)
    e1.grid(row=2, pady=10, padx=20, ipady=8)
    e1.bind('<FocusIn>',
            lambda e: (e1.delete(0, "end"), e1.config(fg='black')) if usr.get() == v1 else None)
    e1.bind("<FocusOut>",
            lambda e: (e1.insert(0, v1), e1.config(fg='silver')) if usr.get() == "" else None)

    pwd = StringVar()
    e2 = Entry(frame, textvariable=pwd, justify='center', font=('Helvetica 9', 12), fg='silver', width=35,
               highlightthickness=1, highlightbackground="silver", highlightcolor="#1976D2")
    e2.insert(0, v2)
    e2.grid(row=3, pady=10, padx=20, ipady=8)
    e2.bind('<FocusIn>',
            lambda e: (e2.delete(0, "end"), e2.config(fg='black')) if pwd.get() == v2 else None)
    e2.bind("<FocusOut>",
            lambda e: (e2.insert(0, v2), e2.config(fg='silver')) if pwd.get() == "" else None)

    main = Button(frame, text="Back to main", bd=0, font=('Helvetica 9', 8, 'bold'), fg="#2962FF", bg='white',
                  command=lambda: (win.destroy(), first()), width=20)
    main.grid(row=4, pady=5, sticky='E')

    login = Button(frame, text='Submit', font=('Helvetica 9', 12, 'bold'), fg="white", bg="#2196FF",
                   command=create, width=31)
    login.grid(row=5, pady=45, ipady=5)

    hover(close, '#1976D2', 1)
    hover(login, '#1976D2')
    win.mainloop()


def first():
    def login():
        us = user.get()
        ps = passwd.get()

        con = db()
        a = con.cursor()
        a.execute("select * from login where username='" + us + "' and password = '" + ps + "'")
        results = a.fetchall()
        count = len(results)
        print(count)
        if count > 0:
            con.close()
            messagebox.showinfo("Success", "Correct Credentials")
            win.destroy()
            # open_main()
        else:
            messagebox.showinfo("message", "Wrong username or password")

    win = Tk()
    align(win)
    win.title("Login")
    win.configure(bg='gray')
    win.resizable(False, False)
    win.overrideredirect(True)
    # win.wm_attributes("-transparentcolor", 'brown')

    w, h = win.winfo_screenwidth(), win.winfo_screenheight()
    x1, y1 = int(h * .9), int(w * .9)

    img = Image.open('icon\\i1.png')
    resized = img.resize((y1, x1))
    load = ImageTk.PhotoImage(resized, Image.ANTIALIAS)

    x = Label(win, image=load)
    x.place(x=0, y=0, relheight=1, relwidth=1)

    # middle frame
    mframe = Frame(win, bg="white", bd=10)
    mframe.pack(pady=150)

    close = Button(mframe, font=('Helvetica 9', 12, 'bold'), bg='white', text='X', fg="black", highlightcolor="white",
                   bd=0, command=win.destroy)
    close.grid(row=0, sticky='NE')

    text = Label(mframe, text='LOG IN ', font=('Helvetica', 20, 'bold'), fg="Black", bg="White")
    text.grid(row=1, pady=25, ipady=5)

    user = StringVar()
    e1 = Entry(mframe, textvariable=user, justify='center', font=('Helvetica 9', 12), fg='silver', width=35,
               highlightthickness=1, highlightbackground="silver", highlightcolor="#1976D2")
    e1.insert(0, "User Name")
    e1.grid(row=2, pady=10, padx=20, ipady=8)
    e1.bind("<FocusIn>",
            lambda event: (e1.delete(0, "end"),
                           e1.config(fg='black', font=('Helvetica 9', 12))) if user.get() == "User Name" else None)
    e1.bind("<FocusOut>",
            lambda event: (e1.insert(0, "User Name"),
                           e1.config(fg='silver', font=('Helvetica 9 italic', 12))) if user.get() == "" else None)

    passwd = StringVar()
    e2 = Entry(mframe, textvariable=passwd, justify='center', font=('Helvetica 9 italic', 12), fg='silver', width=35,
               highlightthickness=1, highlightbackground="silver", highlightcolor="#1976D2")
    e2.insert(2, "Password")
    e2.grid(row=3, ipady=8, pady=2)
    e2.bind("<FocusIn>",
            lambda e: (e2.delete(0, "end"), e2.config(fg='black', show="*", font=(
                'Helvetica 9', 12))) if passwd.get() == "Password" else None)
    e2.bind("<FocusOut>",
            lambda e: (e2.insert(0, "Password"),
                       e2.config(fg='silver', font=('Helvetica 9 italic', 12))) if passwd.get() == "" else None)

    rst = Button(mframe, text="Reset password", bd=0, font=('Helvetica 9', 8, 'bold'), fg="#2962FF", bg='white',
                 command=lambda: (win.destroy(), reset()), width=20)
    rst.grid(row=4, pady=5, sticky='E')

    log = Button(mframe, text='Log in', font=('Helvetica 9', 12, 'bold'), fg="white", bg="#2196FF", command=login,
                 width=31)
    log.grid(row=5, pady=45, ipady=5)

    hover(log, '#1976D2')
    hover(close, '#1976D2', 1)
    hover(rst, '#19DDD2', 1)

    win.mainloop()


try:
    create()
except:
    pass
else:
    first()
