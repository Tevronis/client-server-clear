# coding=utf-8
import json

from rsa import RSA


class User:
    def __init__(self):
        self.name = 'untitled'
        self.groups = []
        self.self_mails = []
        self.login = 'login'
        self.password = '123456'
        self.secret_key = 0
        self.open_key = 0

    def __get_skey(self):
        with open(self.login + '.dat') as f:
            js = json.load(f)
            self.secret_key = js['s_key']

    def addGroup(self, group):
        self.groups.append(group)

    def generateRsaKeys(self):
        # вызыфвать один раз при регистрации!
        result = RSA(12).getKeys()
        self.open_key, self.secret_key = result
        return result

    def setLogin(self, login):
        self.login = login

    def setPassword(self, password):
        self.password = password

    def setParams(self, params):
        self.name = params["name"]
        self.login = params["login"]
        self.password = params["password"]
        self.__get_skey()
        #if params["open_key"]:
        #    self.open_key = params["open_key"]
        # self.secret_key
