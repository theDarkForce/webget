# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import urllib2
import HTMLParser
from dom import *
from doclex import doclex
import pymongo

url = "http://jj.hbtv.com.cn/"

collection = None

'''
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
'''

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, url):
        self.link = []
        self.data = []
        self.key_url = []

        self.url = url
        self.link_url = ""

        self.current_tag = ""

        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    self.link_url = value
                    self.link.append(value)

    def handle_data(self, data):
        if self.current_tag == 'title':
            keys = doclex.simplesplit(data)
            for key in keys:
                self.key_url.append({'key':key, 'url': self.url})
        elif self.current_tag == 'a':
            keys = doclex.simplesplit(data)
            if isinstance(keys, list) and len(keys) > 0:
                for key in keys:
                    self.key_url.append({'key':key, 'url': self.link_url})
        else:
            self.data.append(data)

def process_data(data):
    return doclex.lex(data)

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

def process_page(url, data):
    if data is None:
        return

    htmlp = htmlprocess(url)
    htmlp.feed(data)

    for it in htmlp.key_url:
        collection.insert(it)

    for data in htmlp.data:
        if len(data) > 32:
            keys = doclex.simplesplit(data)
            if isinstance(keys, list) and len(keys) > 0:
                for key in keys:
                    collection.insert({'key':key, 'url': url})
        else:
            keys1 = process_data(data)
            for key1 in keys1:
                collection.insert({"key":key1,"url":url})

    for url1 in htmlp.link:
        process_link(url1)


#process_link(url)
