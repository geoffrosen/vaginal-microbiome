#!/usr/bin/python

import argparse, sys, csv, urllib2, os, hashlib

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t','--table-fp',help='table as "SRSName\tDownloadpath\tMD5"',required=True)
	parser.add_argument('-o','--output-dir',help='output directory',required=True)
	args = parser.parse_args()
	download_fs(args.output_dir,args.table_fp)
	
def download_fs(output_dir,table_fp):
	os.mkdir(output_dir)
	with open(table_fp,'rb') as f:
		r = csv.reader(f,delimiter='\t')
		fs = [filedata for filedata in r]
	for name,downloadpath,md5 in fs:
		print downloadpath
		thisfile = urllib2.urlopen(downloadpath).read()
		if hashlib.md5(thisfile).hexdigest() == md5:
			thisloc = '%s/%s.fsa.gz' % (output_dir,name)
			with open(thisloc,'wb') as f:
				f.write(thisfile)
		else:
			print 'md5 error on %s from %s' % (name,downloadpath)
	


if __name__ == '__main__':
	main()
