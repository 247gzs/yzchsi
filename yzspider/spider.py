# -*- coding: utf-8 -*-
import csv
import re
from urllib import parse
import requests
from bs4 import BeautifulSoup
from yzspider import settings
from yzspider import utils


def yz_major_spider():
    """爬取研招网对应专业的所有学校"""
    item_list = []
    for i in range(3):
        settings.yz_major_data['pageno'] = i + 1
        response = requests.get(
            'https://yz.chsi.com.cn/zsml/queryAction.do',
            headers=settings.headers,
            params=settings.yz_major_data
        ).content.decode()
        soup = BeautifulSoup(response, features='html.parser')
        for tr in soup.find_all('tr'):
            if '招生单位' in tr.text:
                continue
            item = {
                'province': tr.find_all('td')[1].text,
                'school': tr.find_all('a')[0].text,
                'url': tr.find_all('a')[0].get_attribute_list('href')[0]
            }
            item_list.append(item)
    utils.save_json(item_list)
    return item_list


def yz_school_url_spider(item_list):
    pattern = re.compile(rf'zsml/kskm\.jsp\?id=(?P<school_id>\d+)', re.I | re.S)
    school_url = 'https://yz.chsi.com.cn/zsml/kskm.jsp?id={}'
    for index, item in enumerate(item_list, start=1):
        url = parse.urljoin(settings.base_url, item['url'])
        content = requests.get(url, headers=settings.headers).content.decode()
        search = pattern.search(content)
        school_id = search.group('school_id')
        item['school_url'] = school_url.format(school_id)
        print(index, school_id)

    utils.save_json(item_list, filename='school.json')
    return item_list


def yz_school_info_spider(item_list):
    for index, item in enumerate(item_list, start=1):
        school_url = item['school_url']
        content = requests.get(school_url, headers=settings.headers).content.decode()
        soup = BeautifulSoup(content, features='html.parser')
        soup = soup.find_all('table', **{'class': 'zsml-condition'})[0]
        for data in soup.find_all('tr'):
            td_list = []
            for td in data.find_all('td'):
                td_list.append(td.text.strip())
            while td_list:
                x = td_list.pop(0)
                x = x.strip().replace('：', '')
                y = td_list.pop(0)
                item[x] = y
    utils.save_json(item_list)
    return item_list


def transfer(item_list):
    student_number = 0
    pattern = re.compile(r'(?P<number>\d+)', re.S | re.I)
    for item in item_list:
        item.pop('url')
        item['省份'] = item.pop('province')
        item['学校'] = item.pop('school')
        item['学校链接'] = item.pop('school_url')

        search = pattern.search(item['拟招人数'])
        student_number += int(search.group('number'))
    print(f'共招生人数：', student_number)
    utils.save_json(item_list, filename='结果.json')
    return item_list


def save_excel(item_list):
    headers = [
        '学校', '学校链接', '省份', '招生单位', '考试方式', '院系所', '专业', '学习方式',
        '研究方向', '指导老师', '拟招人数', '备注'
    ]
    with open('学校信息.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for item in item_list:
            row = []
            for header in headers:
                row.append(item[header])
            f_csv.writerow(row)
