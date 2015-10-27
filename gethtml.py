# -*- coding: UTF-8 -*-
# darkforce
# create at 2015/10/11
# autor: qianqians

import urllib2
from LexicalAnalysis import *
from dom import  *

url = "http://jj.hbtv.com.cn/"

def process_data(data):
	return

def get_page(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	the_page = response.read()

	return the_page

def process_link(url):
	process_page(get_page(url))

def process_page(data):
	s = statemachine()
	d_stack = []
	d = dom()
	for ch in data:
		div = s.push(ch)
		if div is not None:
			d.append(div)

	for it in d.dom:
		if it[0] == 'a':
			process_link(it[1])
		elif it[0] == 'p':
			process_data(it[1])

process_link(url)