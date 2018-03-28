import hashlib
import json
import os

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineOnlyReceiver

from client.utils import LocalJSON
from server_utils import merge_two_dicts


class Server(LineOnlyReceiver):
    name = ""

    def getName(self):
        if self.name != "":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        print "New connection from " + self.getName()
        self.factory.clientProtocols.append(self)

    def connectionLost(self, reason):
        print "Lost connection from " + self.getName()
        self.factory.clientProtocols.remove(self)
        self.factory.sendMessageToAllClients(LocalJSON.message(self.getName() + " has disconnected."))

    def lineReceived(self, line):
        js = json.loads(line)
        print "in:", json.dumps(js)
        command = js['command']
        # TODO {'command': cmd, 'data': {data}}

        if command == 'REGISTRATION':
            self.user_registration(js)

        if command == 'VERIFICATION':
            self.sendLine(self.verification(js))

        if command == 'GETSENT':
            self.sendLine(self.get_mails_sent_id(js))

        if command == 'GETINBOX':
            self.sendLine(self.get_mails_inbox_id(js))

        if command == 'GETMESSAGE':
            self.sendLine(self.mail_to_send(js))

        if command == 'DELMESSAGE':
            self.sendLine(self.delete_message(js))

        if command == 'SETMESSAGE':
            self.sendLine(self.dump_jsons(js))

        if command == 'SETOPENKEY':
            self.sendLine(self.set_open_key(js))

        if command == 'GETOPENKEY':
            self.sendLine(self.get_user_open_key(js))

    def server_handler(self, fun, js):
        self.sendLine(fun(js))

    def sendLine(self, line):
        self.transport.write(line + "\r\n")

    @staticmethod
    def create_default_json(dir):
        # TODO: check if file exist TODO need validation
        open(dir, 'w').close()
        with open(dir) as f:
            if len(f.readline()) > 1:
                return
        with open(dir, 'w') as f:
            f.write('{"mails":[]}')

    @staticmethod
    def add_item_json(dir, field, item):
        with open(dir, 'r') as json_file:
            jsn = json.load(json_file)
            jsn[field].append(item)
        with open(dir, 'w') as json_file:
            json.dump(jsn, json_file)

    @staticmethod
    def set_item_json(dir, field, item):
        with open(dir, 'r') as json_file:
            jsn = json.load(json_file)
            jsn[field] = item
        with open(dir, 'w') as json_file:
            json.dump(jsn, json_file)

    @staticmethod
    def set_inbox(js):
        if not (os.path.exists('Users/' + js['from'])):
            os.mkdir("""Users\{0}""".format(js['from']))
        for to in js['recivers']:
            dir = """Users\{0}\mails_inbox.json""".format(to)
            Server.add_item_json(dir, 'mails', str(js['id']))

    @staticmethod
    def dump_jsons(js):
        try:
            if not (os.path.exists('Users/' + js['from'])):
                os.mkdir("""Users\{0}""".format(js['from']))
            mail_fold = """Mails\{0}""".format(str(js['id']))
            user_fold_sent = """Users\{0}\mails_sent.json""".format(js['from'])

            Server.create_default_json(user_fold_sent)
            Server.set_inbox(js)
            Server.add_item_json(user_fold_sent, 'mails', str(js['id']))
            with open(mail_fold, 'w') as f:
                f.write(json.dumps(js))
            return json.dumps({'command': 'PRINT', 'data': 'OK'})
        except:
            raise Exception("message not JSON!: " + json.dumps(js))

    @staticmethod
    def get_header_mail(dir):
        result = {'mails': []}
        with open(dir) as json_file:
            jsn = json.load(json_file)
            mails = jsn["mails"]
            for message_id in mails:
                mail = """Mails\{0}""".format(message_id)
                with open(mail) as ffile:
                    jsn = json.load(ffile)
                    obj_mail = {'from': jsn['from'], 'header': jsn['header'], 'id': jsn['id']}
                    result['mails'].append(obj_mail)
        return result

    @staticmethod
    def get_mails_sent_id(js):
        try:
            mail_fold = """Users\{0}\mails_sent.json""".format(str(js['login']))

            result = Server.get_header_mail(mail_fold)

            result = LocalJSON.addCommand(result, "SENT")
            return result
        except:
            raise Exception("GETSENT with: " + json.dumps(js))

    @staticmethod
    def get_mails_inbox_id(js):
        try:
            mail_fold = """Users\{0}\mails_inbox.json""".format(str(js['login']))

            result = Server.get_header_mail(mail_fold)

            result = LocalJSON.addCommand(result, "INBOX")
            return result
        except:
            raise Exception("GETINBOX with: " + json.dumps(js))

    @staticmethod
    def create_default_user_info_json(dir, js):
        open(dir, 'w').close()
        with open(dir) as f:
            if len(f.readline()) > 1:
                return
        with open(dir, 'w') as f:
            todump = {"login": js["login"], "password": js["password"], "name": js["name"]}
            f.write(json.dumps(todump))

    @staticmethod
    def add_to_users_list(dir, js):
        Server.add_item_json(dir, 'users', json.dumps(js))

    @staticmethod
    def user_registration(js):
        try:
            result = {"command": "REGISTRATION"}
            if not (os.path.exists('Users/' + js["login"])):
                os.mkdir("""Users\{0}""".format(js["login"]))
            user_fold_sent = """Users\{0}\mails_sent.json""".format(js["login"])
            user_fold_inbox = """Users\{0}\mails_inbox.json""".format(js["login"])
            user_folder_user_info = """Users\{0}\user_info.json""".format(js["login"])
            users_list_dir = "Users\users.json"

            Server.create_default_json(user_fold_sent)
            Server.create_default_json(user_fold_inbox)
            Server.create_default_user_info_json(user_folder_user_info, js)
            Server.add_to_users_list(users_list_dir, js)
            return json.dumps(result)
        except:
            raise Exception("error with arg: " + json.dumps(js))

    @staticmethod
    def verification(js):
        # in: json {login, password}
        # out: json {command, status, user param..}
        result = {"command": "USER"}
        if not (os.path.exists('Users/' + js["login"])):
            result["status"] = "BAD"
            return json.dumps(result)
        user_info = """Users\{0}\user_info.json""".format(js["login"])
        with open(user_info) as f:
            jsf = json.load(f)
            if js["password"] != jsf["password"]:
                result["status"] = "BAD"
            else:
                result = merge_two_dicts(result, jsf)
                result["status"] = "OK"
        return json.dumps(result)

    @staticmethod
    def get_mail(js):
        try:
            dir = """Mails\{0}""".format(js["idMail"])
            with open(dir) as f:
                result = f.readline()
            return result
        except:
            raise Exception('bad GETMAIL command with JSON: ' + json.dumps(js))

    @staticmethod
    def get_recivers(id_mail):
        m = Server.get_mail(id_mail)
        j = json.loads(m)
        return j['recivers']

    @staticmethod
    def delete_message(js):
        try:
            def delete(dir, id):
                with open(dir, 'r') as json_file:
                    jsn = json.load(json_file)
                    if id in jsn['mails']:
                        jsn['mails'].remove(id)
                with open(dir, 'w') as json_file:
                    json.dump(jsn, json_file)

            id_mail = js['idMail']
            login = js['login']
            users = set()
            for item in Server.get_recivers(id_mail):
                users.add(item)
            users.add(login)
            for to in users:
                delete("""Users\{0}\mails_inbox.json""".format(to), id_mail)
                delete("""Users\{0}\mails_sent.json""".format(to), id_mail)
            return json.dumps({'command': 'PRINT', 'data': 'OK'})
        except:
            return json.dumps({'command': 'PRINT', 'data': 'FALSE'})

    @staticmethod
    def mail_to_send(js):
        mail = Server.get_mail(js)
        m = hashlib.md5()
        m.update(mail)
        print m.hexdigest()
        j_obj = {'HASH': str(m.hexdigest()), 'MESSAGE': mail}
        return LocalJSON.addCommand(j_obj, 'MESSAGE')

    @staticmethod
    def set_open_key(js):
        user_info = """Users\{0}\user_info.json""".format(js["login"])
        Server.set_item_json(user_info, 'open_key', js['open_key'])
        return json.dumps({"status": "OK"})

    @staticmethod
    def get_user_open_key(js):
        user_info = """Users\{0}\user_info.json""".format(js["login"])
        with open(user_info) as file:
            j = json.load(file)
            result = {"command": "OPENKEY", "login": js["login"], "open_key": j["open_key"]}
        return json.dumps(result)



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
