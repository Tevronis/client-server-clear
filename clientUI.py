import json
from Tkinter import *

from twisted.internet import tksupport, reactor

from utils import clientUser, comands


class ClientUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI(parent)

    def initUI(self, root):
        #root = Tk()
        root.geometry('300x100')
        root.title('Login or Registration')

        Label(root, text='Login: ').grid(row=0)
        Label(root, text='Password: ').grid(row=1)

        reg = Button(root, text='Registration')
        login = Entry(root)
        password = Entry(root)
        login.grid(row=0, column=1)
        password.grid(row=1, column=1)
        reg.grid(row=2, column=1)

        def acceptExit(event):
            # check log/pass
            cmd = {"command": "VERIFICATION", "login": login.get(), "password": password.get()}
            comands.append(json.dumps(cmd))
            clientUser.login = login.get()
            clientUser.password = password.get()
            # clientUser.user = .get()
            root.destroy()

        def registrationCB(event):
            reg = Tk()
            reg.geometry('300x100')
            reg.title('Registration')
            Label(reg, text='Login: ').grid(row=1)
            Label(reg, text='Password: ').grid(row=2)
            Label(reg, text='Name: ').grid(row=0)
            loginR = Entry(reg)
            passwordR = Entry(reg)
            name = Entry(reg)
            loginR.grid(row=1, column=1)
            passwordR.grid(row=2, column=1)
            name.grid(row=0, column=1)
            def acceptReg(event):
                cmd = {"command": "REGISTRATION", "login": login.get(), "password": password.get(), "name": name.get()}
                comands.append(json.dumps(cmd))
                reg.destroy()
            passwordR.bind('<Return>', acceptReg)
            loginR.focus_set()
            reg.mainloop()

        password.bind('<Return>', acceptExit)
        login.bind('<Return>', acceptExit)
        reg.bind("<Button-1>", registrationCB)

        login.focus_set()
        root.mainloop()

def readMessage(msg):
    top = Toplevel()
    top.title("Message")

    msg = Message(top, text=msg)
    msg.pack()

    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()



