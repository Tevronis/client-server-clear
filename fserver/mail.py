import json


def nextId():
    with open('file_number.txt', 'r+') as f:
        while True:
            try:
                num = int(f.read())
                break
            except:
                pass
        num += 1
        f.seek(0)
        f.truncate()
        f.write(str(num))
        f.close()
    return num


class Mail:
    def __init__(self):
        self._from = ''
        self.id = 0
        self.header = 'untitled'
        self.recivers = []
        self.data = ''
        self.date = '01.12.2017'
        self.read = False

    def readIt(self):
        self.read = True

    def createMessage(self, _from, header, recivers, data, date):
        self._from = _from
        self.header = header
        self.recivers = recivers
        self.data = data
        self.date = date
        self.id = nextId()
        result = json.dumps(
            {'id': self.id, 'from': self._from, 'header': self.header, 'recivers': recivers, 'data': data,
             'date': date, 'read': 0})
        print result
        return result

    @staticmethod
    def mailPrint(j):
        result = "FROM: " + j["from"] + "\n"
        result += j["header"] + "\n"
        result += j["data"] + "\n"
        result += j["date"] + "\n"
        return result
