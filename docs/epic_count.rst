epic-count
==========

epic-count creates a simple matrix of counts from the .bed/.bedpe files it is
given. These matrixes do not contain information about enrichment.

* **-i, --infiles**

  One or more bed/bedpe files to count reads in.

* **-o, --outfile**

   File to write results to. By default sent to stdout.

* **-cpu, --number-cores**

   The number of cores epic should use. Can at most take advantage of 1 core per
   strand per chromosome (i.e. 46 for humans). Default: 1

* **-gn, --genome**

   Which genome to analyze. By default hg19.

* **-k, --keep-duplicates**

   Keep reads mapping to the same position on the same strand within a library.
   The default is to remove all but the first duplicate (this is done once per
   file, not for all files collectively.)

* **-fs, --fragment-size**

   (Only used for single-end files) Size of the sequenced fragment. The center of
   the fragment will be used to calculate which window a read ended up in. So
   reads are shifted by fragment-size/2. Default 150.

* **-cs, --chromsizes**

   Set the chromosome lengths yourself in a file with two
   columns: chromosome names and sizes. Useful to analyze
   custom genomes, assemblies or simulated data. Only
   chromosomes included in the file will be analyzed.
