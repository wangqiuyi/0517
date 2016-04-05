#!/usr/bin/env python
#coding:utf-8

import sys
import urllib
import urllib2
import re
import json
from xpinyin import Pinyin
from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks

reload(sys)
sys.setdefaultencoding('utf8')

class Spider:

    # 获取宠物种类的url
    def __init__(self):
        self.limit = 50
        self.site_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?format=json&resource_id=6839&query=%s' 
        self.pet_site_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?format=json&resource_id=6829&query=%s&pn=%d&rn=50&from_mid=1' 

    def getPetBreeds(self):
        url = self.site_url % ('宠物大全')
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        result = response.read().decode('gbk')
        if result is not None:
            data = json.loads(result)['data']
            if data:
                return data[0]['result']
            else:
                print '没有取到数据'

    def getPets(self, breed, page):
        query = breed['ename']
        if '宠物' not in query:
            query = '宠物' + query
        url = self.pet_site_url % (query, page) 
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        result = response.read().decode('gbk')
        if result is not None:
            data = json.loads(result)['data'][0]['disp_data']
            if data:
                return data

es = ElasticSearch('http://localhost:9200/')
es.delete_index('pet')
spider = Spider()
breeds = spider.getPetBreeds()
p = Pinyin()
for breed in breeds:
    flg = 1
    page = 1
    pet_list = []
    while(flg):
        pets = spider.getPets(breed, (page - 1) * spider.limit)
        if not pets:
            flg = 0
        else:
            page = page + 1
            for pet in pets:
                pet_obj = {}
                pet_obj['name'] = pet['name']
                pet_obj['img'] = pet['img']
                pet_obj['type'] = breed['ename'] 
                pet_list.append(pet_obj)
                #print pet['name'] + '\t' + p.get_pinyin(pet['name'], '')
    print breed['ename'] + '\n'
    if not pet_list:
        continue
    doc_type = p.get_pinyin(breed['ename'].replace('宠物', ''), '')
    es.bulk((es.index_op(pet_obj) for pet_obj in pet_list), doc_type=doc_type, index = 'pet')
es.refresh('pet')
