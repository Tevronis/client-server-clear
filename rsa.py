# coding=utf-8
import random
from fractions import gcd
import sympy

ALPH = """abcdefghijklmnopqrstuvwxyz .,!@#$%^&*()_-=+"'?><`~ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890:;[]{}"""
table = dict()
table_rev = dict()
for symbol in ALPH:
    value = ord(symbol)
    if ord(symbol) < 100:
        value += 800
    table[symbol] = value
    table_rev[value] = symbol


class RSA:
    def __init__(self, length):
        self.p, self.q = self.__generatePrime(length)
        self.n = self.p * self.q
        self.f = (self.p - 1) * (self.q - 1)
        self.e = self.__generateE()
        self.d = self.__generateD()

        self.generate_table()

    def getKeys(self):
        return (self.e, self.n), (self.d, self.n)

    @staticmethod
    def __encrypt_symbol(m, open_key):
        return pow(m, open_key[0], open_key[1])

    @staticmethod
    def __decrypt_symbol(c, secret_key):
        return pow(c, secret_key[0], secret_key[1])

    @staticmethod
    def encrypt(text, open_key):
        print "encrypt"
        result = []
        block = ""
        for symbol in text:
            if int(block + str(table[symbol])) < open_key[1]:
                block += str(table[symbol])
            else:
                item = RSA.__encrypt_symbol(int(block), open_key)
                result.append(item)
                block = str(table[symbol])
        else:
            item = RSA.__encrypt_symbol(int(block), open_key)
            result.append(item)

        return ':'.join(map(str, result))

    @staticmethod
    def decrypt(crypt, secret_key):
        print "decrypt"
        crypt = crypt.split(":")
        result = ""
        for block in crypt:
            item = RSA.__decrypt_symbol(int(block), secret_key)
            for c in range(0, len(str(item)), 3):
                result += table_rev[int(str(item)[c:c + 3])]
        return result

    def __generatePrime(self, length):
        print "generate q, p"
        a = sympy.randprime(2 ** (length - 1), 2 ** length)
        b = sympy.randprime(2 ** (length - 1), 2 ** length)
        return a, b

    def __generateE(self):
        print "generate e"
        # 17 257 65537
        result = 3
        for num in sympy.primerange(2, self.f):
            if gcd(num, self.f) == 1:
                result = num
                break
        return result

    def __generateD(self):
        print "generate d with f: {0} e: {1}".format(self.f, self.e)
        # (d * e - 1) % f == 0
        d = 2
        while (d * self.e) % self.f != 1:
            d += 1
        return d  # 6111579

    def generate_table(self):
        print "generate table"

# rsa = RSA(10)

# alisa_ok, alisa_sk = rsa.getKeys()
# print alisa_ok, alisa_sk
# text = "nastia_prekrasnaya_divochka<3"
# print text

# encr = rsa.encrypt(text, alisa_ok)
# print encr

# decr = rsa.decrypt(encr, alisa_sk)
# print decr
