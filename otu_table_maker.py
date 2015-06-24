#!/usr/bin/python

import argparse, csv, sys

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-csv',help='the reduped file of taxonomy with one header line', required=True)
	parser.add_argument('-o','--output',help='the output otu table location',required=True)
	parser.add_argument('-r','--rank',help='rank of OTU table', default='species')
	parser.add_argument('-s','--splitter',help='what to split on sequence names on', default='_')
	parser.add_argument('-l','--likelihood',help='minimum likelihood', default=0.8, type=float)
	parser.add_argument('--input-type',help='input from what kind of pipeline. options: pplacer, stirrups, qiime',type=str, default='pplacer')
	args = parser.parse_args()
	make_otu_table(args.input_csv, args.output, args.rank, args.splitter, args.likelihood, args.input_type)

def holder_adjuster(tax_name, sample_name, tax_holder, sample_holder):
	if tax_name not in tax_holder:
		tax_holder[tax_name] = {}
	if sample_name not in tax_holder[tax_name]:
		tax_holder[tax_name][sample_name] = 0
	tax_holder[tax_name][sample_name] += 1
	if sample_name not in sample_holder:
		sample_holder.append(sample_name)

def make_otu_table(input_fp, output_fp, rank, splitter, min_lik, input_from):
	tax_holder = {}
	sample_holder = []
	if input_from == 'pplacer':
		with open(input_fp, 'rU') as f:
			r = csv.reader(f, delimiter=',')
			header = r.next()
			sni = header.index('name')
			ri = header.index('rank')
			tni = header.index('tax_name')
			li = header.index('likelihood')
			for line in r:
				if line[ri] == rank and float(line[li]) >= min_lik:
					tax_name = line[tni]
					sample_name = line[sni].split(splitter)[0]
					holder_adjuster(tax_name, sample_name, tax_holder, sample_holder)
	elif input_from == 'qiime':
		with open(input_fp, 'rU') as f:
			r = csv.reader(f, delimiter='\t')
			header = r.next()
			sni = 0
			tni = 1
			li = 2
			for line in r:
				if float(line[li]) >= min_lik:
					tax_name = line[tni]
					sample_name = line[sni].split(splitter)[0]
					holder_adjuster(tax_name, sample_name, tax_holder, sample_holder)
	elif input_from == 'stirrups':
		samps = []
		with open(input_fp, 'rU') as f:
			r = csv.reader(f, delimiter='|',quoting=csv.QUOTE_NONE)
			li = 4
			for line in r:
				if float(line[4]) >= (min_lik * 100):
					sample_name = line[0]
					##build list of seqs
					seq_name = line[1]
					concat_name = sample_name + '_' + seq_name
					samps.append(concat_name)
					##
					tax_name = line[2]
					holder_adjuster(tax_name, sample_name, tax_holder, sample_holder)
				else:
					sample_name = line[0]
					tax_name = 'unidentified'
					holder_adjuster(tax_name, sample_name, tax_holder, sample_holder)
		## Check for duplicated sequences
		if len(samps) != len(set(samps)):
			print 'Some seqs appear duplicated'
			sys.exit(2)
	else:
		raise TypeError('Unknown input file type')
	header = ['#OTU'] + sample_holder + ['Consensus Lineage']
	otu_table = [header]
	i = 0
	for tax_name, tax_info in tax_holder.iteritems():
		this_row = [i]
		for sample_name in sample_holder:
			try:
				this_row.append(tax_info[sample_name])
			except:
				this_row.append(0)
		this_row.append(tax_name)
		otu_table.append(this_row)
		i += 1
	with open(output_fp, 'wb') as f:
		w = csv.writer(f,delimiter='\t')
		for row in otu_table:
			w.writerow(row)
		


if __name__ == '__main__':
	main()
