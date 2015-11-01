# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import urllib2
from LexicalAnalysis import *
from dom import *
from doclex import doclex
import pymongo

url = "http://jj.hbtv.com.cn/"

collection = None

def process_data(data):
    return doclex.lex(data)

def get_link(str):
    try:
        str1 = str.split("href")[1]

        url = ""
        type = 0
        for ch in str1:
            if ch == "\"":
                if type == 0:
                    type = 1
                    continue
                elif type == 1:
                    break
            elif ch == "'":
                if type == 0:
                    type = 2
                    continue
                elif type == 2:
                    break
            if type > 0:
                url += ch

        return url

    except:
        print 'error', str

    url = ""
    type = 0
    for ch in str:
        if ch == "\"":
            if type == 0:
                type = 1
                continue
            elif type == 1:
                break
        elif ch == "'":
            if type == 0:
                type = 2
                continue
            elif type == 2:
                break
        if type > 0:
            url += ch

    return url

def get_page(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()

        return the_page
    except:
        print 'get_page error', url

def process_link(url):
    process_page(url, get_page(url))

def get_data(str):
    str1 = ""
    type = False
    for ch in str:
        if ch == '>':
            type = True
            continue
        elif ch == '<':
            if type == True:
                break
        if type:
            str1 += ch
    print str, str1, 'get_data'
    return str1

def process_page(url, data):
    linkinurl = []

    s = statemachine()
    d = dom()
    for ch in data:
        div = s.push(ch)
        if div[1] is not None:
            d.append(div)
        print d.dom

    for it in d.dom:
        if it[0] == 'p':
            str = get_data(it[1])
            key = process_data(str)
            collection.insert({"key":key,"url":url})
            print {"key":key,"url":url}
        elif it[0] == 'a':
            url1 = get_link(it[1])
            linkinurl.append(url1)

    for url2 in linkinurl:
        process_link(url2)


process_link(url)
