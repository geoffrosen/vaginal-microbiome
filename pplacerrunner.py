#!/usr/bin/env python

"""this will be the runner file"""
__author__ = 'Geoff Rosen'
__email__ = 'geoff.rosen <at> gmail.com'
__status__ = 'development'
__description__ = '''This program will help to run pplacer \n\
		from start to end'''

import argparse, logging, time, argparse, sys

from classes import update_refpkg as cur

def main(argv):
	logger = make_log('pplacer-runner', 'pplacer-runner.log')
	logger.info('Initiated with command: %s' % ' '.join(argv))
	parser = argparse.ArgumentParser(description = __description__)
	parser.add_argument('-u', '--upgrade', type=str, help='upgrade refpkg')
	args = parser.parse_args(argv[1:])
	if hasattr(args, 'upgrade'):
		cur.update_refpkg_run(args.upgrade, logger)


def make_log(log_name, log_fp):
	logger = logging.getLogger(log_name)
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(log_fp)
	formatter = logging.Formatter('%(levelname)s: %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.info('Log initiated - %s' % time.strftime("%c"))
	return logger

if __name__ == '__main__':
	main(sys.argv)
