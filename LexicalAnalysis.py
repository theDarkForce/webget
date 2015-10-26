# 2014-12-18
# build by qianqians
# statemachine

class statemachine(object):
	getdivtype = 2
	waitend = 4
	notes = 5
	end = 6

	indiv = 1
	instr1 = 3
	instr2 = 7
	instr3 = 8

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
			self.state = statemachine.getdivtype

			if self.strstate == statemachine.indiv:
				if self.current_div is not None:
					self.stack_div.append(self.current_div)
					self.divtype = ""
					self.endtype = ""

				self.current_div = ""
		elif ch == ">":
			if self.strstate != statemachine.instr1 and self.strstate != statemachine.instr2 and self.strstate != statemachine.instr3:
				if ((self.divtype == self.endtype or self.endtype == "")) or self.state == statemachine.notes:
					div = self.current_div + ch
					if len(self.stack_div) == 0:
						self.current_div = None
					else:
						self.current_div = self.stack_div.pop()
					self.state = statemachine.end
		elif ch == "/" and self.strstate != statemachine.instr1 and self.strstate != statemachine.instr2 and self.strstate != statemachine.instr3:
			self.state = statemachine.waitend
		elif ch == "\"":
			if self.strstate == statemachine.indiv:
				self.strstate = statemachine.instr1
			elif self.strstate == statemachine.instr1:
				self.strstate = statemachine.indiv
		elif  ch == "'":
			if self.strstate == statemachine.indiv:
				self.strstate = statemachine.instr2
			elif self.strstate == statemachine.instr2:
				self.strstate = statemachine.indiv
		elif ch == " " and self.strstate != statemachine.instr1 and self.strstate != statemachine.instr2 and self.strstate != statemachine.instr3:
			self.state = statemachine.indiv
		elif ch == "!":
			if self.tmp == "<":
				if self.state == statemachine.indiv or self.state == statemachine.getdivtype:
					self.state = statemachine.notes

		self.tmp = ch
		if self.current_div is not None:
			self.current_div += ch
		if self.state == statemachine.getdivtype and ch != '<':
			self.divtype += ch
		if self.state == statemachine.waitend and ch != '>':
			self.endtype += ch
		if len(self.stack_div) != 0:
			self.stack_div[-1] += ch

		return div


