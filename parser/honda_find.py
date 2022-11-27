import json
import re


def hondafind():
    honda = {}
    with open('../cars.json', newline='', encoding='UTF-8')as file:
        data = json.load(file)
        for i in data:
            if re.findall(r'https+.+/honda/+.+\d{9}', str(i)):
                honda.update(i)
    return honda


honda = hondafind()
