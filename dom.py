# 2014-12-18
# build by qianqians
# statemachine

class dom(object):
	def __init__(self):
		self.dom = []

	def append(self, div):
		self.dom.append(div)

	def append(self, dom):
		self.dom.append(dom)