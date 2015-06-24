#!/usr/bin/python

import argparse, sys, csv

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i','--input-otu-table',help='file path to otu table',required=True)
	parser.add_argument('-f','--feature',help='feature of interest',required=True)
	parser.add_argument('-l','--level',help='level required to count as positive',type=float,default=1.0)
	parser.add_argument('-r','--relative',help='if level is relative',action='store_true',default=False)
	parser.add_argument('-m','--mapping-fp',help='mapping file path',required=True)
	parser.add_argument('-c','--column',help='column name in mapping file to check',required=True)
	parser.add_argument('-p','--positive-name',help='what it says in the column if true positive',required=True)
	args = parser.parse_args()
	get_stats(args.input_otu_table, args.mapping_fp, args.feature, args.level, args.relative, args.column, args.positive_name)

def get_stats(otu_table_fp, mapping_fp, feature, level, relative, column, positive_name):
	with open(otu_table_fp,'rU') as f:
		r = csv.reader(f,delimiter='\t')
		otu_table = [row for row in r]
	mapping_dict = get_mapping(mapping_fp)
	feat_dict = get_feature(otu_table, feature)
	true_pos = 0.0
	true_neg = 0.0
	false_pos = 0.0
	false_neg = 0.0
	if relative:
		sums_dict = get_col_sums(otu_table)
	for sample_name, feat_count in feat_dict.iteritems():
		if relative:
			test_decision = (feat_count/sums_dict[sample_name]) >= level
		else:
			test_decision = feat_count >= level
		true_decision = mapping_dict[sample_name][column] == positive_name
		if test_decision:
			if true_decision:
				true_pos += 1
			else:
				false_pos += 1
		else:
			if true_decision:
				false_neg += 1
			else:
				true_neg += 1
	out = [['true pos',str(true_pos)],['true neg', str(true_neg)], ['false pos',str(false_pos)], ['false neg', str(false_neg)]]
	out.append(['sensitivity',str(true_pos/(true_pos + false_neg))])
	out.append(['specificity',str(true_neg/(true_neg + false_pos))])
	out.append(['precision',str(true_pos/(true_pos + false_pos))])
	out.append(['accuracy',str((true_pos + true_neg)/(true_pos + true_neg + false_pos + false_neg))])
	out.append(['F1 score',str((2*true_pos)/(2*true_pos + false_pos + false_neg))])
	for item in out:
		print ': '.join(item)
	
	
def get_mapping(mapping_fp):
	with open(mapping_fp,'rU') as f:
		r = csv.reader(f,delimiter='\t')
		header = r.next()
		mapper = {row[0]: dict(zip(header,row)) for row in r}
	return mapper

def get_col_sums(otu_table):
	sums = []
	for item in otu_table[1][1:]:
		sums.append(float(item))
	for row in otu_table[2:]:
		for i in range(1,len(row)):
			sums[i] += float(row[i])
	return dict(zip(otu_table[0][1:],sums))

def get_feature(otu_table, feature):
	for row in otu_table:
		if row[0] == feature:
			return dict(zip(otu_table[0][1:], map(float, row[1:])))
		

if __name__ == '__main__':
	main()
