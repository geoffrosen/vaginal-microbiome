#!/usr/bin/python

import argparse, sys, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-csv',help='the input csv that you would like to redup', required=True)
	parser.add_argument('-o','--output-csv',help='the output csv location',required=True)
	parser.add_argument('-d','--dedup-fp',help='filepath to dedup', required=True)
	args = parser.parse_args()
	redup(args.input_csv, args.output_csv, args.dedup_fp)

def redup(input_csv, output_csv, dedup_fp):
	dups = {}
	with open(dedup_fp,'rb') as dedup:
		r = csv.reader(dedup,delimiter=',')
		for [orig, dup, num] in r:
			if orig not in dups:
				dups[orig] = []
			if orig != dup:
				dups[orig].append(dup)
	with open(input_csv,'rU') as incsv, open(output_csv,'wb') as outcsv:
		header = incsv.readline()
		outcsv.write(header)
		for row in incsv:
			split_row = row.split(',')
			for other in dups[split_row[0]]:
				outcsv.write(','.join([other] + split_row[1:]))
			outcsv.write(row)


if __name__ == '__main__':
	main()
