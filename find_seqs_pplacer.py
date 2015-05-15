#!/usr/bin/python

import argparse, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-table-fp',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('--otu-names',help='comma separated otu names surrounded by quotes',required=True)
	parser.add_argument('-l','--level',help='level required',default='species')
	args = parser.parse_args()
	otu_names = args.otu_names.split(',')
	seqs = get_seqs(args.input_table_fp,otu_names,args.level)
	write_seqs(args.output_fp, seqs)

def get_seqs(input_fp, otu_names, level):
	seq_ids = []
	i = 0
	with open(input_fp,'rb') as f:
		r = csv.reader(f,delimiter=',')
		for row in r:
			if i == 0:
				i = 1
			else:
				try:
					if row[2] == level and row[1] in otu_names:
						seq_ids.append(row[0])
				except:
					print row
	return seq_ids

def write_seqs(output_fp, seq_ids):
	with open(output_fp,'wb') as f:
		w = csv.writer(f)
		for item in seq_ids:
			w.writerow([item])

if __name__ == '__main__':
	main()
