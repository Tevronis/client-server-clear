import json
from Tkinter import *

from utils import comands


class ClientUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI(parent)

    def initUI(self, root):
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
            cmd = {"command": "VERIFICATION", "login": login.get(), "password": password.get()}
            comands.append(json.dumps(cmd))
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
                cmd = {"command": "REGISTRATION", "login": loginR.get(), "password": passwordR.get(), "name": name.get()}
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

    @staticmethod
    def readMessage(js):
        frame = Toplevel()
        frame.geometry('300x200+300+200')
        frame.resizable(False, False)

        topFrame = Frame(frame, height=60, bg='gray')
        botFrame = Frame(frame, height=140, width=200)
        topFrame.pack(side='top', fill='x')
        botFrame.pack(side='bottom', fill='both', expand=1)
        frame.title("Message")

        text = 'FROM: ' + js['from'] + '\nHEADER: ' + js['header'] + '\nDATE: ' + js['date'] + '\nTO: ' + ' '.join(js['recivers'])
        tp = Message(topFrame, text=text, bg='gray')
        tp.pack()
        text = js['data']
        bt = Message(botFrame, text=text)
        bt.pack()

        button = Button(botFrame, text="Dismiss", command=frame.destroy)
        button.pack()



