import argparse, os, logging

from time import gmtime, strftime

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i',help='input folder', required=True)
	parser.add_argument('-o',help='output fasta file',required=True)
	args = parser.parse_args()
	logname = 'merge_for_stirrups-%s' % strftime("%Y%m%d%H%M")
	logger = make_log(logname)
	get_and_write(args.o, args.i, logger)
	logger.info('Done')


										
def get_and_write(outfp, infolder, logger):
	with open(outfp, 'wb') as out_file:
		for infp in os.listdir(infolder):
			with open(infolder + '/' + infp,'rU') as in_file:
				sampname = ''.join(infp.split('.')[0:-1])
				logger.info('now working on %s' % sampname)
				i = 0
				for line in in_file:
					if line.startswith('>'):
						out_file.write('>%s|%s\n' % (sampname, i))
						i += 1
					else:
						out_file.write(line.rstrip() + '\n')
		
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