# -*- coding: utf-8 -*-
import json


def save_json(item_list, filename='school.json'):
    with open(filename, 'w') as fw:
        content = json.dumps(item_list, indent=2, ensure_ascii=False)
        fw.write(content)


def read_json(filename='school.json'):
    with open(filename, 'r') as fr:
        content = json.loads(fr.read())
        return content
