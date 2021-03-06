'''This will have the class that will execute the commands
   It will be a container, but will also have a method for
   executing and logging.'''

import time, subprocess

class Command(object):

	'''inputs:
	   title as str
	   description as str
	   command as str
	   named_opts as dictionary
	   positional_opts as array
	'''

	def __init__(self, title, description, command, named_opts, positional_opts):
		self.__title = title
		self.__description = description
		self.__command = command
		self.__named_opts = named_opts
		self.__positional_opts = positional_opts
		self.__built_command = self.build_command()

	def build_command(self):
		starter = [self.__command]
		for name, datum in self.__named_opts.iteritems():
			starter += [str(name), str(datum)]
		starter += [str(pos_opt) for pos_opt in self.__positional_opts]
		return ' '.join(starter)

	def execute(self, logger):
		logger.info('Now performing: %s' % self.__title)
		logger.info('Details: %s' % self.__description)
		logger.info('Command as sent: %s' % self.__built_command)
		start_time = time.time()
		try:
			run_res = subprocess.check_output(self.__built_command, shell=True, stderr = subprocess.STDOUT)
			logger.info(run_res)
		except subprocess.CalledProcessError as e:
			logger.warning('Error on %s' % e.cmd)
			logger.warning('Details: %s' % e.output)
		end_time = time.time()
		logger.info('Runtime was %0.9f s' % (end_time-start_time))

	def __str__(self):
		out = 'Title: %s\n'\
		'Description: %s\n'\
		'Command: %s\n' % (self.__title, self.__description, self.__built_command)
		return out

def test():
	print 'hello'

class MultipleCommands(object):

	def __init__(self):
		self.__commands = []

	def execute_all(self, logger, delete = True):
		for item in self.__commands:
			item.execute(logger)
		if delete == True:
			self.__commands = []

	def append(self, title, description, command, named_opts, positional_opts):
		#make sure positional_opts has one item
		if isinstance(named_opts, dict) and not isinstance(positional_opts[0], list):
			self.add_single(title, description, command, named_opts, positional_opts)
		elif not isinstance(named_opts, dict) and not isinstance(positional_opts[0], list):
			self.add_iter_on_named(title, description, command, named_opts, positional_opts)
		elif isinstance(named_opts, dict) and isinstance(positional_opts[0], list):
			self.add_iter_on_positional(title, description, command, named_opts, positional_opts)
		elif not isinstance(named_opts, dict) and isinstance(positional_opts[0], list):
			self.add_iter_on_both(title, description, command, named_opts, positional_opts)
		else:
			raise TypeError('Make sure that named_opts is a dictionary or a list of dictionaries and positional_opts is a list or list of lists')

	def add_iter_on_both(self, title, description, command, named_opts, positional_opts):
		for item in positional_opts:
			self.add_iter_on_named(title, description, command, named_opts, item)

	def add_iter_on_positional(self, title, description, command, named_opts, positional_opts):
		for item in positional_opts:
			self.add_single(title, description, command, named_opts, item)

	def add_iter_on_named(self, title, description, command, named_opts, positional_opts):
		for item in named_opts:
			self.add_single(title, description, command, item, positional_opts)

	def add_single(self, title, description, command, named_opts, positional_opts):
		self.__commands.append(Command(title, description, command, named_opts, positional_opts))

	def __str__(self):
		outstr = ''
		for item in self.__commands:
			outstr += '%s\n' % item
		return outstr
