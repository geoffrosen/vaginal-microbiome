#!/usr/bin/python

import argparse, sys, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-s','--seqinfo',help='seqinfo from pplacer refpkg',required=True)
	parser.add_argument('-t','--taxtable',help='taxtable from pplacer refpkg',required=True)
	parser.add_argument('-r','--unaligned-ref-fasta',help='unaligned fasta',required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	args = parser.parse_args()
	change_ref_format(args.seqinfo,args.taxtable,args.unaligned_ref_fasta, args.output_fp)
	

def change_ref_format(seqinfo_fp,taxtable_fp,unaligned_fp,output_fp):
	seq_info = {}
	with open(seqinfo_fp,'rb') as f:
		r = csv.reader(f,delimiter=',')
		r.next()
		for row in r:
			if row[0] in seq_info:
				print 'non-unique ids in seqinfo'
				sys.exit(2)
			seq_info[row[0]] = row[3].split(' ')
	genus_holder = []
	species_holder= []
	with open(taxtable_fp,'rb') as f:
		r = csv.reader(f,delimiter=',')
		r.next()
		for row in r:
			if row[2] == 'genus':
				genus_holder.append(row[3])
			elif row[2] == 'species':
				species_holder.append(row[3])
	with open(unaligned_fp,'rb') as infasta, open(output_fp,'wb') as outfasta:
		keep_seq = False
		for row in infasta:
			if row[0] == '>':
				keep_seq= False
				starter = row[0:-1]
				this_info = seq_info[starter[1:]]
				spec = False
				genus = ''
				if ' '.join(this_info) in species_holder:
					spec = ' '.join(this_info)
				elif len(this_info) > 1:
					for i in range(len(this_info)):
						if ' '.join(this_info[i:]) in species_holder:
							spec = ' '.join(this_info[i:])
							genus = ' '.join(this_info[0:i])
				if spec:
					ender = '|genus|%s|species|%s|\n' % (genus,spec)
					outfasta.write(starter + ender)
					keep_seq = True
			elif keep_seq:
				outfasta.write(row)
	

if __name__ == '__main__':
	main()
