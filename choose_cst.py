import argparse, csv, sys

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i',help='otu table file path', required=True)
	parser.add_argument('--output-otu-table',help='output otu table fp', default=False)
	parser.add_argument('--output-mapping-file',help='output mapping fp', default=False)
	parser.add_argument('--cst-definers',help='partial feature name whose dominance defines the cst. comma separated and in the same order as name',required=True)
	parser.add_argument('--cst-names',help='cst names in matching order to the cst definers. comma separated',default=False)
	parser.add_argument('-d',help='dominance level', type=float, default=.5)
	parser.add_argument('-f',help='fallback/catchall name',type=str,default='not otherwise defined')
	args = parser.parse_args()
	cst_definers = args.cst_definers.split(',')
	if not args.cst_names:
		cst_names = cst_definers
	else:
		cst_names = args.cst_names.split(',')
	if len(cst_definers) != len(cst_names):
		print 'cst definers not the same length as cst names'
		sys.exit(2)
	if not args.output_otu_table:
		oot = ''.join(args.i.split('.')[0:-1]) + '_with_csts.tsv'
	else:
		oot = args.output_otu_table
	if not args.output_mapping_file:
		omf = ''.join(args.i.split('.')[0:-1]) + '.map'
	else:
		omf = args.output_mapping_file
	define_csts(args.i, args.d, cst_definers, cst_names, args.f, omf, oot)
	
	

def define_csts(input_fp, dominance_level, cst_definers, cst_names, fallback_name, map_fp, otu_table_fp):
	dominance_level = float(dominance_level)
	feats = []
	data_table = []
	with open(input_fp, 'rU') as f:
		r = csv.reader(f, delimiter='\t')
		header = r.next()
		for row in r:
			feats.append(row[0])
			data_table.append(row[1:])
	ct = col_totals(data_table)
	csts = {samp: [] for samp in header[1:]}
	for i in range(len(cst_definers)):
		row_definers = get_row_definers(cst_definers[i], feats)
		for row_num in row_definers:
			this_row = data_table[row_num]
			for j in range(len(this_row)):
				if float(this_row[j]) > (dominance_level * ct[j]):
					csts[header[j]].append(cst_names[i])
	for samp,cst in csts.iteritems():
		cst.append(fallback_name)
	with open(map_fp,'wb') as f:
		w = csv.writer(f,delimiter='\t')
		w.writerow(['#SampleID','CST'])
		for samp,cst in csts.iteritems():
			w.writerow([samp,cst[0]])
	with open(otu_table_fp,'wb') as f:
		w = csv.writer(f,delimiter='\t')
		secrow = [''] + [csts[samp][0] for samp in header[1:]]
		w.writerow(header)
		w.writerow(secrow)
		for i in range(len(data_table)):
			w.writerow([feats[i]] + data_table[i])


def get_row_definers(definer_substring, feats):
	rownums = []
	for i in range(len(feats)):
		if feats[i].find(definer_substring) != -1:
			rownums.append(i)
	return rownums

def col_totals(data_table):
	tots = map(float, data_table[0])
	for row in data_table[1:]:
		this_row = map(float, row)
		for i in range(len(this_row)):
			tots[i] += this_row[i]
	return tots			
	
if __name__ == '__main__':
	main()