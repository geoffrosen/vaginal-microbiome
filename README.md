# vaginal-microbiome

The script bin/custom_lefse/ppr.py is meant to help with the plotting of lefse res files

1. The feature names are from qiime "k__Bacteria.p__Proteobacteria.c__Gammaproteobacteria.o__Pseudomonadales.f__Pseudomonadaceae.g__Pseudomonas.s__viridiflava"

`ppr.py input.res output.png --qime-print "g s"`

--"g s" will have the above as feature Pseudomonas viridiflava. If the feature does not have a g or an s, it will use the furthest to the right (so "k__Bacteria" will be "Bacteria"). 

2. The feature names have been customized "Pseudomonas_viridiflava"

`use command: ppr.py input.res output.png --remove "_" --repl " "`

--this will work on both the feature names and the status names ("Status_Positive" will become "Status Positive")

3. You want to italicize the feature names

`ppr.py input.res output.png --italicize`

All of these can be used together.

For some, phylosift (Darling et. al 2014) may be more appropriate. See it [here](https://github.com/gjospin/PhyloSift)

Commands available:

  1. You can now update a refpkg fully (including modifying the cm, sto, and afa)

Command:

     pplacerrunner.py -u /path/to/refpkg

or

     pplacerrunner.py --upgrade /path/to/refpkg

  2. You can now add a class to your otu table and modify it for lefse usage and normalize by copy number with modify_otu_table.py

Command:

     modify_otu_table.py -i /input/file -o /output/file -m /map/file -s start_id -e end_id -c class_name [-l -n --in-splitter ";" --out-splitter "|"]

To see all commands:

     modify_otu_table.py -h


Note: paths can be relative

The goal of this is to have an easy way to run a job on pipeline based on pplacer (Matsen et al. 2010).
The only inputs required will be:
  1. Unaligned demultiplexed, quality filtered, fasta file from your microbiome project
  2. A reference package
  3. A config file (though a default one will be provided with the package)

Of course, there will be other optional inputs to do some other funcitons.

The output will be an OTU table, appropriate for use in many programs.

Here are the steps as I see them and as presented in Smith et al. 2012 and in Srinivasan et al. 2012
  1. Deduplicate the fasta file
  2. Split the fasta file
  3. Align the fasta files to stockholm files
  4. Recombine the stockholm files and merge with the reference stockholm file
  5. Place the aligned files on to the reference tree
  6. Reduplicate the sequences
  7. Make an OTU table based on the full tree

Included in this package:
  1. pplacer v1.1 for linux 
  2. mubiomics (available [here](https://github.com/benjsmith/mubiomics))
  3. infernal v1.1.1 for linux (available [here](http://infernal.janelia.org/)). This was made on a qiime virtualbox v 1.9

References:

Darling, A. E., Jospin, G., Lowe, E., Matsen, F. a, Bik, H. M., & Eisen, J. a. (2014). PhyloSift: phylogenetic analysis of genomes and metagenomes. PeerJ, 2, e243. http://doi.org/10.7717/peerj.243

Matsen, F. A., Kodner, R. B., & Armbrust, E. V. (2010). pplacer: linear time maximum-likelihood and Bayesian phylogenetic placement of sequences onto a fixed reference tree. BMC Bioinformatics, 11, 538. http://doi.org/10.1186/1471-2105-11-538

Smith, B. C., McAndrew, T., Chen, Z., Harari, A., Barris, D. M., Viswanathan, S., … Burk, R. D. (2012). The cervical microbiome over 7 years and a comparison of methodologies for its characterization. PLoS ONE, 7(7). http://doi.org/10.1371/journal.pone.0040425

Srinivasan, S., Hoffman, N. G., Morgan, M. T., Matsen, F. A., Fiedler, T. L., Hall, R. W., … Fredricks, D. N. (2012). Bacterial communities in women with bacterial vaginosis: High resolution phylogenetic analyses reveal relationships of microbiota to clinical criteria. PLoS ONE, 7(6). http://doi.org/10.1371/journal.pone.0037818
