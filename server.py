import hashlib
import json
import os
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver

from utils import LocalJSON


def createDefJSON(dir):
    # TODO: check if file exist
    try:
        with open(dir):
            pass
    except:
        e = open(dir, 'w')
        e.close()
    with open(dir) as f:
        if len(f.readline()) > 1:
            return
    with open(dir, 'w') as f:
        f.write('{"mails":[]}')



def add_item_json(dir, field, item):
    with open(dir, 'r') as json_file:
        jsn = json.load(json_file)
        jsn[field].append(item)
    with open(dir, 'w') as json_file:
        json.dump(jsn, json_file)


def setInbox(js):
    if not (os.path.exists('Users/' + js['from'])):
        os.mkdir("""Users\{0}""".format(js['from']))
    for to in js['recivers']:
        dir = """Users\{0}\mails_inbox.json""".format(to)
        add_item_json(dir, 'mails', str(js['id']))


def dumpJsons(js):
    try:
        if not (os.path.exists('Users/' + js['from'])):
            os.mkdir("""Users\{0}""".format(js['from']))
        mail_fold = """Mails\{0}""".format(str(js['id']))
        user_fold_sent = """Users\{0}\mails_sent.json""".format(js['from'])

        createDefJSON(user_fold_sent)
        setInbox(js)
        add_item_json(user_fold_sent, 'mails', str(js['id']))
        with open(mail_fold, 'w') as f:
            f.write(json.dumps(js))
        return json.dumps({'command': 'PRINT', 'data': 'OK'})
    except:
        raise Exception("message not JSON!: " + json.dumps(js))


def getMailsSentID(js):
    try:
        mail_fold = """Users\{0}\mails_sent.json""".format(str(js['login']))
        s_ids = []
        result = {'mails': []}
        try:
            with open(mail_fold) as f:
                jj = json.load(f)
                mm = jj["mails"]
                for i in mm:
                    s_ids.append(i)
            for id_mail in s_ids:
                mail = """Mails\{0}""".format(id_mail)
                with open(mail) as f:
                    jj = json.load(f)
                    obj_mail = {'from': jj['from'], 'header': jj['header'], 'id': jj['id']}
                    result['mails'].append(obj_mail)
        except:
            pass
        result = LocalJSON.addCommand(result, "SENT")
        return result
    except:
        raise Exception("GETSENT with: " + json.dumps(js))


def getMailsInboxID(js):
    try:
        mail_fold = """Users\{0}\mails_inbox.json""".format(str(js['login']))
        s_ids = []
        result = {'mails': []}
        try:
            with open(mail_fold) as f:
                jj = json.load(f)
                mm = jj["mails"]
                for i in mm:
                    s_ids.append(i)
            for id_mail in s_ids:
                mail = """Mails\{0}""".format(id_mail)
                with open(mail) as f:
                    jj = json.load(f)
                    obj_mail = {'from': jj['from'], 'header': jj['header'], 'id': jj['id']}
                    result['mails'].append(obj_mail)
        except:
            pass
        result = LocalJSON.addCommand(result, "INBOX")
        return result
    except:
        raise Exception("GETINBOX with: " + json.dumps(js))


def createDefUserInfoJSON(dir, js):
    try:
        with open(dir):
            pass
    except:
        e = open(dir, 'w')
        e.close()
    with open(dir) as f:
        if len(f.readline()) > 1:
            return
    with open(dir, 'w') as f:
        todump = {"login": js["login"], "password": js["password"], "name": js["name"]}
        f.write(json.dumps(todump))


def add_to_users_list(dir, js):
    add_item_json(dir, 'users', json.dumps(js))


def registerUser(js):
    try:
        # login psw name
        if not (os.path.exists('Users/' + js["login"])):
            os.mkdir("""Users\{0}""".format(js["login"]))
        user_fold_sent = """Users\{0}\mails_sent.json""".format(js["login"])
        user_fold_inbox = """Users\{0}\mails_inbox.json""".format(js["login"])
        user_folder_userInfo = """Users\{0}\user_info.json""".format(js["login"])
        users_list_dir = "Users\users.json"

        createDefJSON(user_fold_sent)
        createDefJSON(user_fold_inbox)
        createDefUserInfoJSON(user_folder_userInfo, js)
        add_to_users_list(users_list_dir, js)
    except:
        raise Exception("error with arg: " + json.dumps(js))


def verification(line):
    dir = "Users\users.json"
    with open(dir) as f:
        j = json.load(f)
        if not j[line] is None:
            f.close()
            return True
    return False


def getMail(js):
    try:
        dir = """Mails\{0}""".format(js["idMail"])
        with open(dir) as f:
            result = f.readline()
        return result
    except:
        raise Exception('bad GETMAIL command with JSON: ' + json.dumps(js))


def getRecivers(idMail):
    m = getMail(idMail)
    j = json.loads(m)
    return j['recivers']


def delMessage(js):
    try:
        def delete(dir, id_mail):
            with open(dir, 'r') as json_file:
                jj = json.load(json_file)
                if id_mail in jj['mails']:
                    jj['mails'].remove(id_mail)
            with open(dir, 'w') as json_file:
                json.dump(jj, json_file)

        id_mail = js['idMail']
        login = js['login']
        users = set()
        for item in getRecivers(id_mail):
            users.add(item)
        users.add(login)
        for to in users:
            delete("""Users\{0}\mails_inbox.json""".format(to), id_mail)
            delete("""Users\{0}\mails_sent.json""".format(to), id_mail)
        return json.dumps({'command': 'PRINT', 'data': 'OK'})
    except:
        return json.dumps({'command': 'PRINT', 'data': 'FALSE'})


def mail_to_send(js):
    mail = getMail(js)
    m = hashlib.md5()
    m.update(mail)
    print m.hexdigest()
    j_obj = {'HASH': str(m.hexdigest()), 'MESSAGE': mail}
    return LocalJSON.addCommand(j_obj, 'MESSAGE')


class Server(LineOnlyReceiver):
    name = ""

    def getName(self):
        if self.name != "":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        print "New connection from " + self.getName()
        # TODO replace to json
        self.sendLine(LocalJSON.message("Welcome to my my chat server."))
        self.factory.sendMessageToAllClients(LocalJSON.message(self.getName() + " has joined the party."))
        self.factory.clientProtocols.append(self)

    def connectionLost(self, reason):
        print "Lost connection from " + self.getName()
        self.factory.clientProtocols.remove(self)
        self.factory.sendMessageToAllClients(LocalJSON.message(self.getName() + " has disconnected."))

    def lineReceived(self, line):
        js = json.loads(line)
        print "in:", json.dumps(js)
        command = js['command']
        if command == 'REGISTRATION':
            registerUser(js)

        if command == 'VERIFICATION':
            # TODO login verification
            pass

        if command == 'GETSENT':
            self.sendLine(getMailsSentID(js))

        if command == 'GETINBOX':
            self.sendLine(getMailsInboxID(js))

        if command == 'GETMESSAGE':
            self.sendLine(mail_to_send(js))

        if command == 'DELMESSAGE':
            self.sendLine(delMessage(js))

        if command == 'SETMESSAGE':
            self.sendLine(dumpJsons(js))

    def sendLine(self, line):
        self.transport.write(line + "\r\n")


class ChatProtocolFactory(ServerFactory):
    protocol = Server

    def __init__(self):
        self.clientProtocols = []

    def sendMessageToAllClients(self, mesg):
        for client in self.clientProtocols:
            client.sendLine(mesg)


print "Starting Server"
factory = ChatProtocolFactory()
reactor.listenTCP(12345, factory)
reactor.run()
