#!/usr/bin/python

import argparse, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-otus-file',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-otus-file',help='output file path',required=True)
	parser.add_argument('--seq-ids-file',help='seq_ids one per line',required=True)
	args = parser.parse_args()
	seqs = get_seqs(args.seq_ids_file)
	write_otus(args.input_otus_file,args.output_otus_file, seqs)

def get_seqs(otu_ids_fp):
	seq_ids = []
	with open(otu_ids_fp,'rb') as f:
		r = csv.reader(f,delimiter='\t')
		for row in r:
			seq_ids.append(row[0])
	return seq_ids

def write_otus(input_fp,output_fp, seq_ids):
	with open(input_fp,'rb') as r, open(output_fp,'wb') as w:
		rr = csv.reader(r,delimiter='\t')
		ww = csv.writer(w,delimiter='\t')
		for row in rr:
			out = [seq_id for seq_id in row if seq_id not in seq_ids]
			ww.writerow(out)
			

if __name__ == '__main__':
	main()
