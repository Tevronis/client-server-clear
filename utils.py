import json

comands = []


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
