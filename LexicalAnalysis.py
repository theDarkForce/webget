# 2014-12-18
# build by qianqians
# statemachine

class statemachine(object):
	getdivtype = 2
	waitend = 4
	notes = 5
	end = 6

	indiv = 1
	instr = 3

	def __init__(self):
		self.stack_div = []
		self.current_div = None
		self.state = statemachine.indiv
		self.strstate = statemachine.indiv
		self.divtype = ""
		self.endtype = ""
		self.tmp = ""
		#self.state

	def push(self, ch):
		div = None

		if ch == "<":
			self.state == statemachine.getdivtype

			if self.strstate == statemachine.indiv:
				if self.current_div is not None:
					self.stack_div.append(self.current_div)
					self.divtype = ""
					self.endtype == ""
				else:
					self.current_div = ""
		elif ch == ">":
			if self.strstate != statemachine.instr:
				if (self.state == statemachine.waitend and (self.divtype == self.endtype or self.endtype == "")) or self.state == statemachine.notes:
					div = self.current_div + ch
					if len(self.stack_div) == 0:
						self.current_div = None
					else:
						self.current_div = self.stack_div.pop()
					self.state = statemachine.end
		elif ch == "/" and self.state != statemachine.instr:
			self.state == statemachine.waitend
		elif ch == "\"" or ch == "'":
			if self.strstate == statemachine.indiv:
				self.strstate = statemachine.instr
			else:
				self.strstate = statemachine.indiv
		elif ch == " ":
			self.state == statemachine.getdivtype
		elif ch == "!":
			if self.tmp == "<":
				if self.state == statemachine.indiv:
					self.state = statemachine.notes

		self.tmp = ch
		if self.current_div is not None:
			self.current_div += ch
		if self.state == statemachine.getdivtype:
			self.divtype += ch
		if self.state == statemachine.waitend:
			self.endtype += ch
		if len(self.stack_div) != 0:
			self.stack_div[-1] += ch

		return div


