# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import urllib2
from LexicalAnalysis import *
from dom import  *

url = "http://jj.hbtv.com.cn/"

def get_page(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	the_page = response.read()

	return the_page

def processlink(url):
	process_page(get_page(url))


def process_data(data):

	return

def process_page(data):
	s = statemachine()
	d_stack = []
	d = dom()
	for ch in data:
		div = s.push(ch)
		if div[1] is not None:
			d.append(div)

	for it in d.dom:
		if it[0] == 'a':
			processlink(it[1])
		if it[0] == 'div' or it[0] == 'p':
			process_data(it[1])

processlink(url)