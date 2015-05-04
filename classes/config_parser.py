import csv

class FullConfig(object):

	'''this will be the container
	   it will accept a filepath and
	   will do the work from there
	   the idea is that the config will look like:
	   command:flag option'''

	def __init__(self, config_fp):
		self.__container = {}
		with open(config_fp,'rb') as f:
			self.make_dict(f)

	def append(self, command, opts_dict):
		for title, arg in opts_dict:
			self.add_one(command, title, arg)
	
	def add_one(self, command, title, arg):
		if command not in self.__container:
			self.__container[command] = {}
		self.__container[command][title] = arg

	def has_attr(self, command):
		if command not in self.__container:
			return False
		else:
			return True

	def make_dict(self,f):
		reader = csv.reader(f, delimiter = ' ')
		tmp = {}
		for line in reader:
			cmd_flag = line[0].split(':')
			if len(line) == 1:
				line.append('')
			self.add_one(cmd_flag[0], cmd_flag[1], line[1])

	def __str__(self):
		outstr = '{\n'
		for item in self.__container:
			outstr += '%s: %s\n' % (item, self.__container[item])
		outstr += '}'
		return outstr

	def __iter__(self):
		return iter(self.__container)


	def __getitem__(self, title):
		return self.__container[title]
