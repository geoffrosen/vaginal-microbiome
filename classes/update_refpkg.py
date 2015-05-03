class UpdateRefpkg:

	'''for some reason, the updater included with
	   pplacer doesn't seem to be quite adequate
	   so this is an attempt to more fully automate the process'''

	#1. run the update_refpkg.py supplied with pplacer

	#2. add folder to hold old files

	#3. move cm, aligned fasta, and stockholm

	#4. cmconvert the oldcm

	#5. unalign the aligned fasta

	#6. realign the fasta with the converted cm
	# a. find the unaligned fasta and cm
	# b. realign

	#7. reformat the stockholm to afa
	
