#!/usr/bin/python

import argparse, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-table-fp',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('--otu-ids',help='comma separated otu ids surrounded by quotes',required=True)
	parser.add_argument('--input-type',help='input type. options: qiime, stirrups',default='qiime')
	parser.add_argument('--fasta_fp',help='fasta filepath to get otus from',default=False)
	parser.add_argument('--keep-opp',help='if you want to keep the opposite sequences',action='store_true',default=False)
	args = parser.parse_args()
	if args.input_type == 'qiime':
		cnum_tax = 0
		delim = '\t'
	elif args.input_type == 'stirrups':
		cnum_tax = 2
		delim = '|'
	otu_ids = args.otu_ids.split(',')
	seqs = get_seqs(args.input_table_fp,otu_ids, delim,cnum_tax,args.input_type)
	if not args.fasta_fp:
		write_seqs(args.output_fp, seqs)
	else:
		get_and_write(args.fasta_fp, args.output_fp, set(seqs), args.keep_opp)
	
def get_and_write(fasta_fp, output_fp, seqs, keep_opp):
	with open(fasta_fp,'rU') as r, open(output_fp, 'wb') as w:
		thisseq = ''
		for line in r:
			if line.startswith('>'):
				seqid = line.split()[0][1:]
				if len(thisseq) > 0:
					w.write(thisseq + '\n')
					thisseq = ''
					inseq = False
				if (not keep_opp) and (seqid in seqs):
					w.write(line.rstrip() + '\n')
					inseq = True
				elif (keep_opp) and (seqid not in seqs):
					w.write(line.rstrip() + '\n')
					inseq = True
				else:
					inseq = False
			elif inseq == True:
				thisseq += line.rstrip()
		if len(thisseq) > 0:
			w.write(thisseq)
					

def get_seqs(input_fp, otu_ids, delim, cnum_tax, input_type):
	seq_ids = []
	with open(input_fp,'rb') as f:
		r = csv.reader(f,delimiter=delim)
		for row in r:
			if row[cnum_tax] in otu_ids:
				if input_type == 'qiime':
					seq_ids += row[1:]
				elif input_type == 'stirrups':
					seq_ids.append(row[0] + '|' + row[1])
	return seq_ids

def write_seqs(output_fp, seq_ids):
	with open(output_fp,'wb') as f:
		w = csv.writer(f)
		for item in seq_ids:
			w.writerow([item])

if __name__ == '__main__':
	main()
