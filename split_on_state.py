#!/usr/bin/python

import argparse, csv

from classes import modify_otu

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-table-fp',help='file that is <otu id>tab<seq_id>tab<seq_id>', required=True)
	parser.add_argument('-o','--output-fp',help='output base file path',required=True)
	parser.add_argument('-c',help='class to split on',required=True)
	args = parser.parse_args()
	holder = modify_otu.OtuTable(args.input_table_fp, args.c, args.output_fp)
	holder.write_all()

if __name__ == '__main__':
	main()
