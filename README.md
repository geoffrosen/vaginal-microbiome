# pplacer-runner

The goal of this is to have an easy way to start a job running on a pipeline based on pplacer (Matsen et al. 2010).
The only inputs needed:
  1. Unaligned demultiplexed, quality filtered, fasta file from your microbiome project
  2. A reference package

The output will be an OTU table, appropriate for use in many programs.

Here are the steps as I see them and as presented in Smith et al. 2012
  1. Deduplicate the fasta file
  2. Split the fasta file
  3. Align the fasta files to stockholm files
  4. Recombine the stockholm files and merge with the reference stockholm file
  5. Place the aligned files on to the reference tree
  6. Make an OTU table based on the full tree
  

References:

Matsen, F. A., Kodner, R. B., & Armbrust, E. V. (2010). pplacer: linear time maximum-likelihood and Bayesian phylogenetic 
  placement of sequences onto a fixed reference tree. BMC Bioinformatics, 11, 538. http://doi.org/10.1186/1471-2105-11-538

Smith, B. C., McAndrew, T., Chen, Z., Harari, A., Barris, D. M., Viswanathan, S., … Burk, R. D. (2012). The cervical microbiome
  over 7 years and a comparison of methodologies for its characterization. PLoS ONE, 7(7).
  http://doi.org/10.1371/journal.pone.0040425

