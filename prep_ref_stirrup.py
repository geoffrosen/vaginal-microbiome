#!/usr/bin/python

import argparse, sys, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-s','--seqinfo',help='seqinfo from pplacer refpkg')
	parser.add_argument('-t','--taxtable',help='taxtable from pplacer refpkg')
	parser.add_argument('-r','--unaligned-ref-fasta',help='unaligned fasta',required=True)
	parser.add_argument('-o','--output-fp',help='output file path',required=True)
	parser.add_argument('--source',help='source type. options: silva, pplacer',required=True)
	args = parser.parse_args()
	if args.source == 'pplacer':
		change_ref_format(args.seqinfo,args.taxtable,args.unaligned_ref_fasta, args.output_fp)
	elif args.source == 'silva':
		arb_fasta_to_ref_format(args.unaligned_ref_fasta, args.output_fp)
	else:
		print 'unrecognized input format'
	
def arb_fasta_to_ref_format(arb_fasta_fp, output_fasta_fp):
	args_list = ['kingdom','phylum','class','order','family','genus','species']
	args_list.reverse()
	args_dict = {nom: args_list.index(nom) for nom in args_list}
	genera = {}
	with open(arb_fasta_fp,'rU') as r, open(output_fasta_fp, 'wb') as wof:
		write_arb_line(r.next(), wof)
		this_seq = ''
		for line in r:
			if line.startswith('>'):
				wof.write(this_seq + '\n')
				this_seq = ''
				write_arb_line(line, wof)
			else:
				this_seq += line.rstrip()
		wof.write(this_seq)
			

def write_arb_line(line, wof):
	split_line = line.rstrip().split(' ')
	seqname = split_line[0][1:]
	restname = ' '.join(split_line[1:]).split(';')
	restname.reverse()
	genus = restname[1]
	strain = restname[0]
	split_spec = strain.split(' ')
	if split_spec[0] == genus:
		spec = ' '.join(split_spec[1:])
	else:
		spec = strain
	wof.write('>arbsilva|' + seqname + '|genus|' + genus + '|species|' + spec + '|strain|' + strain + '|\n')
				
				
				

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
				starter = row.rstrip()
				this_info = seq_info[starter[1:]]
				spec = False
				genus = ''
				if ' '.join(this_info) in species_holder:
					spec = ' '.join(this_info)
					if this_info[0] in genus_holder:
						genus = this_info[0]
				elif len(this_info) > 1:
					for i in range(len(this_info)):
						if ' '.join(this_info[i:]) in species_holder:
							spec = ' '.join(this_info[i:])
							genus = ' '.join(this_info[0:i])
							if len(genus) == 0:
								genus = this_info[0]
				if spec:
					ender = '|genus|%s|species|%s|\n' % (genus,spec)
					outfasta.write(starter + ender)
					keep_seq = True
			elif keep_seq:
				outfasta.write(row)
	

if __name__ == '__main__':
	main()
