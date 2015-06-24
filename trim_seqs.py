#!/usr/bin/python

import argparse, sys, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-fp',help='input aligned fasta file',required=True)
	parser.add_argument('-o','--output-fp',help='output aligned fasta file',required=True)
	parser.add_argument('-s','--start-pos',help='first position to keep. 0 is first character',type=int, required=True)
	parser.add_argument('-e','--end-pos',help='last position to keep. 0 is first character',type=int, required=True)
	args = parser.parse_args()
	trim_fasta(args.input_fp, args.output_fp, args.start_pos, args.end_pos)
	
def trim_fasta(input_fp, output_fp, start_pos, end_pos):
	with open(input_fp, 'rU') as r, open(output_fp, 'wb') as w:
		this_seq = ''
		w.write(r.next())
		for line in r:
			if line.startswith('>'):
				w.write(this_seq[start_pos:end_pos] + '\n')
				this_seq = ''
				w.write(line.rstrip() + '\n')
			else:
				this_seq += line.rstrip()
		w.write(this_seq[start_pos:end_pos])
	

if __name__ == '__main__':
	main()
