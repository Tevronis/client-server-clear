import json


class clll:
    AB = clll.fun
    @staticmethod
    def fun():
        print 'qwe'

    def foo(self):
        clll.AB()

c = clll()

print c.foo()