from __future__ import print_function, division

import sys
import atexit
from subprocess import check_call, check_output
import os
from os.path import basename
import logging
from tempfile import TemporaryDirectory

from pyfaidx import Fasta

from epic.config import logging_settings


def effective_genome_size(fasta, read_length, nb_cores, tmpdir=None):
    """Compute effective genome size for genome."""

    idx = Fasta(fasta)

    genome_length = sum([len(c) for c in idx])

    logging.info("Temporary directory: " + tmpdir)
    logging.info("File analyzed: " + fasta)
    logging.info("Genome length: " + str(genome_length))
    print("File analyzed: ", fasta)
    print("Genome length: ", genome_length)

    chromosomes = ", ".join([c.name for c in idx])

    if "_" in chromosomes:
        print("Warning. The following chromosomes are part of your genome:\n",
              chromosomes.replace(">", "") + "\n",
              file=sys.stderr)
        print(
            "You probably want to remove all chromosomes in your fasta containing '_' for the effective genome size computation to be accurate.",
            file=sys.stderr)

    with TemporaryDirectory(prefix="epic-effective", dir=tmpdir) as output_dir:
        output_file = os.path.join(output_dir, '{1}.jf'.format(read_length,
                                                               basename(fasta)))
        check_call(
            "jellyfish count -t {nb_cores} -m {read_length} -s {genome_length} -L 1 -U 1 --out-counter-len 1 --counter-len 1 {fasta} -o {output_file}".format(
                **vars()),
            shell=True)

        stats = check_output("jellyfish stats {output_file}".format(
            output_file=output_file),
                             shell=True)

        unique_kmers = int(stats.split()[1])

        effective_genome_size = unique_kmers / genome_length

        logging.info("Number unique {read_length}-mers: ".format(
            read_length=read_length) + str(unique_kmers))
        logging.info("Effective genome size: " + str(effective_genome_size))
        print("Number unique {read_length}-mers: ".format(read_length=read_length),
              unique_kmers)
        print("Effective genome size: ", effective_genome_size)
        assert effective_genome_size < 1, "Something wrong happened, effective genome size over 1!"
