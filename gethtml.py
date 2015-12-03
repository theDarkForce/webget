# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib2
import HTMLParser
from doclex import doclex
import time
import pymongo
import chardet

url = "http://jj.hbtv.com.cn/"

collection = None
collection_url_profile = None

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

def judged_url(url):
    if url.find('http') == -1:
        return False
    return True

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, url):
        self.link = []
        self.data = []
        self.key_url = {}

        self.url = url
        self.link_url = ""

        self.current_tag = ""

        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    if not judged_url(value):
                        value = self.url + value
                    self.link_url = value
                    self.link.append(value)

    def handle_data(self, data):
        if self.current_tag == 'title':
            keys = doclex.simplesplit(data)
            if isinstance(keys, list) and len(keys) > 0:
                for key in keys:
                    if not self.key_url.has_key(key):
                        self.key_url[key] = []
                    self.key_url[key].append(self.url)
        elif self.current_tag == 'a':
            if not judged_url(self.link_url):
                self.link_url = self.url + self.link_url
            keys = doclex.simplesplit(data)
            if isinstance(keys, list) and len(keys) > 0:
                for key in keys:
                    if not self.key_url.has_key(key):
                        self.key_url[key] = []
                    self.key_url[key].append(self.link_url)
        else:
            if self.current_tag == 'p' or self.current_tag == 'div':
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
        #import traceback
        #traceback.print_exc()
        #print 'get_page error', url
        pass

def process_link(url):
    url_profile_dict = process_url_real(url, [])

    for key, value in url_profile_dict.iteritems():
        encoding = chardet.detect(value)
        str = unicode(value, encoding['encoding'])
        collection_url_profile.insert({'key':key, 'urlprofile':str, 'timetmp':time.time()})

def process_url_real(url, process_link_list):
    if url in process_link_list:
        return

    process_link_list.append(url)
    url_profile_dict = {}

    data = get_page(url)
    if data is None:
        return

    pageinfo = process_page(url, data)
    if pageinfo is None:
        return

    link_list, key_url1, url_profile = pageinfo
    url_profile_dict[url] = url_profile

    key_url = {}

    def process_sub_link_list(_data_list, process_link_list):
        link_list = []
        key_url = {}
        url_profile_dict = {}

        for url, data in _data_list.iteritems():
            if url in process_link_list:
                continue

            process_link_list.append(url)

            pageinfo = process_page(url, data)
            if pageinfo is not None:
                linklist, keyurl, urlprofile = pageinfo
                link_list.extend(linklist)
                for key, value in keyurl.iteritems():
                    if key_url.has_key(key):
                        key_url[key] += value
                    else:
                        key_url[key] = value
                url_profile_dict[url] = urlprofile

        return link_list, key_url, url_profile_dict

    def lprocess_link_list(data_list, key_url, process_link_list):
        while isinstance(data_list, dict) and len(data_list) > 0:
            linklist, keyurl, urlprofile = process_sub_link_list(data_list, process_link_list)

            data_list = {}
            for key, value in keyurl.iteritems():
                if not key_url.has_key(key):
                    key_url[key] = []

                for url in value:
                    if not data_list.has_key(url):
                        data = get_page(url)
                        if data is not None:
                            data_list[url] = data
                        else:
                            continue

                    if url not in key_url[key]:
                        key_url[key].append(url)
                        collection.insert({'key':key, 'url':url, 'timetmp':time.time()})

                if len(data_list) > 50:
                    url_profile_dict.update(lprocess_link_list(data_list, key_url, process_link_list))
                    data_list = {}

            for url in linklist:
                data = get_page(url)
                if data is not None:
                    data_list[url] = data

                if len(data_list) > 50:
                    url_profile_dict.update(lprocess_link_list(data_list, key_url, process_link_list))
                    data_list = {}

            url_profile_dict.update(urlprofile)

        return url_profile_dict

    data_list = {}
    for key, value in key_url1.iteritems():
        if not key_url.has_key(key):
            key_url[key] = []

        for url in value:
            if not data_list.has_key(url):
                data = get_page(url)
                if data is not None:
                    data_list[url] = data
                else:
                    continue

            if url not in key_url[key]:
                key_url[key].append(url)
                collection.insert({'key':key, 'url':url, 'timetmp':time.time()})

            if len(data_list) > 50:
                url_profile_dict.update(lprocess_link_list(data_list, key_url, process_link_list))
                data_list = {}

    for url in link_list:
        if not data_list.has_key(url):
            data = get_page(url)
            if data is not None:
                data_list[url] = data

            if len(data_list) > 50:
                url_profile_dict.update(process_link_list(data_list, key_url, process_link_list))
                data_list = {}

    return url_profile_dict

def process_page(url, data):
    if data is None:
        return

    try:
        key_url = {}
        url_profile = ""

        htmlp = htmlprocess(url)
        encoding = chardet.detect(data)
        udata = unicode(data, encoding['encoding'])
        htmlp.feed(udata.encode('utf-8'))

        key_url.update(htmlp.key_url)
        if len(key_url) > 0:
            for key, value in key_url.iteritems():
                if len(value) > 0:
                    urllist = []
                    urllist = [url for url in value if urllist.count(url) == 0]
                    if url not in key_url[key]:
                        key_url[key] = urllist

        for data in htmlp.data:
            if len(data) < 32:
                keys = doclex.simplesplit(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        if not key_url.has_key(key):
                            key_url[key] = []
                        if url not in key_url[key]:
                            key_url[key].append(url)
            else:
                if len(data) > 100:
                    url_profile = data[0:len(data) if len(data) < 100 else 100] + "..."
                keys1 = process_data(data)
                for key1 in keys1:
                    if not key_url.has_key(key1):
                        key_url[key1] = []
                    if url not in key_url[key1]:
                        key_url[key1].append(url)

        return htmlp.link, key_url, url_profile

    except:
        import traceback
        traceback.print_exc()
        #print 'get_page error', url
        pass


#process_link(url)
