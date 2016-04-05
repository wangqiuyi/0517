#!/usr/bin/env python
#coding:utf-8

from pyelasticsearch import ElasticSearch
from pyelasticsearch import bulk_chunks

es = ElasticSearch('http://localhost:9200/')

def create_index(es):
    # _index, _type, _source, _id
    es.index('contacts','person',{'name': 'Joe Tester', 'age': 25, 'title': 'QA Master'},id=1)

    docs = [{'id': 2, 'name': 'Jessica Coder', 'age': 32, 'title': 'Programmer'},\
            {'id': 3, 'name': 'Freddy Tester', 'age': 29, 'title': 'Office Assistant'}]

    es.bulk((es.index_op(doc, id=doc.pop('id')) for doc in docs),\
            index='contacts',\
            doc_type='person')

    es.refresh('contacts')

def delete_index(es):
    es.delete_index('contacts')

#create_index(es)
print es.get('contacts', 'person', 2)
print es.search('name:joe OR name:freddy', index='contacts')
