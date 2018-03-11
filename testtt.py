import json


def createJSON(js, command):
    js['command'] = command
    return json.dumps(js)

ss = {"hi": 123}
j = createJSON(ss, 'jopa')
print(j)
