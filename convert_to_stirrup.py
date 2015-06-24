#!/usr/bin/python

import argparse, sys, re, os

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f','--fasta-fp',help='input fasta file')
    parser.add_argument('-d','--directory',help='directory if you want this to be done on a directory',default=False)
    parser.add_argument('-o','--output-fp',help='output file path',required=True)
    parser.add_argument('--hmp-data',help='mark for HMP data',action='store_true',default=False)
    parser.add_argument('--hmp-region',help='HMP region. Comma separated',type=str,default='V1-V3')
    parser.add_argument('--hmp-regexp',help='regexp pattern for hmp',type=str,default='(\w+?)=([\w-]*)')
    parser.add_argument('-r','--regexp-pat',help='regexp pattern for sample,seq',default='>(.+)_(\w+) .*')
    args = parser.parse_args()
    if args.directory:
        input_files = [args.directory + '/' + fp for fp in os.listdir(args.directory)]
        output_files = [args.output_fp + '/' + fp for fp in os.listdir(args.directory)]
        os.mkdir(args.output_fp)
        for i in range(len(input_files)):
            if args.hmp_data:
                deal_with_hmp(input_files[i], output_files[i], args.hmp_regexp, args.hmp_region.split(','))
            else:
                change_input_format(input_files[i], output_files[i],args.regexp_pat)
    else:
        if args.hmp_data:
            deal_with_hmp(args.fasta_fp, args.output_fp, args.hmp_regexp, args.hmp_region.split(','))
        else:
            change_input_format(args.fasta_fp,args.output_fp,args.regexp_pat)

def deal_with_hmp(fasta_fp,output_fp,regexp_pat,regions):
    regexp_comp = re.compile(regexp_pat)
    with open(fasta_fp,'rb') as r, open(output_fp,'wb') as w:
        i = 1
        for line in r:
            if line.startswith('>'):
                split_line = dict(regexp_comp.findall(line))
                if split_line['primer'] not in regions:
                    isrightregion = False
                    continue
                isrightregion = True
                subj = split_line['subject']
                samp = split_line['sample']
                seq = i
                w.write('>%s_%s|%s\n' % (subj,samp,seq))
                i += 1
            elif isrightregion:
                w.write(line)

def change_input_format(fasta_fp,output_fp,regexp_pat):
    regexp_comp = re.compile(regexp_pat)
    with open(fasta_fp,'rb') as r, open(output_fp,'wb') as w:
        for line in r:
            if line.startswith('>'):
                try:
                    samp, seq = regexp_comp.search(line).groups()
                except:
                    print 'Error on line'
                    print line
                    print 'You may need to change the regexp_pattern. It is currently "%s"' % regexp_pat
                    sys.exit(2)
                w.write('>%s|%s\n' % (samp,seq))
            else:
                w.write(line)
	

if __name__ == '__main__':
	main()
