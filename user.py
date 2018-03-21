class User:
    def __init__(self):
        self.name = 'untitled'
        self.groups = []
        self.self_mails = []
        self.login = 'login'
        self.password = '123456'
        self.secret_key = 0
        self.open_key = 0

    def addGroup(self, group):
        self.groups.append(group)

    def generateRsaKeys(self):
        return 1, 2

    def setLogin(self, login):
        self.login = login

    def setPassword(self, password):
        self.password = password

    def setParams(self, params):
        self.name = params["name"]
        self.login = params["login"]
        self.password = params["password"]
        #if params["open_key"]:
        #    self.open_key = params["open_key"]
        # self.secret_key
