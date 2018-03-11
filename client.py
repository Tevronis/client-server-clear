# -*- coding:utf-8 -*-
import json

from tkinter import *
from twisted.internet import reactor, tksupport
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

import mail
from mail import Mail
from group import Group
import hashlib
from user import ClientUser
from clientUI import ClientUI, readMessage
from utils import comands, clientUser, LocalJSON

reload(sys)
sys.setdefaultencoding('utf-8')


def setText(message):
    listbox.insert(END, message + '\n')
    text.set('')


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
            listbox.delete(0, listbox.size())
            for item in js['mails']:
                setText('id: ' + str(item['id']) + ' FROM: ' + item['from'] + ' Title: ' + item['header'])
        if command == 'INBOX':
            listbox.delete(0, listbox.size())
            for item in js['mails']:
                setText('id: ' + str(item['id']) + ' FROM: ' + item['from'] + ' Title: ' + item['header'])
        if command == 'GINBOX':
            listbox.delete(0, listbox.size())
            for item in js['mails']:
                setText('id: ' + str(item['id']) + ' FROM: ' + item['from'] + ' Title: ' + item['header'])
        if command == 'MESSAGE':
            LAST_HASH = js['HASH']
            print LAST_HASH

            m = hashlib.md5()
            m.update(js['MESSAGE'])
            print m.hexdigest()
            if m.hexdigest() != LAST_HASH:
                print 'BAD HASH'
            j = json.loads(js['MESSAGE'])
            readMessage(Mail.mailPrint(j))
        if command == 'PRINT':
            print js['data']
        print data

    def connectionMade(self):
        print 'Connect good'
        for cmd in comands:
            self.sendData(cmd)

        reload(sys)
        sys.setdefaultencoding('utf-8')

        def sendMAIL(event):
            def send(event):
                js = {'id': mail.nextId(), 'from': clientUser.login, 'header': title.get(),
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
            js = {"login": clientUser.login}
            toSent = LocalJSON.addCommand(js, 'GETSENT')
            self.sendData(toSent)

        def getInboxJSON(event):
            js = {"login": clientUser.login}
            toSent = LocalJSON.addCommand(js, 'GETINBOX')
            self.sendData(toSent)

        def getMessage(event):
            pat = r'id: ([0-9]+)'
            id = re.search(pat, listbox.get(listbox.curselection()))
            js = {"idMail": str(id.group(1))}
            toSent = LocalJSON.addCommand(js, 'GETMESSAGE')
            self.sendData(toSent)

        def delMessage(event):
            js = {"login": clientUser.login, "idMail": listbox.get(listbox.curselection())}
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

UI = ClientUI(root)
root.mainloop()

# UI.runLogin()
# exit()

tk = Tk()
panelFrame = Frame(tk, height=60, bg='gray')
logFrame = Frame(tk, height=340, width=600)
bottomFrame = Frame(tk, height=60, bg='gray')

panelFrame.pack(side='top', fill='x')
logFrame.pack(side='bottom', fill='both', expand=1)
bottomFrame.pack(side='bottom', fill='both', expand=1)
# Buttons:
inBoxButton = Button(panelFrame, text='Inbox')
sentButton = Button(panelFrame, text='Sent')
toWriteButton = Button(panelFrame, text='Write')

delMessageButton = Button(bottomFrame, text='delete msg')
readMessageButton = Button(bottomFrame, text='read msg')

tk.title('Client ' + clientUser.login)
tk.geometry('500x500')

text = StringVar()
text.set('')

listbox = Listbox(logFrame)
listbox.pack(fill='x', expand='true')
listbox.insert(END, "a list entry")

# Grid

inBoxButton.grid(row=1, column=1)
sentButton.grid(row=1, column=2)
toWriteButton.grid(row=1, column=3)
delMessageButton.grid(row=1, column=2)
readMessageButton.grid(row=1, column=3)

factory = Twist_Factory()
reactor.connectTCP("localhost", 12345, factory)

tksupport.install(tk)

reactor.run()
