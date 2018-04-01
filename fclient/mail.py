import json


def to_send_message(from_, header, recivers, data, date):
    js = {'command': 'SETMESSAGE', 'from': from_, 'header': header, 'recivers': recivers, 'data': data,
          'date': date}
    toSent = json.dumps(js)
    return toSent


def mailPrint(j):
    result = "FROM: " + j["from"] + "\n"
    result += j["header"] + "\n"
    result += j["data"] + "\n"
    result += j["date"] + "\n"
    return result
