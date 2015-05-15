import csv

class OtuTable(object):
	def __init__(self, fp, split_class, base_fp, delim='\t'):
		self.__data = []
		self.__newtables = []
		split_bfp = base_fp.split('.')
		with open(fp,'rb') as f:
			r = csv.reader(f,delimiter=delim)
			for row in r:
				self.__data.append(row)
				if row[0] == split_class:
					self.__opts = self.find_cols(row)
		for item in self.__opts:
			self.__newtables.append(NewTable(item, self.__opts[item], split_bfp))
		for row in self.__data:
			self.append(row)
	
	def write_all(self):
		for nt in self.__newtables:
			nt.write()
		
	def append(self, row):
		for nt in self.__newtables:
			nt.append(row)

	def find_cols(self, header_row):
		opts = {}
		for i in range(1,len(header_row)):
			if header_row[i] not in opts:
				opts[header_row[i]] = [0]
			opts[header_row[i]].append(i)
		return opts


class NewTable(object):
	def __init__(self, name, cols, base_fp=['out','txt']):
		self.__rows = []
		self.__cols = cols
		self.__name = name
		self.__fp = ''.join(base_fp[0:-1] + [name] + ['.'] + [base_fp[-1]])

	def append(self, row):
		this_row = []
		for col in self.__cols:
			this_row.append(row[col])
		self.__rows.append(this_row)

	def write(self):
		with open(self.__fp,'wb') as w:
			ww = csv.writer(w,delimiter='\t')
			for row in self.__rows:
				ww.writerow(row)

