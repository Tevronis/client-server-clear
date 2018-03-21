# coding=utf-8
import random
from fractions import gcd

def yakobi(a, b):
    if gcd(a, b) != 1:
        return 0
    r = 1

    if a < 0:
        a = -a
        if b % 4 == 3:
            r = -r

    def stuff(a, b, r):
        t = 0
        while a % 2 == 0:
            t += 1
            a /= 2
        if t % 2 == 1:
            if (b % 8) == 3 or (b % 8) == 5:
                r = -r

        if (a % 4) == (b % 4) == 3:
            r = -r
        c = a
        a = b % c
        b = c
        return a, b, r

    a, b, r = stuff(a, b, r)
    while a != 0:
        a, b, r = stuff(a, b, r)

    return r

def isPrime(num):

    for k in range(1, 5):
        a = random.randrange(1, num)
        if not gcd(a, num) > 1:
            b = a ** ((num - 1) / 2)
            r = yakobi(a, num)
            if (b - r) % num != 0:
                break
        else:
            break
    else:
        return True
    return False

class RSA:

    ALPH = """abcdefghijklmnopqrstuvwxyz .,!@#$%^&*()_-=+"'?><`~ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890:;[]{}"""

    def __init__(self, length):
        self.p, self.q = self.__generatePrime(length)
        self.n = self.p * self.q
        self.f = (self.p - 1) * (self.q - 1)
        self.e = self.__generateE()
        self.d = self.__generateD()
        self.table = dict()
        self.table_rev = dict()
        self.generate_table()

    def getKeys(self):
        return (self.e, self.n), (self.d, self.n)

    @staticmethod
    def __encrypt_symbol(m, open_key):
        return pow(m, open_key[0], open_key[1])

    @staticmethod
    def __decrypt_symbol(c, secret_key):
        return pow(c, secret_key[0], secret_key[1])

    #@staticmethod
    def encrypt(self, text, open_key):
        result = []
        block = ""
        for symbol in text:
            if int(block + str(self.table[symbol])) < self.n:
                block += str(self.table[symbol])
            else:
                item = RSA.__encrypt_symbol(int(block), open_key)
                result.append(item)
                block = str(self.table[symbol])
        else:
            item = RSA.__encrypt_symbol(int(block), open_key)
            result.append(item)

        return ':'.join(map(str, result))

    #@staticmethod
    def decrypt(self, crypt, secret_key):
        crypt = crypt.split(":")
        result = ""
        for block in crypt:
            item = RSA.__decrypt_symbol(int(block), secret_key)
            for c in range(0, len(str(item)), 3):
                result += self.table_rev[int(str(item)[c:c+3])]
        return result

    def __generatePrime(self, length):
        result = []
        for item in range(2**(length-1), 2**length):
            if isPrime(item):
                result.append(item)
            if len(result) == 2:
                break
        return result[0], result[1]

    def __generateE(self):
        # 17 257 65537
        return 3

    def __generateD(self):
        # (d * e - 1) % f == 0
        d = 2
        while (d * self.e - 1) % self.f != 0:
            d += 1
        return d # 6111579

    def generate_table(self):
        for symbol in RSA.ALPH:
            value = ord(symbol)
            if ord(symbol) < 100:
                value += 800
            self.table[symbol] = value
            self.table_rev[value] = symbol

rsa = RSA(3)

alisa_ok, alisa_sk = rsa.getKeys()

text = "nastia_prekrasnaya_divochka<3"
print text

encr = rsa.encrypt(text, alisa_ok)
print encr

decr = rsa.decrypt(encr, alisa_sk)
print decr