# -*- coding:utf-8 -*-
import hashlib
import json

from tkinter import *
from twisted.internet import reactor, tksupport
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

from fclient.mail import to_send_message
from fclient.storage import comands, requests
from fclient.ui.clientUI import ClientUI
from fclient.ui.listbox import CS_Listbox
from fclient.utils import LocalJSON, currentUser, parse_request
from rsa import RSA

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
        for item in parse_request(data):
            js = json.loads(item)
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
                o_key, s_key = currentUser.generateRsaKeys()
                print o_key
                print s_key
                with open(js['login'] + '.dat', 'w') as file:
                    json.dump({"s_key": s_key}, file)
                self.sendData(json.dumps({"command": "SETOPENKEY", "open_key": o_key, "login": js['login']}))
            if command == 'OPENKEY':
                for request in requests:
                    json_req = json.loads(request)
                    if json_req['command'] == 'SETMESSAGE' and json_req["recivers"] == js["login"]:
                        json_req["data"] = RSA.encrypt(json_req["data"], js['open_key'])
                        self.sendData(json.dumps(json_req))
                requests[:] = [item for item in requests if json.loads(item)['recivers'] != js["login"]]


            print data

    def connectionMade(self):
        print 'Connect good'
        for cmd in comands:
            self.sendData(cmd)

        reload(sys)
        sys.setdefaultencoding('utf-8')

        def sendMAIL(event):
            def send(event):
                # create message and save him to [requests]
                # TODO созать реквест и дождаться ответа сервера с открытым ключом
                # TODO set date
                toSent = to_send_message(from_=currentUser.login, header=title.get(), recivers=to.get(), data=msg.get("1.0", END), date='')
                requests.append(toSent)
                self.sendData(json.dumps({"command": "GETOPENKEY", "user": to.get()}))
                top.destroy()

            top = Toplevel()
            top.title("Message")

            button = Button(top, text="Dismiss", width=10, bd=5)
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
UI = ClientUI(root)
root.mainloop()

tk = Tk()
panelFrame = Frame(tk, height=40, bg='gray')
logFrame = Frame(tk, height=340, width=400)

panelFrame.pack(side='top', fill='x')
logFrame.pack(side='bottom', fill='both', expand=1)
# Buttons:
inBoxButton = Button(panelFrame, text='Inbox', width=10, bd=5)
sentButton = Button(panelFrame, text='Sent', width=10, bd=5)
toWriteButton = Button(panelFrame, text='Write', width=10, bd=5)

delMessageButton = Button(panelFrame, text='delete msg', width=10, bd=5)
readMessageButton = Button(panelFrame, text='read msg', width=10, bd=5)

# del this
tk.title('Client ' + currentUser.login)
tk.geometry('430x200')

listbox = CS_Listbox(logFrame)

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
