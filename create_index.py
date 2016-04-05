#!/usr/bin/env python
#coding:utf-8

import pyes

conn = pyes.ES(['127.0.0.1:9200'])#连接es

def create_index(conn):
    conn.indices.create_index('test-index')#新建一个索引

    #定义索引存储结构
    mapping = { u'parsedtext': {'boost': 1.0,
                      'index': 'analyzed',
                      'store': 'yes',
                      'type': u'string',
                      "term_vector" : "with_positions_offsets"},
              u'name': {'boost': 1.0,
                         'index': 'analyzed',
                         'store': 'yes',
                         'type': u'string',
                         "term_vector" : "with_positions_offsets"},
              u'title': {'boost': 1.0,
                         'index': 'analyzed',
                         'store': 'yes',
                         'type': u'string',
                         "term_vector" : "with_positions_offsets"},
              u'position': {'store': 'yes',
                         'type': u'integer'},
              u'uuid': {'boost': 1.0,
                        'index': 'not_analyzed',
                        'store': 'yes',
                        'type': u'string'}
        }

    conn.indices.put_mapping("test-type", {'properties':mapping}, ["test-index"])#定义test-type

    #插入索引数据
    #{"name":"Joe Tester", "parsedtext":"Joe Testere nice guy", "uuid":"11111", "position":1}: 文档数据
    #test-index：索引名称
    #test-type: 类型
    #1: id 注：id可以不给，系统会自动生成
    conn.index({"name":"Joe Tester", "parsedtext":"Joe Testere nice guy", "uuid":"11111", "position":1}, "test-index", "test-type", 1)
    conn.index({"name":"Bill Baloney", "parsedtext":"Bill Testere nice guy", "uuid":"22222", "position":2}, "test-index", "test-type", 2)
    conn.index({"name":u"百 度 中 国"}, "test-index", "test-type")#这个相当于中文的一元切分吧-_-
    conn.index({"name":u"百 中 度"}, "test-index", "test-type")

    conn.default_indices=["test-index"]#设置默认的索引
    conn.indices.refresh()#刷新以获得最新插入的文档


q = pyes.TermQuery("name", "bill")#查询name中包含bill的记录
results = conn.search(q)

for r in results:
    print r

#查询name中包含 百度 的数据
q = pyes.QueryStringQuery(u"百 度",'name')
results = conn.search(q)

for r in results:
    print r

try:
    conn.indices.delete_index("test-index")
except:
    pass
