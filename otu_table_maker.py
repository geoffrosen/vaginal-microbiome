#!/usr/bin/python

import argparse, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-csv',help='the reduped file of taxonomy with one header line', required=True)
	parser.add_argument('-o','--output',help='the output otu table location',required=True)
	parser.add_argument('-r','--rank',help='rank of OTU table', default='species')
	parser.add_argument('-s','--splitter',help='what to split on sequence names on', default='_')
	parser.add_argument('-l','--likelihood',help='minimum likelihood', default=0.8, type=float)
	args = parser.parse_args()
	make_otu_table(args.input_csv, args.output, args.rank, args.splitter, args.likelihood)

def make_otu_table(input_fp, output_fp, rank, splitter, min_lik):
	tax_holder = {}
	sample_holder = []
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
				if tax_name not in tax_holder:
					tax_holder[tax_name] = {}
				if sample_name not in tax_holder[tax_name]:
					tax_holder[tax_name][sample_name] = 0
				tax_holder[tax_name][sample_name] += 1
				if sample_name not in sample_holder:
					sample_holder.append(sample_name)
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
