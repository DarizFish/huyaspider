#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" 

"""

__author__ = 'fishzd'

import requests
import re
import json

url = "https://www.huya.com/kaerlol"

reponse = requests.get(url)
html = reponse.text

group = re.search(r'"lp":"(\d*?)"', html)
pid = group.group(1)

rank_api = "https://www.huya.com/cache5min.php?m=WeekRank&do=getItemsByPid&pid="

rank_url = rank_api + pid

rank_rep = requests.get(rank_url)
rank_json = rank_rep.text
rank = json.loads(rank_json)

rank_list = rank['data']['vWeekRankItem']
for r in rank_list:
    print(r['iScore'])

