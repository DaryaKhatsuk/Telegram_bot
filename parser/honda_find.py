import json
import re


def hondafind():
    honda = []
    with open('../cars.json', newline='', encoding='UTF-8')as file:
        data = json.load(file)
        for i in data:
            if re.findall(r'https+.+/honda/+.+\d{9}', str(i)):
                honda.append(i)
                # print(i)
    print(honda, "\n")
    print(honda[0])
    return honda


honda = hondafind()
