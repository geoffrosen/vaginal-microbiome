import csv

class Sequence(object):
	def __init__(self, name, species):
		self.__name = name
		self.__species = species
	def spec(self):
		return self.__species

class AllSequences(object):
	def __init__(self, tax_fp):
		self.__seqs = {}
		with open(tax_fp, 'rb') as f:
			r = csv.reader(f,delimiter=',')
			for row in r:
				if row[2] == 'species':
					self.__seqs[row[0]] = Sequence(row[0],row[1])
	def __getitem__(self, seq):
		try:
			return self.__seqs[seq]
		except:
			return Sequence('unclassified','unclassified')

class OTU(object):
	def __init__(self, name):
		self.__name = name
		self.__seqs = []
		self.__counts = {}

	def append(self, list_to_append, all_sequences):
		for item in list_to_append:
			self.__seqs.append(all_sequences[item])

	def count(self):
		self.__counts = {}
		for seq in self.__seqs:
			spec = seq.spec()
			if spec not in self.__counts:
				self.__counts[spec] = 0
			self.__counts[spec] += 1

	def return_counts(self):
		self.count()
		return dict(self.__counts)

class AllOTUS(object):
	def __init__(self, otus_fp, all_sequences):
		self.__otus = {}
		with open(otus_fp,'rb') as f:
			r = csv.reader(f,delimiter='\t')
			for row in r:
				this = OTU(row[0])
				this.append(row[1:],all_sequences)
				self.__otus[row[0]] = this
	def __getitem__(self,otu):
		return self.__otus[otu]

class Function(object):
	def __init__(self, name):
		self.__name = name
		self.__otus = []
		self.__counts = {}
	def add_otu(self, otu_name, all_otus):
		self.__otus.append(all_otus[otu_name])
	def count(self):
		for otu in self.__otus:
			for spec, count in otu.return_counts().iteritems():
				if spec not in self.__counts:
					self.__counts[spec] = 0
				self.__counts[spec] += 1
	def return_array(self):
		self.count()
		out = []
		for spec,count in self.__counts.iteritems():
			out.append([self.__name,spec,count])
		return out

class AllFunctions(object):
	def __init__(self, functions_fp, all_otus):
		self.__functions = {}
		with open(functions_fp,'rb') as f:
			r = csv.reader(f,delimiter='\t')
			r.next()
			for row in r:
				self.append(row[0], row[2], all_otus)
	def append(self, function_name, otu_id, all_otus):
		if function_name not in self.__functions:
			self.__functions[function_name] = Function(function_name)
		self.__functions[function_name].add_otu(otu_id, all_otus)

	def export(self, out_fp):
		with open(out_fp,'wb') as f:
			w = csv.writer(f,delimiter='\t')
			for fun_name, function in self.__functions.iteritems():
				for row in function.return_array():
					w.writerow(row)
			

