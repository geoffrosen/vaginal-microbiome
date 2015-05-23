import os, shutil, executer

'''
  this will construct and then execute
  this pipeline pipeline: 
  1. Deduplicate the fasta file
  2. Split the fasta file
  3. Align the fasta files to stockholm files
  4. Recombine the stockholm files and merge with the reference stockholm file
  5. Place the aligned files on to the reference tree
  6. Reduplicate the sequences
  7. Make an OTU table based on the full tree
  '''

def run_pplacer_pipeline(refpkg_fp, fasta_fp, config, logger, threads = 4):
	
	#set some variables
	commands = executer.MultipleCommands()
	dedup_fp = 
	dedup_fasta_fp = 
	splitter = 
	split_fastas_folder = 
	aligned_stos_folder = 
	parallel_jobs = 
	cm_fp = 
	merged_stos_folder = 
	ref_sto_fp = 
	trees_folder = 
	sql_fp = 
	dedup_csv_fp = 
	redup_csv_fp = 
	tax_level = 'species'
	otu_table_fp = 
	
	# Deduplicate the fasta file
	commands.append('Deduplicate fasta file', 'deduplicate the fasta file so we don\'t place it multiple times',
			'deduplicate_sequences.py',{'--deduplicated-sequences-file': dedup_fp},	['--keep-ids', fasta_fp, dedup_fasta_fp])

	#Should I do this pythonically?

	# Compress the original fasta file
	commands.append('Compress the original fasta file', 'we won\'t be using the fasta file anymore, so let\'t compress it',
			'gzip',{},[fasta_fp])

	# Make a directory to hold the split fastas
	os.mkdir(split_fastas_folder)

	#Split the fasta based on the splitter
	commands.append('Split the deduplicated fasta', 'split the deduplicated fasta so that we can do alignments in a timely manner',
			'split_sequence_file_on_sample_ids.py',{'-i':dedup_fasta_fp,'--file_type': 'fasta', '-o': split_fastas_folder},[])

	# Compress the deduplicated_fasta file
	commands.append('Compress the deduplicated fasta file',
			'we won\'t be using the deduplicated fasta file anymore, so let\'t compress it',
			'gzip',{},[dedup_fasta_fp])

	# Compress the split fasta files
	commands.append('Compress the deduplicated split fasta files',
			'we will be going through each of these slowly, so we can compress them all for now',
			'gzip',{},['-r',split_fastas_fp])
	

	# Make a folder for the aligned stos
	os.mkdir(aligned_stos_folder)


	# Run up to this point
	commands.execute_all(logger)


	#Align the fasta to stockholm files
	for split_fasta_gz in os.listdir(split_fastas_fp):
		commands.append('Decompress one of the fasta files',
				'decompress one file in preparation for alignment',
				'gunzip',{},[split_fastas_folder + '/' + split_fasta_gz])
		split_fasta_fp = split_fasta_gz[0:-3]
		split_sto_fp = '.'.join(split_fasta.split('.')[0:-1] + ['sto'])
		commands.append('Align this fasta file','align one fasta file to the refpkg',
				'cmalign',{'--cpu': parallel_jobs,'--outformat': 'Pfam','-o': aligned_stos_folder + '/' + split_sto_fp},
				['--dna', '-q', cm_fp, split_fastas_folder + '/' + split_fasta_fp])
		commands.append('Recompress the fasta file',
				'recompress the fasta file, we won\'t use it again',
				'gzip',{},[split_fastas_folder + '/' + split_fasta_fp])
		commands.append('Compress the sto file',
				'compress the sto file, we won\'t use it for a little while',
				'gzip',{},[aligned_stos_folder + '/' + split_sto_fp])
	
	# run up to this point
	commands.execute_all(logger)

	# I think this might be a waste! There must be a way to run this without merging

	# Make folder to hold merged alignments
	os.mkdir(merged_stos_folder)

	#Merge these files with reference stockholm
	for aligned_sto_gz in os.listdir(aligned_stos_folder):
		commands.append('Decompress one of the aligned sto files',
				'decompress one file in preparation for merging',
				'gunzip',{},[aligned_stos_folder + '/' + aligned_sto_gz])
		aligned_sto_fp = aligned_sto_gz[0:-3]
		commands.append('Merge the aligned file with the reference','merge the sto with the reference set',
				'esl-alimerge',{'--outformat': 'Pfam','-o': merged_stos_folder + '/' + aligned_sto_fp},
				['--dna', ref_sto_fp, aligned_stos_folder + '/' + aligned_sto_fp])
		commands.append('Recompress the aligned sto file',
				'recompress the aligned sto file, we won\'t use it again',
				'gzip',{},[aligned_stos_folder + '/' + aligned_sto_fp])
		commands.append('Compress the merged sto file',
				'compress the merged sto file, we won\'t use it for a little while',
				'gzip',{},[merged_stos_folder + '/' + aligned_sto_fp])
	# Run this section
	commands.execute_all(logger)

	# Make directory for all the trees
	os.mkdir(trees_folder)

	#Place the aligned files on the tree
	for merged_sto_gz in os.listdir(merged_stos_folder):
		commands.append('Decompress one of the merged sto files',
				'decompress one file in preparation for pplacing',
				'gunzip',{},[merged_stos_folder + '/' + merged_sto_gz])
		merged_sto_fp = aligned_sto_gz[0:-3]
		tree_fp = split_sto_fp = '.'.join(split_fasta.split('.')[0:-1] + ['jplace'])
		commands.append('Pplace the merged sto','pplace the merged sto onto the reference tree',
				'pplacer',{'-o': trees_folder + '/' + tree_fp, '-c': refpkg_fp, '-j': parallel_jobs},
				['-p', '--mrca-class', '--inform-prior', merged_stos_folder + '/' + merged_sto_fp])
		commands.append('Recompress the merged sto file',
				'recompress the merged sto file, we won\'t use it again',
				'gzip',{},[merged_stos_folder + '/' + merged_sto_fp])
		commands.append('Compress the jplace file',
				'compress the jplace file, we won\'t use it for a little while',
				'gzip',{},[trees_folder + '/' + trees_fp])

	# Do the pplacing
	commands.execute_all(logger)

	# Make DB
	commands.append('Make database', 'make the database that will hold the eventual classifications',
			'rppr prep_db', {'--sqlite': sql_fp, '-c': refpkg_fp},[])

	#Classify seqs to DB
	for tree_gz in os.listdir(trees_folder):
		commands.append('Decompress one of the jplace tree files',
				'decompress one file in preparation for classification',
				'gunzip',{},[trees_folder + '/' + tree_gz])
		commands.append('Classify the seqs from the tree','classify the seqs from the tree',
				'guppy classify',{'--sqlite': sql_fp, '-c': refpkg_fp},
				['--pp', '--mrca-class', trees_folder + '/' + tree_fp])
		commands.append('Recompress the jplace tree file',
				'recompress the jplace tree file, we won\'t use it again',
				'gzip',{},[trees_folder + '/' + tree_fp])

	# Execute classification
	commands.execute_all(logger)

	#Pull info from DB
	#this is taken from the sqlit3_script.sh
	#wanted to modify it so that I could control input and output
	sql = "SELECT placement_names.name, taxa.tax_name, rank, pc.likelihood FROM placement_classifications AS pc INNER JOIN taxa ON pc.tax_id=taxa.tax_id INNER JOIN placement_names ON pc.placement_id=placement_names.placement_id WHERE rank=rank ORDER BY placement_names.name"
	commands.append('Pull information from database', 'put the information into a csv',
			'sqlite3',{},['-header','-csv', sql_fp, '"' + sql +'"', dedup_csv_fp])

	# Redup csv
	commands.append('Redup the csv', 'reduplicate the sequences from the csv file with the dedup file',
			'redup_from_csv.py', {'-i': dedup_csv_fp, '-o': redup_csv_fp, '-d': dedup_fp},[])

	#Make OTU Table
	commands.append('Make OTU table', 'make an otu table to the specified level using the reduplicated csv',
			'gcstripper.py', {'-i': redup_csv_fp, '-o': otu_table_fp, '-r': tax_level, '-s': splitter}, [])

