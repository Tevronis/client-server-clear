def parse_request(data):
    result = data.split('}{')
    for idx in range(1, len(result) - 1):
        result[idx] = '{' + result[idx] + '}'
    if len(result) > 1:
        result[0] = result[0] + '}'
        result[-1] = '{' + result[-1]
    return result


print parse_request('{qwerwqt}')

exit()
from PIL import Image

foo = Image.open("test2.jpg")

# foo = foo.resize((160, 300), Image.ANTIALIAS)
foo.save("test.jpg", quality=95)
foo.save("test5.jpg", optimize=True, quality=95)
foo.save("test6.jpg", quality=1)
