import json

from fclient.user import User

currentUser = User()


def parse_request(data):
    result = data.split('}{')
    for idx in range(1, len(result) - 1):
        result[idx] = '{' + result[idx] + '}'
    if len(result) > 1:
        result[0] = result[0] + '}'
        result[-1] = '{' + result[-1]
    return result



class LocalJSON:
    @staticmethod
    def addCommand(js, command):
        js['command'] = command
        return json.dumps(js)

    @staticmethod
    def message(message):
        js = {"data": message}
        LocalJSON.addCommand(js, "PRINT")
        return json.dumps(js)

    @staticmethod
    def addField(js, name, value):
        js[name] = value
        return js
