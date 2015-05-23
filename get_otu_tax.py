#!/usr/bin/python

import argparse, csv, sys

import classes.seq as seqs

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-otu-table-fp',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('-t','--taxonomy-fp',help='taxonomy file path (from pplacer)',required=True)
	parser.add_argument('-m','--metagenome-contributions-fp',help='metagenome contributions file path',required=True)
	args = parser.parse_args()
	print 'about to start getting taxonomy'
	all_sequences = seqs.AllSequences(args.taxonomy_fp)
	print 'done with taxonomy collection. now on to otu finding'
	all_otus = seqs.AllOTUS(args.input_otu_table_fp, all_sequences)
	print 'done with otu finding. now on to function finding'
	all_functions = seqs.AllFunctions(args.metagenome_contributions_fp, all_otus)
	print 'done with function finding. now on to file writing'
	all_functions.export(args.output_fp)

if __name__ == '__main__':
	main()
