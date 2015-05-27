#!/usr/bin/python

import argparse, csv, sys
from operator import itemgetter

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-a','--a-csv',help='one of the files to test', required=True)
	parser.add_argument('-b','--b-csv',help='one of the files to test', required=True)
	args = parser.parse_args()
	test_on_lines(args.a_csv,args.b_csv)

def test_on_lines(a_fp, b_fp):
	a = []
	b = []
	with open(a_fp,'rb') as f:
		for line in f:
			a.append(line)
	with open(b_fp,'rb') as f:
		for line in f:
			b.append(line)
	oia = []
	oib = []
	for line in a:
		if line not in b:
			oia.append(line)
	for line in b:
		if line not in a:
			oib.append(line)
	if len(oia) == 0 and len(oib) == 0:
		print 'The files appear to be the same line by line'
	else:
		print 'An example of %s: %s' % (a_fp, a[int(len(a)/2)])
		print 'An example of %s: %s' % (b_fp, b[int(len(b)/2)])


if __name__ == '__main__':
	main()
