import argparse, os, logging, re

from time import gmtime, strftime

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i',help='input folder', required=True)
	parser.add_argument('-o',help='output fasta folder',required=True)
	args = parser.parse_args()
	logname = 'merge_samples_hmp-%s' % strftime("%Y%m%d%H%M")
	logger = make_log(logname)
	os.mkdir(args.o)
	logger.info('made %s' % (args.o))
	get_and_write(args.o, args.i, logger)
	logger.info('Done')


										
def get_and_write(outfp, infolder, logger):
	for infp in os.listdir(infolder):
		with open(infolder + '/' + infp,'rU') as in_file:
			sampname = ''.join(infp.split('.')[0:-1])
			logger.info('now working on %s' % sampname)
			i = 0
			outfiles = {}
			for line in in_file:
				if line.startswith('>'):
					split_line = re.split('(\W+)',line)
					pl = split_line.index('primer')
					sl = split_line.index('subject')
					region = ''.join(split_line[pl + 2: sl - 1])
					outfile = '%s/%s.fasta' % (outfp, region)
					if outfile not in outfiles:
						outfiles[outfile] = open(outfile, 'ab')
						to_write = '>%s|%s %s\n' % (sampname, i, line[1:].rstrip())
					else:
						to_write = '\n>%s_%s %s\n' % (sampname, i, line[1:].rstrip())
					outfiles[outfile].write(to_write)
					i += 1
				else:
					outfiles[outfile].write('%s' % (line.rstrip()))
	for ofname,outfile in outfiles.iteritems():
		outfile.close()

def make_log(log_name, log_fp = False):
	if not log_fp:
		log_fp = log_name + '.log'
	logger = logging.getLogger(log_name)
	logger.setLevel(logging.DEBUG)
	handler = logging.FileHandler(log_fp)
	formatter = logging.Formatter('%(levelname)s: %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.info('Log initiated - %s' % strftime("%c"))
	return logger
	
	
if __name__ == '__main__':
	main()