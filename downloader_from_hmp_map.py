import argparse, csv, os, logging, subprocess

from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from time import gmtime, strftime

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-i',help='comma separated input map files from HMP', required=True)
	parser.add_argument('-s',help='comma separated list of body sites',required=True)
	parser.add_argument('-j',help='threads',type=int,default=1)
	args = parser.parse_args()
	logname = 'import-%s' % strftime("%Y%m%d%H%M")
	logger = make_log(logname)
	map_files = args.i.split(',')
	locs_list = args.s.split(',')
	mapper = {}
	map_to_write = []
	for filename in map_files:
		with open(filename, 'rU') as f:
			r = csv.reader(f,delimiter='\t')
			header = r.next()
			for row in r:
				this_mapper = dict(zip(header,row))
				rid = this_mapper['RunID']
				bs = this_mapper['HMPBodySubsiteHMPBodySite']
				sid = this_mapper['SRS_SampleID']
				if bs not in locs_list:
					continue
				map_to_write.append(make_map_to_write_row(this_mapper))
				if rid not in mapper:
					mapper[rid] = this_mapper
				else:
					logger.warning('found two entries for %s saved just one fastq file but both %s and %s will be added to map' % (rid,sid,mapper[rid]['SRS_SampleID']))
	pool = ThreadPool(args.j)
	holder = [[mapper_item, logger] for nom,mapper_item in mapper.iteritems()]
	pool.map(dummy,holder)
	pool.close()
	pool.join()
	write_map(map_to_write, logger)
	logger.info('done')
	
def make_map_to_write_row(mapper_item):
	run_id = mapper_item['RunID']
	barc = mapper_item['BarcodeSequence']
	lps = mapper_item['LinkerPrimerSequence']
	body_site = mapper_item['HMPBodySubsiteHMPBodySite']
	sample_id = mapper_item['SRS_SampleID']
	region = mapper_item['Region']
	hsid = mapper_item['RSID']
	folder_to_save = body_site + '_' + region
	desc = 'loc and region %s sample %s' % (folder_to_save, sample_id)
	return [folder_to_save,run_id,barc,lps,region,body_site,run_id,hsid,sample_id,desc]
	

def write_map(map_to_write,logger):
	header = ['sample_name','barcode','primer','region','body_site','run_prefix','host_subject_id','sample_id','description']
	holder = {}
	for line in map_to_write:
		if line[0] not in holder:
			holder[line[0]] = []
		holder[line[0]].append(line[1:])
	for nom, items in holder.iteritems():
		save_loc = '%s.txt' % (nom)
		logger.info('now writing mapping file to %s' % (save_loc))
		with open(save_loc, 'wb') as f:
			w = csv.writer(f,delimiter='\t')
			w.writerow(header)
			for row in items:
				w.writerow(row)
		logger.info('done writing %s with %s items' % (save_loc, len(items)))

def dummy(holder_item):
	mapper_item, logger = holder_item
	region = mapper_item['Region']
	run_id = mapper_item['RunID']
	body_site = mapper_item['HMPBodySubsiteHMPBodySite']
	folder_to_save = body_site + '_' + region
	downloader(run_id, folder_to_save, logger)
	

def downloader(run_id, folder_to_save, logger):
	try_dir(folder_to_save, logger)
	com = 'fastq-dump %s -Q 64 --gzip' % (run_id)
	logger.info('sending cmd: %s' % (com))
	proc = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	logger.info('stdout: %s' % (out))
	logger.info('stderr: %s' % (err))
	orig_loc = '%s.fastq.gz' % (run_id)
	new_loc = '%s/%s.fastq.gz' % (folder_to_save, run_id)
	logger.info('moving %s to %s' % (orig_loc, new_loc))
	os.rename(orig_loc, new_loc)
	
def try_dir(folder, logger):
	try:
		os.mkdir(folder)
		logger.info('making folder: %s' % (folder))
	except:
		pass

		
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