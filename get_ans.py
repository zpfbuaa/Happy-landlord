# -*- coding: utf-8 -*-
# @Time    : 2018/12/15 15:54
# @Author  : 伊甸一点
# @FileName: get_ans.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

from urllib import request
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

hard_url = 'http://www.87g.com/zixun/76007.html'
easy_url = 'http://www.87g.com/zixun/76006.html'
expert_url = 'http://www.87g.com/zixun/76008.html'

def get_ans(URL):
    ans_dict = {}
    response  = request.urlopen(URL)
    total_html = response.read().decode("utf-8")
    total_html = BeautifulSoup(total_html, 'html.parser')
    response.close()
    total_url = total_html.tbody.find_all('td')
    length_url = len(total_url)


    for i in tqdm(range(101, length_url)):
        item_url = total_url[i].a['href']
        # print(item_url)
        question_id = total_url[i].text.split('第')[1].split('关')[0]

        item_response = request.urlopen(item_url)
        single_ans = item_response.read().decode("utf-8")
        single_ans = BeautifulSoup(single_ans, 'html.parser')
        item_response.close()
        item_find = str(single_ans.find_all(attrs={"class":"news-content"})[0].find_all('p')[4])
        item_len = len(item_find.split('<p>'))
        if(item_len == 2):
            ans_dict[question_id] = '['+item_find.split('<p>')[1].split('</p>')[0]+']('+item_url+')'
        else:
            new_item_find = str(single_ans.find_all(attrs={"class":"news-content"})[0].find_all('p')[3])
            ans_dict[question_id] = '['+new_item_find +']('+item_url+')'

    return ans_dict

ans = get_ans(expert_url)


with open('expert.md','w', encoding='utf-8') as f:
    for item in ans.keys():
        f.write('* '+ item+' : '+ str(ans[item])+'\n')


