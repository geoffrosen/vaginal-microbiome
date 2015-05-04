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

def run_pplacer_pipeline(refpkg_fp, fasta_fp, config, logger):
	
	#set some variables
	commands = executer.MultipleCommands()
	
	# Deduplicate the fasta file
	#Should I do this pythonically?

	#Split the fasta based on the gcstripper.py info

	#Align the fasta to stockholm files

	#Merge these files with reference stockholm

	#Place the aligned files on the tree

	#Reduplicate 

	#Make DB

	#Classify seqs to DB

	#Pull info from DB

	#Make OTU Table

