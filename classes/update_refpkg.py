import os, shutil, json, executer

def update_refpkg_run(refpkg_fp,logger):

	'''for some reason, the updater included with
	   pplacer doesn't seem to be quite adequate
	   so this is an attempt to more fully automate the process'''
	
	#preamble - set some variables
	commands = executer.MultipleCommands()
	oldfolder = '%s/old/' % refpkg_fp
	json_fp = '%s/CONTENTS.json'% refpkg_fp
	replacements = {
		'tree_file': 'tree',
		'phylo_model_file': 'phylo_model',
	}
	fps = {
		'cm': 'profile',
		'afa': 'aln_fasta',
		'sto': 'aln_sto',
	}

	#1. make a directory to hold the old files
	logger.info('Now making folder to hold old files from %s' % refpkg_fp)
	try:
		os.mkdir(oldfolder)
	except:
		logger.warning('Folder already exists, attempting to continue')
	#2. make some changes to the json (idea and code for this from pplacer/scripts/update_refpkg.py and set some variables
	logger.info('Now moving a copy of the original json')
	shutil.copy(json_fp,oldfolder)
	with open(json_fp,'rb+') as json_file:
		json_contents = json.load(json_file)
		json_records = json_contents['files']
		for repl_in, repl_out in replacements.iteritems():
			if repl_in in json_records:
				logger.info('Now changing the json to show %s is now %s' % (repl_in, repl_out))
				json_records[repl_out] = json_records.pop(repl_in)
		logger.info('Now changing the metadata line')
		json_contents.setdefault('metadata', {})['format_version'] = '1.1'
		for var_name, json_name in fps.iteritems():
			logger.info('Now finding where the %s file is' % var_name)
			fps[var_name] = json_records[json_name]
		json_file.seek(0)
		json_file.truncate()
		json.dump(json_contents, json_file, indent=2)

	#3. move cm, aligned fasta, and stockholm
	for file_type, fp in fps.iteritems():
		logger.info('Now moving the %s file to %s' % (file_type, oldfolder))
		shutil.copy('%s/%s' % (refpkg_fp, fp), oldfolder)


	#4. cmconvert the oldcm
	commands.append('Change the cm format',\
		'Move the cm to an upgraded format',\
		'cmconvert',\
		{'-o': '%s/%s' % (refpkg_fp, fps['cm'])},\
		['%s%s' % (oldfolder, fps['cm'])])


	#5. unalign the aligned fasta
	fps['ufa'] = 'unaligned.fasta'

	commands.append('Unalign the aligned fasta',\
		'We have unalign the fasta to use it with the new cm',\
		'esl-reformat',\
		{'--informat': 'afa',\
		'-o': '%s%s' % (oldfolder, fps['ufa'])},\
		['fasta', '%s%s' % (oldfolder, fps['afa'])])
		

	#6. realign the fasta with the converted cm
	commands.append('Now we realign the fasta',\
		'We use the unaligned fasta and produce a pfam (sto)',\
		'cmalign',\
		{'--dnaout': '', '--outformat': 'Pfam',\
		'-o': '%s/%s' % (refpkg_fp, fps['sto'])},\
		['%s/%s' % (refpkg_fp, fps['cm']),\
		'%s%s' % (oldfolder, fps['ufa'])])

	#7. reformat the stockholm to afa
	commands.append('Now we convert this stockholm back to the afa',\
		'This was part of the original package, so we replace it',\
		'esl-reformat',\
		{'--informat': 'pfam',\
		'-o': '%s/%s' % (refpkg_fp, fps['afa'])},\
		['afa', '%s/%s' % (refpkg_fp, fps['sto'])])
	
	#8. execute all the above commands
	commands.execute_all(logger)
	
