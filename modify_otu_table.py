#!/usr/bin/python

import argparse, csv, sys

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-table-fp',help='the input table that you wish to add the classes to', required=True)
	parser.add_argument('-m','--map-fp',help='the tab delineated map with top line as header', required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('-s','--start-id',help='the id as labelled in the input file', required=True)
	parser.add_argument('-e','--end-id',help='the id you want in the output file',required=True)
	parser.add_argument('-c','--class-name',help='the class you want to be used',required=True)
	parser.add_argument('-l','--level',help='change depth of taxonomy',default=-1,type=int)
	parser.add_argument('-n','--normalize',help='normalize by column',action='store_true',default=False)
	#need to think through how bottom will work with level. maybe can only have one
	parser.add_argument('-b','--bottom',help='will only return the bottom listing (with above heirarchy)',default=False,action='store_true')
	parser.add_argument('--in-splitter',help='the splitter as the files come in',default=';')
	parser.add_argument('--out-splitter',help='the splitter you want as the files go out',default='|')
	parser.add_argument('--otu-min',help='the minimum (as a decimal for normalize or count number) for an otu to be included',default=float(0),type=float)
	args = parser.parse_args()
	with open(args.input_table_fp,'rb') as r, open(args.map_fp,'rb') as m,  open(args.output_fp,'wb') as w:
		rr = csv.reader(r,delimiter='\t')
		ww = csv.writer(w,delimiter='\t')
		rm = csv.reader(m,delimiter='\t')
		mapper = {}
		i = 0
		for row in rm:
			if i == 0:
				start_col = row.index(args.start_id)
				new_col = row.index(args.end_id)
				class_col = row.index(args.class_name)
				i = 1
			else:
				mapper[row[start_col]] = (row[new_col],row[class_col])
		i = 0
		class_row = [args.class_name]
		new_row = [args.end_id]
		if args.level:
			holder = Family(args.out_splitter)
		for row in rr:
			if i == 0:
				for item in row[1:]:
					try:
						(this_new_id, this_class) = mapper[item]
					except:
						if len(row) - row.index(item) > 2:
							print 'failed because mapper didn\'t contain %s' % item
							sys.exit(2)
						else:
							print 'failed on %s' % item
							continue
					new_row.append(this_new_id)
					class_row.append(this_class)
				ww.writerow(class_row)
				ww.writerow(new_row)
				i = 1
			else:
				if args.level:
					this_name = row[-1].split(args.in_splitter)
					this_name = filter(None, this_name)
					for j in range(len(this_name)):
						this_name[j] = this_name[j].strip()
					this_name = args.out_splitter.join(this_name)
					holder.append(this_name,row[1:-1])
				else:
					ww.writerow(row)
		if args.level:
			if args.normalize:
				otu_min = args.otu_min * float(len(class_row) - 1)
			else:
				otu_min = args.otu_min * float(holder.sum_counts())
			for row in holder.out(normalize=args.normalize,level=args.level,minimum=otu_min,bottom=args.bottom):
				ww.writerow(row)




class Clade(object):
	def __init__(self, splitter):
		self.__sub = {}
		self.__counts = None
		self.__splitter = splitter
		pass

	def append(self, name, incounts):
		if not self.__counts:
			self.__counts = list(map(float,incounts))
		else:
			for i in range(len(incounts)):
				self.__counts[i] += float(incounts[i])
		split_name = name.split(self.__splitter)
		self.__name = split_name[0]

		if len(split_name) > 1:
			if split_name[1] not in self.__sub:
				self.__sub[split_name[1]] = Clade(self.__splitter)
			self.__sub[split_name[1]].append(self.__splitter.join(split_name[1:]),incounts)

	def out_array(self,par=False,normalize=False,parcounts=False,level=-1,minimum=0,bottom=False):
		if level == 0:
			return []
		if par:
			my_name = '%s%s%s' % (par,self.__splitter,self.__name)
		else:
			my_name = self.__name
		if normalize:
			if not parcounts:
				parcounts = self.__counts
			my_counts = []
			#I think there is an easy way to do this in numpy
			for i in range(len(self.__counts)):
				if parcounts[i] != 0:
					my_counts.append(float(self.__counts[i])/float(parcounts[i]))
				else:
					#test for error
					if self.__counts[i] != 0:
						raise NameError('Error on division %s count was %s while %s count was %' % (self.__name, self.__counts[i], 'parent', parcounts[i]))
					else:
						my_counts.append(float(0))
						
		else:
			my_counts = self.__counts
		if sum(my_counts) < minimum:
			return []
		out = [[my_name] + my_counts]
		if parcounts:
			pass_counts = list(parcounts)
		else:
			pass_counts = list(self.__counts)
		if not bottom:
			for sub in self.__sub:
				out += self.__sub[sub].out_array(my_name,normalize,list(pass_counts),level=level-1,minimum=minimum,bottom=bottom)
		return out
		
		
		


class Family(object):
	def __init__(self, splitter):
		self.__sub = {}
		self.__splitter = splitter
		self.__counts = None

	def append(self, name, incounts):
		child_name = name.split(self.__splitter)[0]
		if child_name not in self.__sub:
			self.__sub[child_name] = Clade(self.__splitter)
		self.__sub[child_name].append(name,incounts)
		if not self.__counts:
			self.__counts = list(map(float,incounts))
		else:
			for i in range(len(incounts)):
				self.__counts[i] += float(incounts[i])

	def sum_counts(self):
		return sum(self.__counts)

	def out(self,normalize=False,level=-1,minimum=float(0),bottom=False):
		out = []
		for sub in self.__sub:
			out += self.__sub[sub].out_array(normalize=normalize,parcounts=list(self.__counts),level=level,minimum=minimum,bottom=bottom)
		return out

if __name__ == '__main__':
	main()
