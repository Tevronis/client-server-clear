import json


class Group:

    def __init__(self):
        self.name = 'untitled'
        self.users = []
        self.admins = []
        self.mails = []

    def addUser(self, user):
        self.users.append(user)

    @staticmethod
    def getJSONtoADDGROUP(name, users, admin, mails):
        result = json.dumps({"name": name, "users": users, "admin": admin, "mails": mails})
        return result

    @staticmethod
    def getJSONtoJOINGROUP(name, user):
        result = json.dumps({"name": name, "user": user})
        return result

    @staticmethod
    def getJSONtoQUITGROUP(name, user):
        result = json.dumps({"name": name, "user": user})
        return result