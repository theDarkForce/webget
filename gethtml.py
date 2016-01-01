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

collection = None
collection_url_profile = None
collection_url_title = None

def judged_url(url):
    if url is None or url.find('http') == -1:
        return False
    return True

class htmlprocess(HTMLParser.HTMLParser):
    def __init__(self, url):
        self.link = []
        self.data = []
        self.key_url = {}

        self.url = url
        self.link_url = ""

        self.keywords = []
        self.profile = ""

        self.current_tag = ""

        self.style = ""

        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        self.style = 'None'

        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    if not judged_url(value):
                        value = self.url + value
                    self.link_url = value
                    self.link.append(value)
        elif tag == 'meta':
            for name,value in attrs:
                if name == 'name':
                    if value == 'keywords' or value == 'metaKeywords':
                        self.style = 'keywords'
                    elif value == 'description' or value == 'metaDescription':
                        self.style = 'profile'
            for name,value in attrs:
                if name == 'content':
                    if self.style == 'keywords':
                        self.keywords = doclex.simplesplit(value)
                    elif self.style == 'profile':
                        self.profile = value
                        #print value

    def handle_data(self, data):
        if self.current_tag == 'title':
            keys = doclex.lex(data)
            if isinstance(keys, list) and len(keys) > 0:
                for key in keys:
                    if not self.key_url.has_key(key):
                        self.key_url[key] = []
                    self.key_url[key].append(self.url)
            data = doclex.delspace(data)
            if len(data) > 0:
                collection_url_title.insert({'key':self.url, 'title':data, 'timetmp':time.time()})
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

def real_page(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        headers = response.info()
        return True
    except:
        return False

def get_page(url):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        the_page = response.read()
        headers = response.info()

        return the_page, headers
    except:
        #import traceback
        #traceback.print_exc()
        #print 'get_page error', url
        pass

def process_url(url):
    info = get_page(url)
    if info is None:
        print "url, error"
        return

    data, headers = info

    pageinfo = process_page(url, data)

    if pageinfo is None:
        print "url, process_page error"
        return

    link_list, url_profile, keywords, profile, key_url = pageinfo
    #encoding = chardet.detect(url_profile)

    try:
        #if encoding['encoding'] is not None:
        encodingdate = chardet.detect(headers['date'])
        date = unicode(headers['date'], encodingdate['encoding'])
        if profile == '':
            url_profile = unicode(url_profile, "utf-8")#encoding['encoding'])
            collection_url_profile.insert({'key':url, 'urlprofile':url_profile, 'timetmp':time.time(), 'date:':date})
        else:
            profile = unicode(profile, "utf-8")
            collection_url_profile.insert({'key':url, 'urlprofile':profile, 'timetmp':time.time(), 'date:':date})

        for key in keywords:
            collection.insert({'key':key, 'url':url, 'timetmp':time.time()})

        for key, value in key_url.iteritems():
            for url in value:
                if real_page(url):
                    collection.insert({'key':key, 'url':url, 'timetmp':time.time()})

    except:
        print "encoding error"
        pass

    return link_list

def process_page(url, data):
    if data is None:
        return

    try:
        key_url = {}
        url_profile = ""

        htmlp = htmlprocess(url)
        encoding = chardet.detect(data)
        if encoding['encoding'] is None:
            return
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
            data = doclex.delspace(data)
            if len(data) < 32:
                url_profile += data
                keys = doclex.simplesplit(data)
                if isinstance(keys, list) and len(keys) > 0:
                    for key in keys:
                        if not key_url.has_key(key):
                            key_url[key] = []
                        if url not in key_url[key]:
                            key_url[key].append(url)
            else:
                if len(data) > 100:
                    url_profile += data[0:len(data) if len(data) < 100 else 100] + "..."
                keys1 = doclex.lex(data)
                for key1 in keys1:
                    if not key_url.has_key(key1):
                        key_url[key1] = []
                    if url not in key_url[key1]:
                        key_url[key1].append(url)

        #for key, value in key_url.iteritems():
        #    for url in value:
        #        if real_page(url):
        #            collection.insert({'key':key, 'url':url, 'timetmp':time.time()})

        return htmlp.link, url_profile, htmlp.keywords, htmlp.profile, key_url

    except:
        import traceback
        traceback.print_exc()
        pass


#process_link(url)
