#!/usr/bin/env python

"""this will be the runner file"""
__author__ = 'Geoff Rosen'
__email__ = 'geoff.rosen <at> gmail.com'
__status__ = 'development'
__description__ = '''This program will help to run pplacer \n\
		from start to end'''

import argparse, logging, time, argparse, sys

from classes import update_refpkg as cur
from classes import config_parser as ccp
from classes import run_pplacer_pipeline as rpp

def main(argv):
	logger = make_log('pplacer-runner', 'pplacer-runner.log')
	logger.info('Initiated with command: %s' % ' '.join(argv))
	parser = argparse.ArgumentParser(description = __description__,\
		epilog = 'Note: refpkg, alignment, and config files are required without --upgrade')
	parser.add_argument('-u', '--upgrade', type=str, help='upgrade refpkg')
	parser.add_argument('-r', '--refpkg', type=str, help = 'previously updated refpkg file path. if not upgraded use -u')
	parser.add_argument('-f', '--fasta', type=str, help = 'unaligned fasta file path')
	parser.add_argument('-c', '--config', type=str, help = 'configuration file path formatted as command:title argument')
	parser.add_argument('-j', '--threads', type=int, help = 'threads to perform parallel options on', default = 4)
	args = parser.parse_args(argv[1:])
	if args.upgrade != None:
		cur.update_refpkg_run(args.upgrade, logger)
	elif args.refpkg != None and args.fasta != None:
		rpp.run_pplacer_pipeline(args.refpkg, args.fasta, logger, threads = args.threads)
	elif args.refpkg == None or args.fasta == None or args.config == None:
		parser.error('refpkg, fasta, and config are required')
	else:
		config_info = ccp.FullConfig(args.config)
		print config_info

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
