# -*- coding:utf-8 -*-
import hashlib
import json

from tkinter import *
from twisted.internet import reactor, tksupport
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

import mail
import ui.listbox
from clientUI import ClientUI
from mail import Mail
from user import User
from utils import comands, LocalJSON

reload(sys)
sys.setdefaultencoding('utf-8')




def setText(message):
    text = 'FROM: ' + message['from'] + ' Title: ' + message['header']
    listbox.addElement(text, message)


LAST_HASH = ''


class Client(LineOnlyReceiver):
    def sendMessage(self, msg):
        self.sendLine("%s\n" % msg)

    def sendData(self, data):
        if data:
            self.sendMessage(data)
        else:
            self.transport.loseConnection()

    def dataReceived(self, data):
        global LAST_HASH
        js = json.loads(data)
        command = js['command']
        if command == 'SENT':
            listbox.clear()
            for item in js['mails']:
                setText(item)
        if command == 'INBOX':
            listbox.clear()
            for item in js['mails']:
                setText(item)
        if command == 'GINBOX':
            listbox.clear()
            for item in js['mails']:
                setText(item)
        if command == 'MESSAGE':
            LAST_HASH = js['HASH']
            print LAST_HASH

            m = hashlib.md5()
            m.update(js['MESSAGE'])
            print m.hexdigest()
            if m.hexdigest() != LAST_HASH:
                print 'BAD HASH'
            j = json.loads(js['MESSAGE'])
            ClientUI.readMessage(j)
        if command == 'PRINT':
            print js['data']
        if command == 'USER':
            if js['status'] == "OK":
                currentUser.setParams(js)
                tk.title('Client ' + currentUser.login)
            else:
                # TODO repeat log pass
                raise Exception("Неверный логин или пароль")
        if command == "REGISTRATION":
            # TODO save s_key local
            s_key, o_key = currentUser.generateRsaKeys()
            self.sendData(json.dumps({"command": "SETOPENKEY", "open_key": o_key, "login": currentUser.login}))
        print data

    def connectionMade(self):
        print 'Connect good'
        for cmd in comands:
            self.sendData(cmd)

        reload(sys)
        sys.setdefaultencoding('utf-8')

        def sendMAIL(event):
            def send(event):
                js = {'id': mail.nextId(), 'from': currentUser.login, 'header': title.get(),
                      'recivers': to.get().split(),
                      'data': msg.get("1.0", END), 'date': ''}
                toSent = LocalJSON.addCommand(js, 'SETMESSAGE')
                self.sendData(toSent)
                top.destroy()

            top = Toplevel()
            top.title("Message")

            button = Button(top, text="Dismiss")
            msg = Text(top)
            to = Entry(top)
            title = Entry(top)
            Label(top, text='To: ').grid(row=2, column=1)
            Label(top, text='Title: ').grid(row=3, column=1)

            msg.grid(row=1, column=2)
            to.grid(row=2, column=0)
            title.grid(row=3, column=0)
            button.grid(row=4, column=0)
            button.bind("<Button-1>", send)

        def getSentJSON(event):
            js = {"login": currentUser.login}
            toSent = LocalJSON.addCommand(js, 'GETSENT')
            self.sendData(toSent)

        def getInboxJSON(event):
            js = {"login": currentUser.login}
            toSent = LocalJSON.addCommand(js, 'GETINBOX')
            self.sendData(toSent)

        def getMessage(event):
            mail_object = listbox.getCurrent()
            js = {"idMail": mail_object['id']}
            toSent = LocalJSON.addCommand(js, 'GETMESSAGE')
            self.sendData(toSent)

        def delMessage(event):
            mail_object = listbox.getCurrent()
            js = {"login": currentUser.login, "idMail": mail_object['id']}
            toSent = LocalJSON.addCommand(js, 'DELMESSAGE')
            self.sendData(toSent)

        toWriteButton.bind("<Button-1>", sendMAIL)
        sentButton.bind("<Button-1>", getSentJSON)
        inBoxButton.bind("<Button-1>", getInboxJSON)
        readMessageButton.bind("<Button-1>", getMessage)
        delMessageButton.bind("<Button-1>", delMessage)


class Twist_Factory(ClientFactory):
    protocol = Client

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()


root = Tk()
currentUser = User()
UI = ClientUI(root)
root.mainloop()

tk = Tk()
panelFrame = Frame(tk, height=40, bg='gray')
logFrame = Frame(tk, height=340, width=400)

panelFrame.pack(side='top', fill='x')
logFrame.pack(side='bottom', fill='both', expand=1)
# Buttons:
inBoxButton = Button(panelFrame, text='Inbox')
sentButton = Button(panelFrame, text='Sent')
toWriteButton = Button(panelFrame, text='Write')

delMessageButton = Button(panelFrame, text='delete msg')
readMessageButton = Button(panelFrame, text='read msg')

# del this
tk.title('Client ' + currentUser.login)
tk.geometry('400x200')

listbox = ui.listbox.CS_Listbox(logFrame)

# Grid

inBoxButton.grid(row=1, column=1)
sentButton.grid(row=1, column=2)
toWriteButton.grid(row=1, column=3)
delMessageButton.grid(row=1, column=4)
readMessageButton.grid(row=1, column=5)

factory = Twist_Factory()
reactor.connectTCP("localhost", 12345, factory)

tksupport.install(tk)

reactor.run()
