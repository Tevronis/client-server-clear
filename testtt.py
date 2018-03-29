import json

l = (1, 2)

d = {"1": l}
open("test.txt", 'w').close()
with open("test.txt", 'w') as file:
    json.dump(d, file)

with open("test.txt", 'r') as file:
    js = json.load(file)
    print(js["1"])