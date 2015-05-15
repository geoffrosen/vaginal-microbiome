#!/usr/bin/python

import argparse, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-table-fp',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('--otu-ids',help='comma separated otu ids surrounded by quotes',required=True)
	args = parser.parse_args()
	otu_ids = args.otu_ids.split(',')
	seqs = get_seqs(args.input_table_fp,otu_ids)
	write_seqs(args.output_fp, seqs)

def get_seqs(input_fp, otu_ids):
	seq_ids = []
	with open(input_fp,'rb') as f:
		r = csv.reader(f,delimiter='\t')
		for row in r:
			if row[0] in otu_ids:
				seq_ids += row[1:]
	return seq_ids

def write_seqs(output_fp, seq_ids):
	with open(output_fp,'wb') as f:
		w = csv.writer(f)
		for item in seq_ids:
			w.writerow([item])

if __name__ == '__main__':
	main()
