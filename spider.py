#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" 

"""

__author__ = 'fishzd'

import requests
import re
import json
from bs4 import BeautifulSoup
import xlrd
import xlwt

url = "https://www.huya.com/kaerlol"
dir_url = "https://www.huya.com/l"

def parse_room(url):

    reponse = requests.get(url)
    html = reponse.text

    group = re.search(r'"lp":"?(\d*?)"?,', html)
    pid = group.group(1)

    rank_api = "https://www.huya.com/cache5min.php?m=WeekRank&do=getItemsByPid&pid="

    rank_url = rank_api + pid

    rank_rep = requests.get(rank_url)
    rank_json = rank_rep.text
    rank = json.loads(rank_json)

    rank_list = rank['data']['vWeekRankItem']
    return [r['iScore'] for r in rank_list]

def parse_dir(dir_url):
    reponse = requests.get(dir_url)
    html = reponse.text

    soup = BeautifulSoup(html, 'html.parser')
    room_tags = soup.find_all('li', 'game-live-item')

    room_info_list = []

    for room in room_tags:
        room_info = {}
        room_info['name'] = room.span.span.i.string
        room_info['url'] = room.a['href']
        room_info['num'] = room.find('i', 'js-num').string
        room_info['rank'] = parse_room(room.a['href'])
        room_info_list.append(room_info)

    return room_info_list

room_list = parse_dir(dir_url)

huya_room_book = xlwt.Workbook()
sheet = huya_room_book.add_sheet('page1', cell_overwrite_ok=True)

for row, room_info in enumerate(room_list):

    sheet.write(row, 0, room_info['name'])
    sheet.write(row, 1, room_info['url'])
    sheet.write(row, 2, room_info['num'])
    for col, rank_score in enumerate(room_info['rank']):
        sheet.write(row, col+3, rank_score)

huya_room_book.save('huya room info.xls')