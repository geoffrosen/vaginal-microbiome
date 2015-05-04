#!/usr/bin/env python

"""this will be the runner file"""
__author__ = 'Geoff Rosen'
__email__ = 'geoff.rosen <at> gmail.com'
__status__ = 'development'

import argparse, logging, time

def make_log(log_name, log_fp):
	logger = logging.getLogger(log_name)
	logger.setLevel(logging.INFO)
	handler = logging.FileHandler(log_fp)
	formatter = logging.Formatter('%(levelname)s: %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	logger.info('Log initiated - %s' % time.strftime("%c"))
	return logger
