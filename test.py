import json
import re

with open('cars.json', newline='', encoding='UTF-8') as file:
    data = json.load(file)
    honda = {}
    for i in data:
        if re.findall(r'https+.+/honda/+.+\d{9}', str(i)):
            honda.update(i)
    # print(honda_find)
    output_honda = []
    for i, j in honda.items():
        # print(i, j)
        # for j in honda.items():
        output_honda.append(i)
        output_honda.append(j)
    print(output_honda)
